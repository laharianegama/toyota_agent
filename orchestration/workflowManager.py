from langgraph.graph import StateGraph, END
from orchestration.state import MultiAgentState
from orchestration.llmManager import LLMManager
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.errors import NodeInterrupt
from dateutil.parser import isoparse
from langchain_community.chat_message_histories import ChatMessageHistory
from orchestration.state import MultiAgentState  # Ensure correct import
from langchain.schema import HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langgraph.checkpoint.memory import MemorySaver 
from orchestration.logger import setup_logger
from langgraph.types import interrupt
import os,re, json
from datetime import datetime
import ntpath
import time, uuid   
from dotenv import load_dotenv

from workflows.router_workflow.router_agent import router_agent, route_question
from workflows.vehicle_check_workflow.vehicle_check_agent import check_vehicle_availability
from workflows.service_booking_workflow.service_booking_agent import handle_service_booking
from workflows.test_drive_workflow.test_drive_agent import handle_test_drive
from workflows.no_context_workflow.no_context_agent import no_context_node


load_dotenv()

logger = setup_logger(__name__)

class WorkflowManager:
    def __init__(self, llm_manager: LLMManager,callbacks=None):
        try:
            logger.info("Initializing WorkflowManager")
            self.llm_manager = llm_manager
            self.llm = llm_manager.llm
            self.llm_for_router = llm_manager.llm_for_router
            self.callbacks = callbacks
            logger.info("WorkflowManager initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing WorkflowManager: {e}")
            raise

    def create_workflow(self) -> StateGraph:
        workflow = StateGraph(MultiAgentState)
        
        # Core router - use a lambda to pass both LLM and state
        workflow.add_node("router_node", lambda state: router_agent(self.llm_for_router, state)
        )
        workflow.set_entry_point("router_node")
        
        # Vehicle Availability Workflow
        workflow.add_node("vehicle_check_node", 
            lambda state: check_vehicle_availability(self.llm, state)
        )
        
        # Service Appointment Workflow
        workflow.add_node("service_booking_node", 
            lambda state: handle_service_booking(self.llm_for_router, state)
        )

        # Test Drive Workflow
        workflow.add_node("test_drive_node", 
            lambda state: handle_test_drive(self.llm, state)
        )
        
        workflow.add_node("no_context_node", 
            lambda state: no_context_node(self.llm, state)
        )

        # Add conditional edges
        workflow.add_conditional_edges(
            "router_node",
            route_question,
            {
                'VehicleCheck': 'vehicle_check_node',
                'ServiceBooking': 'service_booking_node',
                'TestDrive': 'test_drive_node',
                'NoContext': 'no_context_node'
            }
        )
        
        # Add edges to END for each node
        workflow.add_edge("vehicle_check_node", END)
        workflow.add_edge("no_context_node", END)
        workflow.add_edge("service_booking_node", END)
        workflow.add_edge("test_drive_node", END)

        return workflow

    def generate_graph(self):
        try:
            logger.info("Generating workflow graph")
            memory = MemorySaver()
            enableDebugging = os.getenv("ENABLE_DEBUGGING") == "true"
            
            # Pass callbacks to the graph compilation if available
            if self.callbacks:
                graph = self.create_workflow().compile(
                    checkpointer=memory, 
                    debug=enableDebugging,
                    callback_manager=self.callbacks
                )
            else:
                graph = self.create_workflow().compile(
                    checkpointer=memory, 
                    debug=enableDebugging
                )
                
            graph.name = "Toyota Assistant Graph"
            
            # Draw the graph and get the bytes
            image_bytes = graph.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
            )

            # Save the bytes to an image file
            with open("workflow_graph.png", "wb") as image_file:
                image_file.write(image_bytes)
            logger.info("Workflow graph generated successfully")
            return graph
        except Exception as e:
            logger.error(f"Error generating workflow graph: {e}")
            raise