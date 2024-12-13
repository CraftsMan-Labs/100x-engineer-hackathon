from typing import List, Optional, Dict
from mem0 import Memory
import os

# Global variables
USER_ID = "rishub"  # Hardcoded user ID as specified
memory = None


def initialize_memory() -> Memory:
    """
    Initialize Mem0 memory system

    Returns:
        Memory instance configured with Neo4j
    """
    global memory

    # Initialize graph memory configuration
    config = {
        "graph_store": {
            "provider": "neo4j",
            "config": {
                "url": os.getenv("NEO_4J_URL"),
                "username": os.getenv("NEO_4J_USERNAME"),
                "password": os.getenv("NEO_4J_PASSWORD"),
            },
        },
        "version": "v1.1",
    }
    memory = Memory()
    return memory


def add_memory(text: str) -> Dict:
    """
    Add a new memory

    Args:
        text: Text content to store as memory

    Returns:
        Dict containing operation result
    """
    global memory
    if memory is None:
        memory = initialize_memory()
    return memory.add(text, user_id=USER_ID)


def update_memory(memory_id: str, text: str) -> Dict:
    """
    Update an existing memory

    Args:
        memory_id: ID of memory to update
        text: New text content

    Returns:
        Dict containing operation result
    """
    global memory
    if memory is None:
        memory = initialize_memory()
    return memory.update(memory_id=memory_id, data=text)


def search_memories(query: str) -> List[str]:
    """
    Search memories based on query

    Args:
        query: Search query string

    Returns:
        List of relevant memory texts
    """
    global memory
    if memory is None:
        memory = initialize_memory()
    return memory.search(query=query, user_id=USER_ID)


def get_all_memories() -> Dict:
    """
    Get all stored memories

    Returns:
        Dict containing all memories
    """
    global memory
    if memory is None:
        memory = initialize_memory()
    return memory.get_all()


def get_memory_history(memory_id: str) -> Dict:
    """
    Get history of changes for a specific memory

    Args:
        memory_id: ID of memory to get history for

    Returns:
        Dict containing memory change history
    """
    global memory
    if memory is None:
        memory = initialize_memory()
    return memory.history(memory_id=memory_id)
