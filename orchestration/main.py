import os
import getpass
import json
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse

from orchestration.state import MultiAgentState
from orchestration.workflowManager import WorkflowManager
from orchestration.llmManager import LLMManager
from models.models import Query, QueryResponse
from langchain.globals import set_debug, set_verbose
from langgraph.graph import END 
from orchestration.logger import setup_logger
from orchestration.langsmith_setup import setup_langsmith



logger = setup_logger(__name__)

# Load environment variables
load_dotenv()

if os.getenv("ENABLE_DEBUGGING") == "true":
    set_debug(True)
else:
    set_verbose(True)

def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}")

# Setup LangSmith
langsmith_callbacks = setup_langsmith()

# Initialize managers
try:
    logger.info("Initializing managers")
    llm_manager = LLMManager()
    workflow_manager = WorkflowManager(llm_manager=llm_manager)
    logger.info("Managers initialized successfully")
except Exception as e:
    logger.error(f"Error initializing managers: {e}")
    raise

# Create workflow graph
try:
    logger.info("Generating workflow graph")
    graph = workflow_manager.generate_graph()
    logger.info("Workflow graph generated successfully")
except Exception as e:
    logger.error(f"Error generating workflow graph: {e}")
    raise

# Initialize FastAPI app
app = FastAPI()

# Setup CORS middleware
origins = ["http://localhost:4200", "http://localhost:3005"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/query")

# Global state dictionary - will persist until server restart
conversation_states = {}
@app.post("/query")
async def runQuery(query: Query) -> QueryResponse:
    try:
        logger.info(f"Processing query: {query.query}")
        finalResponse = QueryResponse(message="Processing query...")
        thread_id = query.thread_id if hasattr(query, 'thread_id') else "1"
        config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 100, "tags":["Toyota Assistant"]}
        response=[]
        
        # in-memory dictionary to store conversation states
        global conversation_states
        existing_state = conversation_states.get(thread_id, {})
        
        
        # Input data with preserved state
        input_data = {
            "question": query.query,
            "messages": existing_state.get("messages", []),
            "question_type": existing_state.get("question_type", ""),
            "answer": "",
            "available_slots": existing_state.get("available_slots", None),
            "available_dealerships": existing_state.get("available_dealerships", None),
            "context": existing_state.get("context", None)
        }
        
        run_name = f"Toyota Assistant - {query.query[:30]}..."
        # Add run name to config if we have LangSmith enabled
        if langsmith_callbacks:
            config["run_name"] = run_name
            
        latest_state = {}
        
        for stream_data in graph.stream(input_data, config):
            if "__end__" not in stream_data:
                response.append(stream_data)
                node_response = (
                    stream_data.get('vehicle_check_node') or
                    stream_data.get('service_booking_node') or
                    stream_data.get('test_drive_node') or
                    stream_data.get('no_context_node')
                )
               
                if node_response:
                    finalResponse.message = node_response.get('answer')
                    
                    latest_state = {
                    "context": node_response.get("context"),
                    "messages": node_response.get("messages", input_data["messages"]),
                    "question_type": input_data["question_type"],
                    "available_slots": node_response.get("available_slots", input_data["available_slots"]),
                    "available_dealerships": node_response.get("available_dealerships", input_data["available_dealerships"]),
                    }
                    conversation_states[thread_id] = latest_state
    
        
        if finalResponse.message == "":
            finalResponse.message = "Sorry, I am not able to understand your query. Please try again."
        logger.info(f"Query processed successfully: {finalResponse.message}")
        return finalResponse
    except Exception as e: 
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Error processing query")
    


@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=QueryResponse(
            message="Validation error occurred",
        ).dict()
    )

def handleInterrupts(query, config, state, input):
    try:
        logger.info("Handling potential workflow interrupts")
        
        # List of nodes that might require special interrupt handling
        interrupt_nodes = [
            "router_node", 
            "test_drive_node", 
            "service_booking_node", 
            "vehicle_check_node",
            "no_context_node"
        ]
        
        # Check if any tasks are in an unexpected state
        if state.tasks:
            for task in state.tasks:
                if task.name in interrupt_nodes:
                    logger.info(f"Interrupt detected in node: {task.name}")
                    
                    # Reset input or update state as needed
                    input = None
                    graph.update_state(config=config, values={
                        "question": query.query,
                        "messages": [],
                        "question_type": "",
                        "answer": ""
                    })
        
        logger.info("Interrupt handling completed successfully")
        return input
    
    except Exception as e:
        logger.error(f"Error in interrupt handling: {e}")
        # Log the full error for debugging
        logger.exception("Detailed interrupt handling error")
        raise

if __name__ == "__main__":
    try:
        logger.info("Starting the application")
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.error(f"Error starting the application: {e}")
        raise


#start the FAST API server
#python -m uvicorn orchestration.main:app --reload --port 8000

