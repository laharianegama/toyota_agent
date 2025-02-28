import time
import re
import random
import json
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from orchestration.logger import setup_logger
from orchestration.state import MultiAgentState
from workflows.test_drive_workflow.data.test_drive_mock_data import TEST_DRIVE_SLOTS
from workflows.test_drive_workflow.test_drive_prompt import get_test_drive_prompt

logger = setup_logger(__name__)

# Global variable to store displayed dealerships for each thread
displayed_dealerships = {}

def handle_test_drive(llm, state: MultiAgentState):
    try:
        logger.info("Processing test drive request")
        question = state.get('question', '')
        thread_id = state.get('configurable', {}).get('thread_id', '1')
        context = state.get('context')
        
        # Check if we're in test drive context and user is selecting a dealership
        if context == "test_drive" and thread_id in displayed_dealerships:
            # User is selecting a dealership
            dealership_match = re.search(r'(?:dealership|slot)\s*(\d+)', question.lower())
            if dealership_match:
                selection_index = int(dealership_match.group(1)) - 1
                available_dealerships = displayed_dealerships.get(thread_id, [])
                
                if 0 <= selection_index < len(available_dealerships):
                    # Valid selection
                    selected_dealership = available_dealerships[selection_index]
                    
                    # Generate booking reference
                    booking_ref = f"TD-{int(time.time())}"
                    
                    # Format confirmation message
                    confirmation_msg = f"""✅ Test drive scheduled!

🚗 Vehicle: {state.get('preferred_model', 'Toyota')}
🏢 Dealership: {selected_dealership['dealership']}
📍 Location: {selected_dealership['location']}
⏰ Hours: {selected_dealership.get('hours', 'Regular business hours')}
☎️ Phone: {selected_dealership.get('phone', 'Contact dealership for details')}
🔖 Booking Reference: {booking_ref}

A representative will contact you soon to arrange the specific date and time for your test drive.
Thank you for choosing Toyota!
"""
                    # Clear context since we're done
                    return {
                        "answer": confirmation_msg,
                        "context": None  # Clear context
                    }
                else:
                    return {
                        "answer": f"Sorry, that's not a valid selection. Please choose a dealership number between 1 and {len(available_dealerships)}.",
                        "context": "test_drive"  # Maintain context
                    }
            else:
                return {
                    "answer": "I didn't understand your selection. Please reply with the dealership number (e.g., 'dealership 3' or just '3').",
                    "context": "test_drive"  # Maintain context
                }
        
        # Initial test drive request - extract requirements and show options
        try:
            # Use LLM to extract details
            prompt = get_test_drive_prompt()
            response = llm.invoke(prompt.format(question=question))
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{[^{]*"preferred_model"[^}]*\}', response.content, re.DOTALL)
            if json_match:
                try:
                    requirements = json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    requirements = {}
            else:
                requirements = {}
                
            # Fall back to simple extraction if needed
            if 'preferred_model' not in requirements:
                requirements['preferred_model'] = extract_model(question)
            if 'preferred_location' not in requirements:
                requirements['preferred_location'] = extract_location(question)
        except Exception as e:
            logger.warning(f"Error extracting requirements: {e}")
            requirements = {
                'preferred_model': extract_model(question),
                'preferred_location': extract_location(question)
            }
            
        # Store the preferred model in state
        preferred_model = requirements.get('preferred_model', 'Toyota')
        preferred_location = requirements.get('preferred_location')
        
        # Get available dealerships
        available_dealerships = TEST_DRIVE_SLOTS
        
        if not available_dealerships:
            return {"answer": "Sorry, there are no dealerships available for test drives at this time."}
        
        # If location specified, find closest dealerships
        if preferred_location and preferred_location.lower() not in ["null", "none"]:
            try:
                # Sort dealerships by proximity to location
                sorted_dealerships = find_closest_dealerships(llm, preferred_location, available_dealerships)
                location_message = f"Here are dealerships closest to {preferred_location} for your test drive:"
            except Exception as e:
                logger.warning(f"Error finding closest dealership: {e}")
                sorted_dealerships = available_dealerships
                location_message = "Here are our available dealerships for your test drive:"
        else:
            sorted_dealerships = available_dealerships
            location_message = "Here are our available dealerships for your test drive:"
        
        # Limit to 5 dealerships for display
        display_dealerships = sorted_dealerships[:5]
        
        # Store displayed dealerships for this thread
        displayed_dealerships[thread_id] = display_dealerships
        
        # Format dealerships for display
        dealership_display = format_dealerships(display_dealerships, preferred_model)
        
        response = f"""Thanks for your interest in test driving {preferred_model if preferred_model and preferred_model.lower() not in ["null", "none"] else "a Toyota"}.

{location_message}

{dealership_display}

To schedule your test drive, please reply with the dealership number (e.g., 'dealership 3').
"""
        
        # Set context to test_drive
        return {
            "answer": response,
            "context": "test_drive",  # Set context
        }
    
    except Exception as e:
        logger.error(f"Error in handle_test_drive: {e}")
        return {"answer": "Sorry, I encountered an error while processing your test drive request. Please try again or contact our customer service."}

