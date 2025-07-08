from pydantic import BaseModel, EmailStr, ValidationError, Field
from typing import Optional

class validate_send_msg(BaseModel):
   message_text: str = Field(min_length=20, max_length=399)
   sender_username: str = Field(min_length=5, max_length=30)

class validate_del_msg(BaseModel):
   id: int
