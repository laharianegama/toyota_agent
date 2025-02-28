from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from orchestration.logger import setup_logger

logger = setup_logger(__name__)

test_drive_prompt = """You are a Toyota test drive scheduling assistant.
Extract test drive requirements from the user's request.

User request: {question}

Return ONLY a JSON with these fields:
{
    "preferred_model": "<vehicle model>",
    "preferred_date": "<date if mentioned, else null>",
    "preferred_time": "<time if mentioned, else null>",
    "preferred_location": "<location if mentioned, else null>"
}
"""

def get_test_drive_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", test_drive_prompt),
        ("human", "{question}")
    ])