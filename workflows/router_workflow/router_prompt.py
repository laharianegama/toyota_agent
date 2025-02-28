from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from orchestration.logger import setup_logger
logger = setup_logger(__name__)

system_router_prompt = (
    """You are an AI router agent responsible for classifying incoming questions. Based on your classification, the question will be routed to the appropriate team.
        -if the question is about **vehicle availability, inventory, stock, or model**, it should be routed to the VehicleCheck team.
        -if the question is about **service, maintenance, or repair**, it should be routed to the ServiceBooking team.
        -if the question is about **test drive, try, or drive**, it should be routed to the TestDrive team.
        - NoContext: For questions that do not fit into any of the above categories.

        Your output should be **only** one of the words: VehicleCheck, ServiceBooking , TestDrive or NoContext. 
        Do not include any other text. 

    """
)

members = [
    "VehicleCheck",
    "ServiceBooking",   
    "TestDrive",
    "NoContext",
]

options = [] + members


def get_router_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_router_prompt),
            MessagesPlaceholder(variable_name="question"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Or should we FINISH? Select one of: {options}",
            ),
        ]
    ).partial(options=str(options), members=", ".join(members))
    return prompt

