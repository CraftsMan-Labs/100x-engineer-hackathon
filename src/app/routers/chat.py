from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional
from src.app.llm import LiteLLMKit
from src.app.schemas.llm import ChatRequest, Message
from src.app.pinecone_client import PineconeRAG
from src.app.config import get_settings
from dotenv import load_dotenv
from app.exa import ExaAPI
import os

load_dotenv()

exa = ExaAPI(os.getenv("EXA_API_KEY"))

router = APIRouter(prefix="/chat", tags=["chat"])

settings = get_settings()

# Initialize RAG client
pinecone_rag = PineconeRAG()


class RAGCheck(BaseModel):
    rag_needed: bool
    rag_query: Optional[str]


SYSTEM_PROMPT = """I am Market Edge Analyzer, your advanced market intelligence assistant. I specialize in providing data-driven insights across multiple domains:

1. Market Analysis: Detailed market trends, size estimations, and growth projections
2. Competitive Intelligence: In-depth competitor analysis, market positioning, and strategic advantages
3. Customer Insights: Customer behavior patterns, segmentation, and preference analysis
4. Product Strategy: Product evolution tracking, feature analysis, and market fit assessment
5. Market Opportunities: Growth opportunities, market gaps, and expansion potential

I base my responses on comprehensive market reports, real-time data, and historical trends. I can provide specific metrics, comparative analyses, and strategic recommendations. How can I assist you with your market intelligence needs today?"""

CLASSIFER_PROMPT = """Based on the convertsation you have do we need to perform a a database search to get more information? if user is asking more information from outside the conversation"""


def check_if_rag_needed(data: ChatRequest) -> RAGCheck:
    """Check if RAG is needed based on the conversation"""
    messages_ = data.model_copy(deep=True)
    messages_.messages.append(Message(role="user", content=CLASSIFER_PROMPT))
    llm = LiteLLMKit(model_name="gpt-4o", temperature=0.7)
    response = llm.generate(messages_, response_format=RAGCheck)
    print(response)
    return response


@router.post("/")
async def chat_with_llm(request: ChatRequest):
    """
    Chat endpoint that uses LiteLLM to generate responses with optional memory and RAG

    Args:
        request: Chat request containing messages
        use_memory: Enable Mem0 memory augmentation
        use_rag: Enable Pinecone RAG document retrieval
    """
    # insert in the first
    request.messages.insert(0, Message(role="system", content=SYSTEM_PROMPT))
    llm = LiteLLMKit(model_name="gpt-4o", temperature=0.7)

    # Augment context with RAG if enabled
    rag_flag = check_if_rag_needed(request)
    if rag_flag["rag_needed"]:
        relevant_docs = pinecone_rag.query(rag_flag["rag_query"])

        # Add RAG context to messages
        if relevant_docs:
            rag_context = Message(
                role="assistant",
                content="Relevant documents:\n" + "\n".join(relevant_docs),
            )
            request.messages.insert(-1, rag_context)

            exa_res = exa.search_and_contents(rag_flag["rag_query"], num_results=2)
            exa_res_str = " ".join([result.text for result in exa_res.results])
            request.messages.insert(-1, Message(role="assistant", content=exa_res_str))

    # Generate response
    print(request)
    response = await llm.agenerate(request)

    return {"response": response}
