# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from orchestration.logger import setup_logger
# logger = setup_logger(__name__)


# service_booking_prompt = """You are an AI assistant that helps customers book a Toyota service appointment.

# ### Instructions:
# - Identify if the user has mentioned a **specific service type** (e.g., oil change, tire service, repair).
# - Identify if the user has mentioned a **preferred date, time, or location**.
# - Acknowledge their request by confirming what they have mentioned.
# - **Regardless of the details provided, always tell them they need to select one of the available slots**.
# - **Your response must be a plain string**—do not use JSON or backticks.
# - Keep your response **short and to the point**.

# ### User request:
# {question}

# ### Response Format:
# "Okay, for your requested service {service_type if mentioned else 'appointment'}, please select one of the available slots."
# """

# def get_service_booking_prompt():
#     return ChatPromptTemplate.from_messages([
#         ("system", service_booking_prompt),
#         ("human", "{question}"),
#     ])


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from orchestration.logger import setup_logger
logger = setup_logger(__name__)

# Main service booking prompt
service_booking_prompt = """You are an AI assistant that helps customers book a Toyota service appointment.

### Instructions:
- Identify if the user has mentioned a **specific service type** (e.g., oil change, tire service, repair).
- Identify if the user has mentioned a **preferred date, time, or location**.
- Be helpful and concise in your responses.
- **Your response must be a plain string**—do not use JSON or backticks.

### User request:
{question}

### Available Slots:
{available_slots}

### Response Format:
If the user is mentioning a service type or requesting an appointment:
"Here are the available service slots for your [service type] appointment. Please select a slot by replying with the slot number."
"""

# Slot selection prompt
slot_selection_prompt = """The user is selecting a service slot. Extract the slot number from their message.

### User message:
{user_message}

### Extract the slot number (just return the number):
"""

# Confirmation prompt
confirmation_prompt = """The user has selected slot #{slot_number}. Format a confirmation message with the details.

### Slot details:
Date: {date}
Time: {time}
Location: {location}
Service Type: {service_type}
Duration: {duration} minutes

### Booking reference:
{booking_ref}

### Format a friendly confirmation message:
"""

def get_service_booking_prompt():
    """Return the main service booking prompt"""
    return ChatPromptTemplate.from_messages([
        ("system", service_booking_prompt),
        ("human", "{question}"),
    ])

def get_slot_selection_prompt():
    """Return the slot selection prompt"""
    return ChatPromptTemplate.from_messages([
        ("system", slot_selection_prompt),
        ("human", "{user_message}"),
    ])

def get_confirmation_prompt():
    """Return the confirmation prompt"""
    return ChatPromptTemplate.from_messages([
        ("system", confirmation_prompt),
        ("human", "Generate a confirmation message for slot #{slot_number}"),
    ])