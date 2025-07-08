from pydantic import BaseModel, EmailStr, ValidationError, Field
from typing import Optional

class data_validation(BaseModel):
   try:
      message_text: str = Field(min_length=20, max_length=399)
      sender_username: str = Field(min_length=5, max_length=30)
   except ValidationError as err:
      print(repr(err.errors()[0]['type']))