def extract_model(question):
    """Simple function to extract Toyota model from text"""
    toyota_models = [
        "camry", "corolla", "rav4", "highlander", "tacoma", "tundra", 
        "4runner", "sienna", "prius", "yaris", "avalon", "supra", 
        "gr86", "venza", "chr", "sequoia", "land cruiser"
    ]
    
    question_lower = question.lower()
    
    for model in toyota_models:
        if model in question_lower:
            return model.capitalize()
    
    return None

def extract_location(question):
    """Simple function to extract location from text"""
    # Look for common location patterns
    location_patterns = [
        r'near\s+([A-Za-z\s]+)',
        r'in\s+([A-Za-z\s]+)',
        r'at\s+([A-Za-z\s]+)',
        r'around\s+([A-Za-z\s]+)'
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, question.lower())
        if match:
            # Clean up the extracted location
            location = match.group(1).strip()
            # Remove common stop words at the end
            location = re.sub(r'\s+(area|city|town|region)$', '', location)
            return location
    
    return None

def find_closest_dealerships(llm, user_location, available_dealerships):
    """Sort dealerships by proximity to user's location using LLM"""
    try:
        logger.info(f"Finding closest dealerships to {user_location}")
        
        # Create a prompt for the LLM to rank dealerships by proximity
        dealership_info = []
        for i, d in enumerate(available_dealerships):
            dealership_info.append(f"{i+1}. {d['dealership']} - {d['location']}")
        
        dealership_list = "\n".join(dealership_info)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a geographic proximity expert. Given a user location and a list of dealerships, rank the dealerships from closest to furthest.

            Return a JSON array of indices representing the ranking. For example, if dealership 3 is closest, followed by dealership 1, then dealership 2, you would return:
            [3, 1, 2]

            Only return the JSON array, nothing else.
            """),
                        ("human", f"""User location: {user_location}

            Dealership options:
            {dealership_list}

            Rank these dealerships from closest to furthest to {user_location}:""")
        ])
        
        response = llm.invoke(prompt)
        logger.info(f"LLM ranking response: {response.content}")
        
        # Try to extract JSON array from response
        matches = re.search(r'\[.*\]', response.content, re.DOTALL)
        if matches:
            try:
                ranking = json.loads(matches.group(0))
                # Adjust indices (LLM might use 1-based indexing)
                ranking = [i-1 if i > 0 else i for i in ranking]
                # Filter valid indices
                ranking = [i for i in ranking if 0 <= i < len(available_dealerships)]
                # Get remaining indices not in ranking
                remaining = [i for i in range(len(available_dealerships)) if i not in ranking]
                # Complete ranking
                full_ranking = ranking + remaining
                # Sort dealerships by ranking
                return [available_dealerships[i] for i in full_ranking]
            except json.JSONDecodeError:
                pass
        
        # Fallback to original order
        return available_dealerships
    
    except Exception as e:
        logger.error(f"Error finding closest dealerships: {e}")
        return available_dealerships

def format_dealerships(dealerships, preferred_model):
    """Format the dealerships for display with model availability"""
    formatted = ""
    
    for i, dealership in enumerate(dealerships):
        # Check if preferred model is available
        available_models = dealership.get('available_models', [])
        model_available = preferred_model and preferred_model.lower() not in ["null", "none"] and \
                         any(preferred_model.lower() in model.lower() for model in available_models)
        
        model_status = f"✓ {preferred_model} available" if model_available else ""
        
        formatted += f"[{i+1}] {dealership['dealership']}\n"
        formatted += f"   📍 {dealership['location']}\n"
        formatted += f"   ⏰ {dealership.get('hours', 'Regular business hours')}\n"
        if model_status:
            formatted += f"   🚗 {model_status}\n"
        formatted += "\n"
    
    return formatted
