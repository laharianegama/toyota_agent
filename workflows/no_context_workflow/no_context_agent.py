from orchestration.logger import setup_logger
from orchestration.state import MultiAgentState

logger = setup_logger(__name__)

def no_context_node(state: MultiAgentState):
    logger.info("Processing no context node")
    return {"answer": "I'm sorry, I don't understand the question. Please provide more context or rephrase your question."}