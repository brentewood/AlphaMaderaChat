"""Anthropic Claude AI driver implementation for text-based chat."""

from anthropic import Anthropic
from .base_driver import AIDriver
import logging

logger = logging.getLogger(__name__)

class ClaudeDriver(AIDriver):
    """Anthropic Claude AI driver implementation for text-based chat."""

    def initialize(self, config):
        """Initialize the driver with configuration.

        Args:
            config (dict): Configuration with api_key, model, max_tokens, and temperature
        """
        logger.info(f"\nClaude Driver initializing with config: {config}")
        self.client = Anthropic(api_key=config['api_key'])
        self.model = config.get('model', 'claude-3-5-sonnet-latest')
        self.max_tokens = config.get('max_tokens', 32768)
        self.temperature = config.get('temperature', 0.7)
        logger.info(
            "Claude Driver initialized with model: %s, max_tokens: %s, temperature: %s",
            self.model,
            self.max_tokens,
            self.temperature,
        )

    def generate_response(self, messages):
        """Generate a response from Claude.

        Args:
            messages (list): List of formatted message dictionaries

        Returns:
            str: Generated text response

        Raises:
            ValueError: If no messages provided
            Exception: If API call fails
        """
        logger.info(f"\nGenerating response using model: {self.model}")
        try:
            if not messages:
                raise ValueError("No valid messages to send")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=messages,
                stream=True
            )

            # Handle streaming response
            collected_messages = []
            for chunk in response:
                if hasattr(chunk, 'type'):
                    if chunk.type == 'content_block_delta':
                        chunk_text = chunk.delta.text
                        print(chunk_text, end='', flush=True)
                        collected_messages.append(chunk_text)
                    elif chunk.type == 'message_start':
                        continue
                    elif chunk.type == 'message_stop':
                        break

            # Return the complete message
            full_response = ''.join(collected_messages)
            print()  # Add newline after streaming
            return full_response

        except Exception as e:
            logger.error(f"\nError in generate_response: {str(e)}")
            raise e

    def get_default_max_tokens(self):
        """Get default maximum tokens for Claude model.

        Returns:
            int: Default maximum tokens (32768)
        """
        return 32768
