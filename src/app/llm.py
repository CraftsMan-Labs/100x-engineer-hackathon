from typing import List, Optional
from litellm import completion, acompletion
from pydantic import BaseModel
from dotenv import load_dotenv
import json
from typing import Any
from src.app.schemas.llm import (
    ModelProvider,
    Message,
    ChatRequest,
    ModelConfig,
    APIKeyManager,
)
from typing import Type

# Load environment variables at module level
load_dotenv()


class CompletionHandler:
    """Handles completion requests to language models"""

    NUM_RETRIES = 2

    @staticmethod
    async def agenerate(
        model_config: ModelConfig,
        messages: List[Message],
        api_key: str,
        response_format: Optional[BaseModel] = None,
    ) -> Any:
        """Generate async completion"""
        try:
            completion_args = {
                "model": model_config.name,
                "messages": [msg.model_dump() for msg in messages],
                "temperature": model_config.temperature,
                "max_tokens": model_config.max_tokens,
                "api_key": api_key,
                "num_retries": CompletionHandler.NUM_RETRIES,
            }

            if response_format:
                completion_args["response_format"] = response_format

            response = await acompletion(**completion_args)

            if response_format:
                return json.loads(
                    response.model_dump()["choices"][0]["message"]["content"]
                )
            return response.model_dump()["choices"][0]["message"]["content"]

        except Exception as e:
            raise Exception(f"Async completion failed: {str(e)}")

    @staticmethod
    def generate(
        model_config: ModelConfig,
        messages: List[Message],
        api_key: str,
        response_format: Optional[Type[BaseModel]] = None,
    ) -> Any:
        """Generate sync completion"""
        try:
            completion_args = {
                "model": model_config.name,
                "messages": [msg.model_dump() for msg in messages],
                "temperature": model_config.temperature,
                "max_tokens": model_config.max_tokens,
                "api_key": api_key,
                "num_retries": CompletionHandler.NUM_RETRIES,
            }

            if response_format:
                completion_args["response_format"] = response_format

            response = completion(**completion_args)

            if response_format:
                return json.loads(
                    response.model_dump()["choices"][0]["message"]["content"]
                )
            return response.model_dump()["choices"][0]["message"]["content"]

        except Exception as e:
            raise Exception(f"Sync completion failed: {str(e)}")


class LiteLLMKit:
    """Enhanced LiteLLM client with better organization and error handling"""

    # Model mappings with their configurations
    MODELS = {
        "qwen-2.5": ModelConfig(
            name="Qwen/Qwen2.5-32B-Instruct", provider=ModelProvider.HUGGINGFACE
        ),
        "claude-haiku-3.5": ModelConfig(
            name="claude-haiku-3.5", provider=ModelProvider.ANTHROPIC
        ),
        "claude-sonnet-3.5": ModelConfig(
            name="claude-sonnet-3.5", provider=ModelProvider.ANTHROPIC
        ),
        "gpt-4o": ModelConfig(name="gpt-4o", provider=ModelProvider.OPENAI),
        "gpt-4o-mini": ModelConfig(name="gpt-4o-mini", provider=ModelProvider.OPENAI),
        "deepseek": ModelConfig(
            name="deepseek/deepseek-chat", provider=ModelProvider.DEEPSEEK
        ),
        "gemini-1.5-flash": ModelConfig(
            name="gemini/gemini-1.5-flash", provider=ModelProvider.GOOGLE
        ),
    }

    def __init__(
        self,
        model_name: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False,
    ):
        """Initialize the enhanced LiteLLM client"""
        if model_name not in self.MODELS:
            raise ValueError(
                f"Unsupported model: {model_name}. Available models: {list(self.MODELS.keys())}"
            )

        self.model_config = self.MODELS[model_name]
        self.model_config.temperature = temperature
        self.model_config.max_tokens = max_tokens
        self.model_config.stream = stream

        self.api_key_manager = APIKeyManager()
        self.completion_handler = CompletionHandler()

    async def agenerate(
        self, request: ChatRequest, response_format: Optional[BaseModel] = None
    ) -> Any:
        """Generate async completion"""
        api_key = self.api_key_manager.get_key(self.model_config.provider)
        return await self.completion_handler.agenerate(
            self.model_config, request.messages, api_key, response_format
        )

    def generate(
        self, request: ChatRequest, response_format: Optional[Type[BaseModel]] = None
    ) -> Any:
        """Generate sync completion"""
        api_key = self.api_key_manager.get_key(self.model_config.provider)
        return self.completion_handler.generate(
            self.model_config, request.messages, api_key, response_format
        )
