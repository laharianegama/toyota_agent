from pydantic import BaseModel
from typing import Literal


class RouteResponse(BaseModel):
    content: Literal[
        "VehicleCheck",
        "ServiceBooking",
        "TestDrive",
        "NoContext"
    ]