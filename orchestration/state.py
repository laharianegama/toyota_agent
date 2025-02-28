from typing import List, Any, Annotated, Dict, Optional, Sequence
from typing_extensions import TypedDict
from langgraph.prebuilt.chat_agent_executor import AgentState
from dataclasses import dataclass, field


class MultiAgentState(AgentState):
    messages: Sequence[Any] = field(default_factory=list)
    question: str = ""
    question_type: str = ""
    answer: str = ""
    available_slots: Optional[List[Dict[str, Any]]] = None
    available_dealerships: Optional[List[Dict[str, Any]]] = None
    
    context: str = "None"
    
    # We can have these fields for future extensibility
    # booking_messages: Sequence[Any] = field(default_factory=list)
    # test_messages: Sequence[Any] = field(default_factory=list)
    


