import uuid
from langchain_core.messages import HumanMessage
from orchestration.logger import setup_logger
from orchestration.state import MultiAgentState
from workflows.service_booking_workflow.service_booking_prompt import get_service_booking_prompt
from workflows.service_booking_workflow.data.service_slots_mock_data import SERVICE_SLOTS

logger = setup_logger(__name__)

def handle_service_booking(llm_for_router, state: MultiAgentState): 
    try:
        logger.info("Processing service booking node")
        
        messages = state['messages']
        human_msg = HumanMessage(state['question'])
        messages = messages + [human_msg]

        # Find available slots
        available_slots = [
            slot for slot in SERVICE_SLOTS if slot["available"]
        ]
        
        if not available_slots:
            return {"answer": "Sorry, there are no available service slots at this time."}
        
        # Randomly select a slot
        import random
        selected_slot = random.choice(available_slots)
        
        # Generate booking reference
        booking_ref = f"SB-{uuid.uuid4().hex[:8].upper()}"
        
        # Format confirmation message
        confirmation_msg = f"""✅ Service appointment automatically booked for you! Below are the details!!
📅 Date: {selected_slot['date']}
⏰ Time: {selected_slot['time']}
📍 Location: {selected_slot['location']}
🔖 Booking Reference: {booking_ref}"""
        
        return {"answer": confirmation_msg}
    except Exception as e:
        logger.error(f"Error in handle_service_booking: {e}")
        raise