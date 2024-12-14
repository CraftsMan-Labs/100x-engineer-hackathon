from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from src.app.llm import LiteLLMKit
from src.app.schemas.llm import ChatRequest, Message
from src.app.pinecone_client import PineconeRAG
from src.app.config import get_settings
from dotenv import load_dotenv
from app.exa import ExaAPI
from god_prompt import GOD_PROMPT
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


class RAGCheckGodMode(BaseModel):
    rag_needed: bool
    rag_query: Optional[list[str]]


class ResponseChat(BaseModel):
    response: str
    img_bool: bool = Field(
        description="If you need to plot some graphs set true or else False"
    )
    x_labels: Optional[list[str]]
    y_labels: Optional[list[str]]
    x_values: Optional[list[float]]
    y_values: Optional[list[float]]
    title: Optional[str]
    x_axis_name: Optional[str]
    y_axis_name: Optional[str]


SYSTEM_PROMPT = """I am Market Edge Analyzer, your advanced market intelligence assistant. I specialize in providing data-driven insights across multiple domains:

1. Market Analysis: Detailed market trends, size estimations, and growth projections
2. Competitive Intelligence: In-depth competitor analysis, market positioning, and strategic advantages
3. Customer Insights: Customer behavior patterns, segmentation, and preference analysis
4. Product Strategy: Product evolution tracking, feature analysis, and market fit assessment
5. Market Opportunities: Growth opportunities, market gaps, and expansion potential

I base my responses on comprehensive market reports, real-time data, and historical trends. I can provide specific metrics, comparative analyses, and strategic recommendations. How can I assist you with your market intelligence needs today?"""

CLASSIFER_PROMPT = """Based on the convertsation you have do we need to perform a a database search to get more information? if user is asking more information from outside the conversation. generate a relevant saerch query"""

GOD_CLASSIFER_PROMPT = """Based on the convertsation you have do we need to perform a a database search to get more information? if user is asking more information from outside the conversation. generate a relevant saerch queries upto 5"""


def check_if_rag_needed(data: ChatRequest) -> RAGCheck:
    """Check if RAG is needed based on the conversation"""
    messages_ = data.model_copy(deep=True)
    messages_.messages.append(Message(role="user", content=CLASSIFER_PROMPT))
    llm = LiteLLMKit(model_name="gpt-4o", temperature=0.7)
    response = llm.generate(messages_, response_format=RAGCheck)
    print(response)
    return response


def check_if_rag_needed_god_mode(data: ChatRequest) -> RAGCheck:
    """Check if RAG is needed based on the conversation"""
    messages_ = data.model_copy(deep=True)
    messages_.messages.append(
        Message(role="user", content=GOD_PROMPT + GOD_CLASSIFER_PROMPT)
    )
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
        for query in rag_flag["rag_query"]:
            relevant_docs = pinecone_rag.query(query)

            # Add RAG context to messages
            if relevant_docs:
                rag_context = Message(
                    role="assistant",
                    content="Relevant documents:\n" + "\n".join(relevant_docs),
                )
                request.messages.insert(-1, rag_context)

                exa_res = exa.search_and_contents(query, num_results=2)
                exa_res_str = " ".join([result.text for result in exa_res.results])
                request.messages.insert(
                    -1, Message(role="assistant", content=exa_res_str)
                )

    # Generate response
    print(request)
    response = await llm.agenerate(request)

    return {"response": response}


@router.post("/god_mode")
async def chat_with_llm_in_god_mode(request: ChatRequest) -> ResponseChat:
    """
    Chat endpoint that uses LiteLLM to generate responses with optional memory and RAG

    Args:
        request: Chat request containing messages
        use_memory: Enable Mem0 memory augmentation
        use_rag: Enable Pinecone RAG document retrieval
    """
    # insert in the first
    request.messages.insert(
        0, Message(role="system", content=SYSTEM_PROMPT + GOD_PROMPT)
    )
    llm = LiteLLMKit(model_name="gpt-4o", temperature=0.7)

    # Augment context with RAG if enabled
    rag_flag = check_if_rag_needed_god_mode(request)
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
    response = await llm.agenerate(request, response_format=ResponseChat)

    return response
