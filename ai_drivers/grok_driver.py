"""xAI Grok driver implementation for image analysis and chat."""

from openai import OpenAI
from .base_driver import AIDriver
import logging

logger = logging.getLogger(__name__)

class GrokDriver(AIDriver):
    """xAI Grok driver implementation for image analysis."""

    def __init__(self):
        """Initialize default attributes."""
        super().__init__()
        self.client = None
        self.text_model = None
        self.vision_model = None
        self.max_tokens = None
        self.temperature = None

    def initialize(self, config):
        """Initialize the driver with configuration.

        Args:
            config (dict): Configuration with api_key, model, max_tokens, and temperature
        """
        logger.info(f"\nGrok Driver initializing with config: {config}")
        self.client = OpenAI(
            api_key=config['api_key'],
            base_url="https://api.x.ai/v1"
        )
        self.text_model = config.get('text_model', 'grok-2-latest')
        self.vision_model = config.get('vision_model', 'grok-2-vision-1212')
        self.max_tokens = config.get('max_tokens', 4096)
        self.temperature = config.get('temperature', 0.7)
        logger.info(
            "Grok Driver initialized with vision model: %s, text model: %s, max_tokens: %s, temperature: %s",
            self.vision_model,
            self.text_model,
            self.max_tokens,
            self.temperature,
        )

    def format_vision_message(self, text: str, image_data: str) -> list:
        """Format message for Grok's vision API.

        Args:
            text (str): The text prompt or message
            image_data (str): Base64 encoded image data

        Returns:
            list: Formatted messages for Grok's vision API
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
                        "url": f"data:image/jpeg;base64,{image_data}",
                        "detail": "high"
                    }
                }
            ]
        }]

    def generate_response(self, messages):
        """Generate a response from Grok.

        Args:
            messages (list): List of message objects

        Returns:
            str: Generated response text
        """
        try:
            # Format messages for Grok API
            formatted_messages = []
            for msg in messages:
                if isinstance(msg.get("content"), dict) and "image" in msg["content"]:
                    # Handle image messages
                    formatted_messages.extend(self.format_vision_message(
                        msg["content"]["text"],
                        msg["content"]["image"]["data"]
                    ))
                else:
                    # Handle text messages
                    formatted_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            # Use vision model if any message contains an image
            has_image = any(
                isinstance(msg.get("content"), list) and
                any(content.get("type") == "image_url" for content in msg.get("content", []))
                for msg in formatted_messages
            )
            model = self.vision_model if has_image else self.text_model
            logger.info(f"Using Grok model: {model}")

            response = self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                max_tokens=self.max_tokens,
                stream=True,
                temperature=self.temperature
            )

            # Collect streamed response
            collected_messages = []
            for chunk in response:
                if chunk.choices[0].delta.content:
                    collected_messages.append(chunk.choices[0].delta.content)
                    print(chunk.choices[0].delta.content, end="", flush=True)

            return "".join(collected_messages)

        except Exception as e:
            error_msg = f"Error in generate_response: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def get_default_max_tokens(self):
        """Get default maximum tokens for Grok model.

        Returns:
            int: Default maximum tokens (4096)
        """
        return 4096
