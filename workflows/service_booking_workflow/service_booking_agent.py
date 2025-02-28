import uuid
from langchain_core.messages import HumanMessage, AIMessage
from orchestration.logger import setup_logger
from orchestration.state import MultiAgentState
from workflows.service_booking_workflow.service_booking_prompt import get_service_booking_prompt
from workflows.service_booking_workflow.data.service_slots_mock_data import SERVICE_SLOTS
import re,random

logger = setup_logger(__name__)


LATEST_SHOWN_SLOTS = []
def handle_service_booking(llm_for_router, state: MultiAgentState): 
    try:
        logger.info("Processing service booking node")
        
        global LATEST_SHOWN_SLOTS
        
        question = state.get('question', '')
        logger.info(f"Service booking processing question: {question}")
        
                # Check if this is a slot selection
        slot_pattern = r'(?:slot\s*)?(\d+)'
        slot_match = re.search(slot_pattern, question.lower())
        
        if slot_match and LATEST_SHOWN_SLOTS:
            # User is selecting a slot
            try:
                slot_num = int(slot_match.group(1))
                logger.info(f"User selected slot number: {slot_num}")
                
                # Check if it's a valid slot number
                if 1 <= slot_num <= len(LATEST_SHOWN_SLOTS):
                    selected_slot = LATEST_SHOWN_SLOTS[slot_num - 1]
                    
                    # Generate booking reference
                    booking_ref = f"SB-{uuid.uuid4().hex[:8].upper()}"
                    
                    # Format confirmation message
                    confirmation_msg = f"""✅ Service appointment confirmed! Here are your booking details:

📅 Date: {selected_slot['date']}
⏰ Time: {selected_slot['time']}
📍 Location: {selected_slot['location']}
⏱️ Estimated Duration: {selected_slot['duration']} minutes
🔖 Booking Reference: {booking_ref}

A confirmation has been sent to your registered email address. If you need to reschedule or cancel, please quote your booking reference.

Is there anything else I can help you with today?"""

                    return {"answer": confirmation_msg, "context": "None"}
                else:
                    return {"answer": f"Sorry, that's not a valid slot number. Please choose a slot number between 1 and {len(LATEST_SHOWN_SLOTS)}."}
            except Exception as e:
                logger.error(f"Error processing slot selection: {e}")
                return {"answer": "I couldn't understand which slot you wanted. Please reply with the slot number (e.g., 'slot 3' or just '3')."}
        
        # Find available slots
        available_slots = [
            slot for slot in SERVICE_SLOTS if slot["available"]
        ]
        
        if not available_slots:
            return {"answer": "Sorry, there are no available service slots at this time."}
        
        slots_display = format_available_slots(available_slots[:15])

        LATEST_SHOWN_SLOTS = available_slots
        logger.info(f"Stored {len(available_slots)} slots for selection")
        
        response = f"""Thanks for your interest in booking an appointment for your Toyota vehicle.

Here are the available service slots:

{slots_display}

To select a slot, simply reply with the slot number (e.g., 'slot 3' ).
"""
        
        return {"answer": response, "context": "service_booking"}
    except Exception as e:
        logger.error(f"Error in handle_service_booking: {e}")
        return {"answer": "Sorry, I encountered an error while processing your request. Please try again later."}


def format_available_slots(slots):
    """Format the available slots for display"""
    formatted = ""
    
    # Group by date first
    slots_by_date = {}
    for slot in slots:
        date = slot["date"]
        if date not in slots_by_date:
            slots_by_date[date] = []
        slots_by_date[date].append(slot)
    
    # Display slots grouped by date
    slot_number = 1
    for date, date_slots in slots_by_date.items():
        formatted += f"\n{date}:\n"
        
        for slot in date_slots:
            formatted += f"[{slot_number}] {slot['time']} - {slot['location']}\n"
            slot_number += 1
    
    return formatted