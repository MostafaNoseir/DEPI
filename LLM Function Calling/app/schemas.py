# app/schemas.py

from pydantic import BaseModel
from typing import Literal


class TicketUpdate(BaseModel):
    """
    Schema for updating tickets.
    
    Literal acts as an ENUM:
    - Only these values are allowed
    - Anything else fails validation
    """

    ticket_id: str
    status: Literal["open", "pending", "closed"]