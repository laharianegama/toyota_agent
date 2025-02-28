from datetime import datetime, timezone
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from orchestration.logger import setup_logger
import json  # Import json to properly load the inventory data

logger = setup_logger(__name__)

# Inventory Data (ensure it's properly formatted)
data = [
    {"Brand": "Toyota", "Model": "Camry", "Year": "2018"},
    {"Brand": "Toyota", "Model": "Corolla", "Year": "2017"},
    {"Brand": "Toyota", "Model": "RAV4", "Year": "2020"},
    {"Brand": "Toyota", "Model": "Highlander", "Year": "2021"},
    {"Brand": "Toyota", "Model": "Tacoma", "Year": "2019"},
    {"Brand": "Toyota", "Model": "Tundra", "Year": "2021"},
    {"Brand": "Toyota", "Model": "Prius", "Year": "2016"},
    {"Brand": "Toyota", "Model": "Avalon", "Year": "2022"},
    {"Brand": "Toyota", "Model": "4Runner", "Year": "2023"},
    {"Brand": "Toyota", "Model": "Sienna", "Year": "2015"}
]

# Convert data to a JSON string
data_str = json.dumps(data, indent=2)

availability_prompt = (
    """You are an AI agent responsible for checking the availability of a vehicle in the inventory. 
    Your task is to take the user's request and check the availability of the vehicle.

    The inventory data is as follows:
    {data}

    ### Fields Description
    - `Brand` (String): The brand of the vehicle.
    - `Model` (String): The model of the vehicle.
    - `Year` (Integer): The year of the vehicle.

    The user's request is: {question}
    
    If the Model is available in the inventory, respond with "Vehicle is available".
    If the Model is not available in the inventory, respond with "Vehicle is not available in the inventory".
    """
)

def get_availabilty_prompt():
    """Returns a properly formatted ChatPromptTemplate with inventory data."""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", availability_prompt),  # Pass formatted data
            ("human", "{question}"),
        ]
    ).partial(data=data_str)
    
    return prompt
