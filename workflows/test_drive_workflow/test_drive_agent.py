import time
from langchain_core.messages import HumanMessage
from orchestration.logger import setup_logger
from orchestration.state import MultiAgentState
from workflows.test_drive_workflow.data.test_drive_mock_data import TEST_DRIVE_SLOTS

logger = setup_logger(__name__)

def handle_test_drive(state: MultiAgentState):
    try:
        logger.info("Processing test drive request")
        messages = state['messages']

        human_msg = HumanMessage(state['question'])
        messages = messages + [human_msg]

        # Get available dealerships
        available_dealerships = TEST_DRIVE_SLOTS
        
        if not available_dealerships:
            return {"answer": "Sorry, there are no dealerships available for test drives at this time."}
        
        # Randomly select a dealership
        import random
        dealership = random.choice(available_dealerships)
        
        # Generate booking reference
        booking_ref = f"TD-{int(time.time())}"
        
        # Format confirmation message
        confirmation_msg = f"""✅ Test drive automatically scheduled!
🏢 Dealership: {dealership['dealership']}
📍 Location: {dealership['location']}
🔖 Booking Reference: {booking_ref}

A representative will contact you soon to arrange the details of your test drive."""
        
        return {"answer": confirmation_msg}
    
    except Exception as e:
        logger.error(f"Error in handle_test_drive: {e}")
        raise