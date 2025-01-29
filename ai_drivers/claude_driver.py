from anthropic import Anthropic
from .base_driver import AIDriver

class ClaudeDriver(AIDriver):
    """Anthropic Claude AI driver implementation for vision analysis."""

    def initialize(self, config):
        """Initialize the driver with configuration.

        Args:
            config (dict): Configuration with api_key, model, max_tokens, and temperature
        """
        print(f"\nClaude Driver initializing with config: {config}")
        self.client = Anthropic(api_key=config['api_key'])
        self.model = config.get('model', 'claude-3-sonnet-20240229')
        self.max_tokens = config.get('max_tokens', 32768)
        self.temperature = config.get('temperature', 0.7)
        print(f"Claude Driver initialized with model: {self.model}, max_tokens: {self.max_tokens}, temperature: {self.temperature}")

    def format_vision_message(self, text: str, image_data: str) -> list:
        """Format message for Claude's vision API.

        Args:
            text (str): The text prompt or message
            image_data (str): Base64 encoded image data

        Returns:
            list: Formatted messages for Claude's vision API
        """
        return [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data
                    }
                }
            ]
        }]

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
        print(f"\nGenerating response using model: {self.model}")
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
            print(f"\nError in generate_response: {str(e)}")
            raise e

    def get_default_max_tokens(self):
        """Get default maximum tokens for Claude model.

        Returns:
            int: Default maximum tokens (32768)
        """
        return 32768