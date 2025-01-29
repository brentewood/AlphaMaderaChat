"""OpenAI GPT-4 Vision driver implementation for image analysis and chat."""

from openai import OpenAI
from .base_driver import AIDriver

class OpenAIDriver(AIDriver):
    """OpenAI GPT-4 Vision driver implementation for image analysis."""

    def initialize(self, config):
        """Initialize the driver with configuration.

        Args:
            config (dict): Configuration with api_key, model, max_tokens, and temperature
        """
        print(f"\nOpenAI Driver initializing with config: {config}")
        self.client = OpenAI(api_key=config['api_key'])
        self.model = config.get('model', 'gpt-4-vision-preview')
        self.max_tokens = config.get('max_tokens', 4096)
        self.temperature = config.get('temperature', 0.7)
        print(f"OpenAI Driver initialized with model: {self.model}, max_tokens: {self.max_tokens}, temperature: {self.temperature}")

    def format_vision_message(self, text: str, image_data: str) -> list:
        """Format message for OpenAI's vision API.

        Args:
            text (str): The text prompt or message
            image_data (str): Base64 encoded image data

        Returns:
            list: Formatted messages for OpenAI's vision API
        """
        return [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                }
            ]
        }]

    def generate_response(self, messages):
        """Generate a response from OpenAI.

        Args:
            messages (list): List of formatted message dictionaries

        Returns:
            str: Generated text response

        Raises:
            Exception: If API call fails
        """
        print(f"\nGenerating response using model: {self.model}")
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
            print(f"\nError in generate_response: {str(e)}")
            raise e

    def get_default_max_tokens(self):
        """Get default maximum tokens for GPT-4 Vision model.

        Returns:
            int: Default maximum tokens (4096)
        """
        return 4096