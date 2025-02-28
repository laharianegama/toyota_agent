from langchain_core.messages import HumanMessage
from orchestration.logger import setup_logger
from orchestration.state import MultiAgentState
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
import json
import re

logger = setup_logger(__name__)

def check_vehicle_availability(llm, state: MultiAgentState):
    try:
        logger.info("Processing vehicle check node")
        
        # Extract model information from the question
        question = state.get('question', '')
        model_mentioned = extract_vehicle_model(question)
        
        # Generate inventory with bias toward mentioned model
        inventory_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI inventory manager for Toyota. 
            Generate a dataset of 10 Toyota vehicle inventories.
            
            The customer is asking about: {model_mentioned}
            
            Include at least 2-3 of the specifically mentioned model (if any) in the inventory.
            
            For each vehicle, include:
            - model: Toyota model name
            - year: between 2020-2024
            - color: realistic color name
            - trim: appropriate trim level for the model
            - price: realistic price in USD (no $ symbol, just the number)
            - available: boolean (true/false)
            
            Format as a valid JSON array. Do not include explanatory text."""),
            ("human", "Generate a realistic Toyota vehicle inventory.")
        ])
        
        inventory_response = llm.invoke(inventory_prompt.format(
            model_mentioned=model_mentioned if model_mentioned else "general Toyota vehicles"
        ))
        
        # Parse the inventory
        try:
            # Try to extract JSON array
            json_match = re.search(r'\[.*\]', inventory_response.content, re.DOTALL)
            if json_match:
                inventory = json.loads(json_match.group())
            else:
                inventory = json.loads(inventory_response.content)
        except json.JSONDecodeError:
            # Fallback inventory if parsing fails
            inventory = generate_fallback_inventory(model_mentioned)
        
        # Create a prompt to answer the specific vehicle availability query
        availability_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful Toyota sales assistant. 
            A customer is asking about vehicle availability.
            
            Use this inventory data to respond to their query:
            {inventory}
            
            Guidelines:
            1. Be conversational and friendly, like a real sales associate
            2. Provide specific details (model, year, color, price) from the inventory
            3. If they ask about a specific model, focus on that model
            4. Mention if a model is available or not in stock
            5. If a model isn't available, suggest similar alternatives from the inventory
            6. Keep your response fairly brief (2-4 sentences)
            7. End by asking if they would like more information or to see the vehicle
            8. Always return a string response formatted correctly, not JSON or other formats"""),
            ("human", "{question}")
        ])
        
        # Get the availability response
        availability_response = llm.invoke(availability_prompt.format(
            inventory=json.dumps(inventory, indent=2),
            question=question
        ))
        
        # Return the response with context for conversation continuity
        return {
            "answer": availability_response.content
        }
    
    except Exception as e:
        logger.error(f"Error in vehicle availability check: {e}")
        return {"answer": "An error occurred while checking vehicle availability."}

def extract_vehicle_model(question):
    """Extract Toyota model from the question"""
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

def generate_fallback_inventory(model_mentioned):
    """Generate a fallback inventory if JSON parsing fails"""
    base_inventory = [
        {"model": "Camry", "year": 2022, "color": "Black", "trim": "LE", "price": 26420, "available": True},
        {"model": "Corolla", "year": 2023, "color": "Silver", "trim": "SE", "price": 23475, "available": True},
        {"model": "RAV4", "year": 2022, "color": "Blue", "trim": "XLE", "price": 28475, "available": True},
        {"model": "Highlander", "year": 2023, "color": "White", "trim": "Limited", "price": 42420, "available": False},
        {"model": "Tacoma", "year": 2022, "color": "Red", "trim": "TRD", "price": 37250, "available": True}
    ]
    
    # If a specific model was mentioned, add it to inventory
    if model_mentioned and not any(item["model"].lower() == model_mentioned.lower() for item in base_inventory):
        base_inventory.append({
            "model": model_mentioned,
            "year": 2023,
            "color": "Silver",
            "trim": "SE",
            "price": 30000,
            "available": True
        })
    
    return base_inventory