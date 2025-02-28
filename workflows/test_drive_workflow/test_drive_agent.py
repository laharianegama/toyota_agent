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

def handle_test_drive(llm, state: MultiAgentState):
    try:
        logger.info("Processing test drive request")
        question = state.get('question', '')
        
        # Simple fail-safe extraction first
        requirements = {
            "preferred_model": extract_model(question),
            "preferred_location": extract_location(question),
            "preferred_date": None,
            "preferred_time": None
        }
        
        # Try to use LLM for better extraction, but doesn't fail if it doesn't work
        try:
            prompt = get_test_drive_prompt()
            response = llm.invoke(prompt.format(question=question))
            logger.info(f"Test drive extraction response: {response.content}")
            
            # Try to extract JSON from the response using regex
            json_match = re.search(r'\{[^{]*"preferred_model"[^}]*\}', response.content, re.DOTALL)
            if json_match:
                try:
                    extracted_data = json.loads(json_match.group(0))
                    # Only update if we successfully parsed
                    requirements.update(extracted_data)
                    logger.info(f"Successfully extracted requirements: {requirements}")
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON: {e}")
        except Exception as e:
            logger.warning(f"LLM extraction failed, using fallback: {e}")
        
        # Get available dealerships
        available_dealerships = TEST_DRIVE_SLOTS
        
        if not available_dealerships:
            return {"answer": "Sorry, there are no dealerships available for test drives at this time."}
        
        # Check if user specified a location
        preferred_location = requirements.get("preferred_location")
        preferred_model = requirements.get("preferred_model", "Toyota")
        
        if preferred_location and preferred_location.lower() not in ["null", "none"]:
            # User specified a location - find closest match
            try:
                closest_dealership = find_closest_dealership(llm, preferred_location, available_dealerships)
                dealership = closest_dealership
                location_message = f"I've found a dealership closest to {preferred_location}."
            except Exception as e:
                logger.warning(f"Error finding closest dealership: {e}")
                # Fallback to random
                dealership = random.choice(available_dealerships)
                location_message = "I've selected a dealership for your test drive."
        else:
            # No location specified - select random dealership
            dealership = random.choice(available_dealerships)
            location_message = "I've selected a dealership for your test drive."
        
        # Check if the model is available at this dealership
        available_models = dealership.get("available_models", [])
        
        model_availability_msg = ""
        if preferred_model and preferred_model.lower() not in ["null", "none"]:
            # Convert to lowercase for comparison
            preferred_model_lower = preferred_model.lower()
            available_models_lower = [model.lower() for model in available_models]
            
            # Check if the preferred model is available
            if any(preferred_model_lower in model.lower() for model in available_models):
                model_availability_msg = f"✓ {preferred_model} is available for test drive at this location."
            else:
                # Find similar models that are available
                similar_models = [model for model in available_models if model.lower() != "null" and model.lower() != "none"]
                if similar_models:
                    model_availability_msg = f"Note: {preferred_model} is not available at this location, but you can test drive {', '.join(similar_models[:3])}."
                else:
                    model_availability_msg = f"Note: Please call the dealership to confirm {preferred_model} availability."
        
        # Generate booking reference
        booking_ref = f"TD-{int(time.time())}"
        
        # Format confirmation message
        confirmation_msg = f"""✅ Test drive scheduled!

{location_message}

🚗 Vehicle: {preferred_model if preferred_model and preferred_model.lower() not in ["null", "none"] else "Toyota"}
🏢 Dealership: {dealership['dealership']}
📍 Location: {dealership['location']}
⏰ Hours: {dealership.get('hours', 'Regular business hours')}
☎️ Phone: {dealership.get('phone', 'Contact dealership for details')}
🔖 Booking Reference: {booking_ref}

{model_availability_msg}

A representative will contact you soon to arrange the specific date and time for your test drive. If you have any preferences, please let them know when they call.
"""
        
        return {"answer": confirmation_msg}
    
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

def find_closest_dealership(llm, user_location, available_dealerships):
    """Find the closest dealership to the user's location using LLM"""
    try:
        logger.info(f"Finding closest dealership to {user_location}")
        
        # Create a prompt for the LLM to find the closest dealership
        dealership_info = []
        for i, d in enumerate(available_dealerships):
            dealership_info.append(f"{i+1}. {d['dealership']} - {d['location']}")
        
        dealership_list = "\n".join(dealership_info)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an assistant that helps find the closest Toyota dealership to a user's location.
            
Given a user location and a list of dealerships, determine which dealership is most likely the closest geographically. 
Use common sense geographical knowledge.

Important: Respond ONLY with the INDEX NUMBER of the closest dealership, nothing else.
If uncertain, choose the first dealership (1).
"""),
            ("human", f"""User location: {user_location}

Dealership options:
{dealership_list}

Which dealership is closest to {user_location}? Respond with ONLY the index number:""")
        ])
        
        response = llm.invoke(prompt)
        logger.info(f"LLM response for closest dealership: {response.content}")
        
        
        # Try to extract a number from the response
        match = re.search(r'\d+', response.content)
        if match:
            index = int(match.group(0)) - 1
            if 0 <= index < len(available_dealerships):
                logger.info(f"Selected dealership index: {index}")
                return available_dealerships[index]
        
        # Fallback to first dealership if no valid match
        logger.info("Falling back to first dealership")
        return available_dealerships[0]
    
    except Exception as e:
        logger.error(f"Error finding closest dealership: {e}")
        # Fallback to returning a random dealership
        random_dealership = random.choice(available_dealerships)
        logger.info(f"Falling back to random dealership: {random_dealership['dealership']}")
        return random_dealership