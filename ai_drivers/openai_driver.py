"""OpenAI GPT driver implementation for text-based chat."""

from openai import OpenAI
from .base_driver import AIDriver
import logging

logger = logging.getLogger(__name__)

class OpenAIDriver(AIDriver):
    """OpenAI GPT driver implementation for text-based chat."""

    def initialize(self, config):
        """Initialize the driver with configuration.

        Args:
            config (dict): Configuration with api_key, model, max_tokens, and temperature
        """
        logger.info(f"\nOpenAI Driver initializing with config: {config}")
        self.client = OpenAI(api_key=config['api_key'])
        self.model = config.get('model', 'chatgpt-4o-latest')
        self.max_tokens = config.get('max_tokens', 4096)
        self.temperature = config.get('temperature', 0.7)
        logger.info(
            "OpenAI Driver initialized with model: %s, max_tokens: %s, temperature: %s",
            self.model,
            self.max_tokens,
            self.temperature,
        )

    def generate_response(self, messages):
        """Generate a response from OpenAI.

        Args:
            messages (list): List of formatted message dictionaries

        Returns:
            str: Generated text response

        Raises:
            Exception: If API call fails
        """
        logger.info(f"\nGenerating response using model: {self.model}")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=True
            )

            # Handle streaming response
            collected_messages = []
            for chunk in response:
                if chunk.choices[0].delta.content:
                    chunk_message = chunk.choices[0].delta.content
                    print(chunk_message, end='', flush=True)
                    collected_messages.append(chunk_message)

            # Return the complete message
            full_response = ''.join(collected_messages)
            print()  # Add newline after streaming
            return full_response

        except Exception as e:
            logger.error(f"\nError in generate_response: {str(e)}")
            raise e

    def get_default_max_tokens(self):
        """Get default maximum tokens for GPT model.

        Returns:
            int: Default maximum tokens (4096)
        """
        return 4096
