from langchain_cerebras import ChatCerebras
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_fireworks import ChatFireworks
from orchestration.logger import setup_logger
from langchain_groq import ChatGroq
import os

logger = setup_logger(__name__)


#different opensource LLMs to use, incase you want to change the LLM, or the inference engine
#change the LLM_TO_USE environment variable to the following values: nvidia, fireworks, groq, cerebras

llm_to_use = os.getenv('LLM_TO_USE', 'groq')
class LLMManager:
    def __init__(self,callbacks=None):
        try:
            logger.info("Initializing LLMManager")
            
             # Store callbacks
            self.callbacks = callbacks

            # Initialize models with callbacks if available
            if self.callbacks:
                self.llm_for_router  = ChatGroq(
                    model="llama-3.3-70b-versatile",
                    temperature=0.0,
                    max_retries=2,
                    callbacks=self.callbacks
                )
            else:
                self.llm_for_router  = ChatGroq(
                    model="llama-3.3-70b-versatile",
                    temperature=0.0,
                    max_retries=2,
                )
                
            if llm_to_use == 'nvidia':
                self.llm = ChatNVIDIA(
                    model="meta/llama3-70b-instruct", temperature=0)
                
            elif llm_to_use == 'fireworks':
                self.llm = ChatFireworks(
                    model="accounts/fireworks/models/llama-v3p1-70b-instruct",
                    temperature=0,
                    max_tokens=None,
                    timeout=None,
                    max_retries=2,
                )
                
            elif (llm_to_use == 'groq'):
                self.llm = ChatGroq(
                    model="llama-3.3-70b-versatile",
                    temperature=0.0,
                    max_retries=2,
                )
            elif (llm_to_use == "cerebras"):
                self.llm = ChatCerebras(
                    model="llama3.1-70b",
                    temperature=0.0,
                    max_retries=2,
                )
            logger.info("LLMManager initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing LLMManager: {e}")
            raise

    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        try:
            logger.info(f"Invoking LLM with prompt: {prompt}")
            messages = prompt.format_messages(**kwargs)
            response = self.llm.invoke(messages)
            logger.info(f"LLM response: {response.content}")
            return response.content
        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            raise
