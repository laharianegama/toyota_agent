from orchestration.logger import setup_logger
from orchestration.state import MultiAgentState

logger = setup_logger(__name__)

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from orchestration.state import MultiAgentState
from orchestration.logger import setup_logger
import re

logger = setup_logger(__name__)

def no_context_node(llm, state: MultiAgentState):
    """
    Handle queries that don't fit into specific workflows using the LLM
    for more natural, helpful responses.
    """
    try:
        logger.info("Processing no context node with LLM")
        
        question = state.get('question', '').strip()
        logger.info(f"No context question: {question}")
        
        # Check for slot selection pattern
        slot_pattern = r'(?:slot\s*)?(\d+)'
        if re.search(slot_pattern, question.lower()):
            return {
                "answer": "It looks like you're trying to select a slot number. Please first use our service booking feature by asking about service appointments or maintenance, and then you'll be able to select from the available slots."
            }
        
        # Use the LLM to generate a more natural response
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Toyota assistant that helps customers with their Toyota-related queries. The user's query doesn't fit into your specific service workflows (vehicle availability check, service appointment booking, or test drive scheduling), but you should still be helpful and friendly.

                    Provide a thoughtful response that:
                    1. Acknowledges their question
                    2. Offers general information about Toyota if relevant
                    3. Guides them toward one of your core services if appropriate
                    4. Maintains a positive, helpful tone

                    Your response should be concise (2-3 sentences maximum) and conversational. Don't apologize for not understanding - just be helpful.

                    The three main services you can help with are:
                    - Vehicle availability checks (inventory inquiries)
                    - Service appointment booking (maintenance and repairs)
                    - Test drive scheduling

                    Also tell them to ask these services if they need help with them.

                    If the question is completely unrelated to Toyota or automobiles, gently guide the conversation back to how you can help with Toyota-related matters.
                    """),
            ("human", "{question}")
        ])
        
        # Invoke the LLM with the prompt
        response = llm.invoke(prompt.format(question=question))
        
        # Return the LLM's response
        return {"answer": response.content}
            
    except Exception as e:
        logger.error(f"Error in no_context_node_with_llm: {e}")
        return {"answer": "I appreciate your question. While I'm specialized in Toyota vehicle availability, service appointments, and test drives, I'd be happy to help with any Toyota-related inquiry you might have."}