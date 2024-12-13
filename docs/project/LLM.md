# LiteLLM Kit Usage Guide

## Overview
The `LiteLLMKit` provides a powerful and flexible interface for interacting with various Large Language Models (LLMs) through the LiteLLM library.

## Installation
Ensure you have the required dependencies installed:
```bash
pip install litellm python-dotenv pydantic
```

## Supported Models
- Qwen 2.5
- Claude Haiku 3.5
- Claude Sonnet 3.5
- GPT-4o
- GPT-4o Mini
- DeepSeek

## Initialization

### Basic Initialization
```python
from app.llm import LiteLLMKit
from app.schemas.llm import ChatRequest, Message

# Initialize with default parameters
llm = LiteLLMKit(model_name="gpt-4o")
```

### Customized Initialization
```python
# Customize temperature and max tokens
llm = LiteLLMKit(
    model_name="claude-sonnet-3.5", 
    temperature=0.5, 
    max_tokens=2048
)
```

## Synchronous Generation
Generate responses using the synchronous method:

```python
# Prepare messages
messages = [
    Message(role="system", content="You are a helpful assistant."),
    Message(role="user", content="Explain quantum computing.")
]

# Create chat request
request = ChatRequest(messages=messages)

# Generate response
response = llm.generate(request)
print(response)
```

## Asynchronous Generation
Use async method for non-blocking calls:

```python
import asyncio

async def main():
    messages = [
        Message(role="system", content="You are a coding expert."),
        Message(role="user", content="Write a Python function to reverse a string.")
    ]
    request = ChatRequest(messages=messages)
    
    # Async generation
    response = await llm.agenerate(request)
    print(response)

asyncio.run(main())
```

## Structured Response Generation
Generate responses in a specific format:

```python
from pydantic import BaseModel

# Define a custom response model
class CodeResponse(BaseModel):
    language: str
    code: str
    explanation: str

# Generate structured response
messages = [
    Message(role="user", content="Create a Python function to calculate factorial")
]
request = ChatRequest(messages=messages)

# Generate with structured response
structured_response = llm.generate(
    request, 
    response_format=CodeResponse
)
```

## Error Handling
```python
try:
    response = llm.generate(request)
except Exception as e:
    print(f"Generation failed: {e}")
```

## Best Practices
- Always use environment variables for API keys
- Handle rate limits and potential errors
- Choose appropriate model based on task complexity
- Adjust temperature for creativity vs. precision

## Model Selection Tips
- Low temperature (0.1-0.3): Precise, deterministic responses
- Medium temperature (0.5-0.7): Balanced creativity
- High temperature (0.8-1.0): More creative, less predictable responses

## Supported Providers
- OpenAI
- Anthropic
- Hugging Face
- DeepSeek

## Logging and Monitoring
Configure logging to track LLM interactions and performance.
```
