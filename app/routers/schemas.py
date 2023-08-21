from pydantic import BaseModel

class ChatMessageSchema(BaseModel):
    message: str
    timestamp: str
    username: str

class CreateMessageInput(BaseModel):
    message: str