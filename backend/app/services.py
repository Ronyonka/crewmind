from datetime import datetime
from typing import List, Optional
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase

from .models import StoredQuestion, QuestionRequest, QuestionResponse
from .database import get_database

logger = logging.getLogger(__name__)


class QuestionService:
    """Service class for handling question operations."""

    def __init__(self):
        self.collection_name = "questions"

    async def store_question(self, question_request: QuestionRequest) -> StoredQuestion:
        """Store a question and its response in the database."""
        try:
            db = await get_database()
            collection = db[self.collection_name]

            # Create document
            question_doc = {
                "question": question_request.question,
                "response": self._generate_response(question_request.question),
                "timestamp": datetime.utcnow(),
            }

            # Insert into database
            result = await collection.insert_one(question_doc)

            # Add the inserted_id to the document
            question_doc["_id"] = str(result.inserted_id)

            # Return the stored question (unpack only once)
            return StoredQuestion(**question_doc)

        except Exception as e:
            logger.error(f"Error storing question: {e}")
            raise

    async def get_conversation_history(self, page: int = 1, per_page: int = 10) -> dict:
        """Retrieve conversation history with pagination."""
        try:
            db = await get_database()
            collection = db[self.collection_name]

            # Calculate skip value for pagination
            skip = (page - 1) * per_page
            total_count = await collection.count_documents({})

            # Get questions with pagination
            cursor = (
                collection.find({}).sort("timestamp", -1).skip(skip).limit(per_page)
            )
            questions = await cursor.to_list(length=per_page)

            # Convert MongoDB documents to dict format, handling ObjectId
            stored_questions = []
            for q in questions:
                q["_id"] = str(q["_id"])  # Convert ObjectId to string
                stored_questions.append(StoredQuestion(**q))

            return {
                "questions": stored_questions,
                "total_count": total_count,
                "page": page,
                "per_page": per_page,
                "total_pages": (total_count + per_page - 1) // per_page,
            }

        except Exception as e:
            logger.error(f"Error retrieving conversation history: {e}")
            raise

    async def get_question_by_id(self, question_id: str) -> Optional[StoredQuestion]:
        """Retrieve a specific question by ID."""
        try:
            from bson import ObjectId

            db = await get_database()
            collection = db[self.collection_name]

            question = await collection.find_one({"_id": ObjectId(question_id)})

            if question:
                return StoredQuestion(**question)
            return None

        except Exception as e:
            logger.error(f"Error retrieving question by ID {question_id}: {e}")
            raise

    def _generate_response(self, question: str) -> str:
        """Generate a response to the question. This is a placeholder for now."""
        # Basic response logic - could be enhanced with AI/LLM integration
        responses = [
            "Thanks for your question, I'll think about it.",
            "That's an interesting question! Let me consider that for you.",
            "I appreciate your question. I'll give it some thought.",
            "Thanks for asking! I'll process that information.",
            "Great question! I'll analyze that for you.",
        ]

        # Simple logic based on question length or content
        if len(question) > 100:
            return "That's quite a detailed question! Thanks for your question, I'll think about it carefully."
        elif "?" in question:
            return "Thanks for your question, I'll think about it."
        else:
            return "I've received your message. Thanks for your question, I'll think about it."


# Create service instance
question_service = QuestionService()
