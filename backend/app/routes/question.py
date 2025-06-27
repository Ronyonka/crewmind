from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging

from ..models import QuestionRequest, QuestionResponse, ConversationHistory
from ..services import question_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(payload: QuestionRequest):
    """
    Submit a question to the assistant.

    - **question**: The user's question (required, 1-1000 characters)

    Returns the assistant's response along with a timestamp.
    """
    try:
        logger.info(f"Received question: {payload.question[:100]}...")

        # Store the question and get response
        stored_question = await question_service.store_question(payload)

        # Return the response
        return QuestionResponse(
            response=stored_question.response, timestamp=stored_question.timestamp
        )

    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while processing question"
        )


@router.get("/history", response_model=ConversationHistory)
async def get_conversation_history(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    per_page: int = Query(
        10, ge=1, le=100, description="Number of questions per page (max 100)"
    ),
):
    """
    Retrieve conversation history with pagination.

    - **page**: Page number (default: 1)
    - **per_page**: Number of questions per page (default: 10, max: 100)

    Returns a list of previous questions and responses, sorted by newest first.
    """
    try:
        logger.info(
            f"Retrieving conversation history - page: {page}, per_page: {per_page}"
        )

        history = await question_service.get_conversation_history(page, per_page)

        return ConversationHistory(**history)

    except Exception as e:
        logger.error(f"Error retrieving conversation history: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while retrieving history"
        )


@router.get("/question/{question_id}")
async def get_question_by_id(question_id: str):
    """
    Retrieve a specific question by its ID.

    - **question_id**: The MongoDB ObjectId of the question

    Returns the question and response details.
    """
    try:
        logger.info(f"Retrieving question by ID: {question_id}")

        question = await question_service.get_question_by_id(question_id)

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        return question

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving question by ID: {e}")
        raise HTTPException(
            status_code=500, detail="Internal server error while retrieving question"
        )
