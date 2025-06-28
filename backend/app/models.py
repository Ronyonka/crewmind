from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId class for Pydantic."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class QuestionRequest(BaseModel):
    """Model for incoming question requests."""

    question: str = Field(
        ..., min_length=1, max_length=1000, description="The user's question"
    )


class QuestionResponse(BaseModel):
    """Model for question responses."""

    response: str = Field(..., description="The assistant's response")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Response timestamp"
    )


class StoredQuestion(BaseModel):
    """Model for questions stored in database."""

    question: str = Field(..., description="The user's question")
    response: str = Field(..., description="The assistant's response")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Question timestamp"
    )

    class Config:
        json_encoders = {datetime: str}  # Handle datetime serialization
        extra = "allow"  # Allow extra fields (like _id) without validation


class ConversationHistory(BaseModel):
    """Model for conversation history response."""

    questions: list[StoredQuestion] = Field(
        default=[], description="List of stored questions and responses"
    )
    total_count: int = Field(..., description="Total number of questions")
    page: int = Field(default=1, description="Current page number")
    per_page: int = Field(default=10, description="Questions per page")
