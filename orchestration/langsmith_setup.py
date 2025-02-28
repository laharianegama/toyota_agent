import os
from dotenv import load_dotenv
from langchain_core.tracers import LangChainTracer
from langsmith import Client
from langchain_core.callbacks.manager import CallbackManager

# Load environment variables
load_dotenv()

def setup_langsmith():
    """
    Setup LangSmith tracing and return a callback manager
    
    Returns:
        callback_manager: A CallbackManager with LangSmith tracer
    """
    # Check for LangSmith environment variables
    api_key = os.getenv("LANGCHAIN_API_KEY")
    api_url = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    project_name = os.getenv("LANGCHAIN_PROJECT", "toyota-assistant")
    
    if not api_key:
        print("Warning: LANGCHAIN_API_KEY not found in environment variables. LangSmith tracing will not be enabled.")
        return None
    
    try:
        # Create LangSmith client
        client = Client(api_key=api_key, api_url=api_url)
        
        # Create a tracer
        tracer = LangChainTracer(project_name=project_name)
        
        # Create a callback manager with the tracer
        callback_manager = CallbackManager([tracer])
        
        print(f"LangSmith tracing enabled for project: {project_name}")
        return callback_manager
    except Exception as e:
        print(f"Error setting up LangSmith: {e}")
        return None