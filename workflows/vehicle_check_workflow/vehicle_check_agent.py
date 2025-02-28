from langchain_core.messages import HumanMessage
from orchestration.logger import setup_logger
from orchestration.state import MultiAgentState
from workflows.vehicle_check_workflow.availability_prompt import get_availabilty_prompt
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
import json

logger = setup_logger(__name__)

def check_vehicle_availability(llm, state: MultiAgentState):
    # try:
    #     logger.info("Processing vehicle check node")
    #     supervisor_chain = get_availabilty_prompt() | llm
    #     messages = state['messages']
    #     human_msg = HumanMessage(content=state['question'])
    #     messages = messages + [human_msg]
    #     response = supervisor_chain.invoke({"question": state['question']})
    #     return {"answer": response.content} if response.content else {"answer": "No vehicles found"}
    # except KeyError as e:
    #     logger.error(f"Missing key in state: {e}")
    #     raise
    # except Exception as e:
    #     logger.error(f"Error in check_vehicle_availability: {e}")
    #     raise
    
    
    try:
        logger.info("Processing vehicle check node")
        
        # Prompt to generate vehicle inventory
        inventory_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI inventory manager for Toyota. 
            Generate a comprehensive and realistic dataset of 10 vehicle inventories.

            Generate a JSON array with these vehicle details:
            - Model (Toyota models only)
            - Year (2020-2024)
            - Color
            - Availability status

            Respond ONLY with a valid JSON array. Do not include any additional text."""),
            ("human", "Generate a detailed Toyota vehicle inventory dataset of 10 vehicles.")
        ])

        # Create chain to generate inventory
        inventory_chain = inventory_prompt | llm
        
        # Generate inventory
        inventory_response = inventory_chain.invoke({})
        
        # Parse the inventory
        try:
            # Attempt to parse the entire response content as JSON
            inventory = json.loads(inventory_response.content)
        except json.JSONDecodeError:
            # Fallback: extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', inventory_response.content, re.DOTALL)
            if json_match:
                inventory = json.loads(json_match.group())
            else:
                return {"answer": "Sorry, could not generate vehicle inventory."}

        # Extract the specific query details
        question = state['question'].lower()
        
        # Create a prompt to answer the specific vehicle availability query
        availability_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Toyota sales assistant. 
            Use the following vehicle inventory to answer the customer's query:
            
            Inventory: {inventory}
            
            Answer the following question about vehicle availability, 
            providing specific details from the inventory. 
            If the exact model isn't available, suggest alternatives."""),
            ("human", "{question}")
        ])

        # Create chain to answer query
        availability_chain = availability_prompt | llm
        
        # Get the availability response
        availability_response = availability_chain.invoke({
            "inventory": json.dumps(inventory),
            "question": state['question']
        })

        # Return the response
        return {"answer": availability_response.content}

    except Exception as e:
        logger.error(f"Error in vehicle availability check: {e}")
        return {"answer": "An error occurred while checking vehicle availability."}