from langchain_core.messages import HumanMessage, AIMessage
from orchestration.logger import setup_logger
from orchestration.state import MultiAgentState
from workflows.router_workflow.router_prompt import get_router_prompt
import re

logger = setup_logger(__name__)

def router_agent(llm_for_router, state: MultiAgentState):  
    try:
        logger.info(f"Routing question: {state['question']}")
        messages = state['messages']
        human_msg = HumanMessage(state['question'])
        messages = messages + [human_msg]
        
        context = state.get('context', 'none')
        question = state.get('question', '').strip()
        
        # If there's an active context, route to that workflow
        if context == "service_booking":
            return {"question_type": "ServiceBooking", 'messages': [HumanMessage(question)]}
        elif context == "test_drive":
            return {"question_type": "TestDrive", 'messages': [HumanMessage(question)]}
        elif context == "vehicle_check":
            return {"question_type": "VehicleCheck", 'messages': [HumanMessage(question)]}
        
        supervisor_chain = get_router_prompt() | llm_for_router
        response = supervisor_chain.invoke({"question": messages})
        

        # Check if the response was filtered
        if 'content_filter_result' in response:
            logger.warning(
                "The response was filtered due to content management policy.")
            return {"question_type": "Error", 'messages': human_msg }

        logger.info(f"Routing to: {response.content}")
        return {"question_type": response.content, 'messages': [human_msg]}
    except Exception as e:
        logger.error(f"Error in router_agent: {e}")
        raise

def route_question(state: MultiAgentState):
    try:
        logger.info(f"Routing question: {state['question_type']}")
        return state['question_type']
    except Exception as e:
        logger.error(f"Error in route_question: {e}")
        raise
