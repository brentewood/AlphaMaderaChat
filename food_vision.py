import os
import uuid
import base64
from typing import Tuple
import yaml
from dotenv import load_dotenv
from ai_drivers.claude_driver import ClaudeDriver
from ai_drivers.openai_driver import OpenAIDriver
from s3_utils import S3Utils
from PIL import Image
import io

class FoodVision:
    """A class that analyzes food images using AI vision APIs and stores them in S3.

    Combines AWS S3 storage with AI vision analysis to process food images and generate descriptions."""

    DRIVER_MAPPING = {
        'claude': ClaudeDriver,
        'openai': OpenAIDriver
    }

    MAX_IMAGE_SIZE = (800, 800)  # Maximum dimensions for resized image

    def __init__(self, image_path: str, hint: str = None, prompt: str = None):
        """Initialize FoodVision with image path and optional hint/prompt"""
        self.image_path = image_path
        self.hint = hint
        self.prompt = prompt or "Please describe what food items you see in this image in detail."

        # Load configuration
        self.load_config()

        # Initialize S3
        self.s3 = S3Utils(
            access_key=os.getenv('AWS_ACCESS_KEY'),
            secret_key=os.getenv('AWS_SECRET_KEY'),
            region_name=os.getenv('AWS_REGION'),
            bucket_name=os.getenv('AWS_BUCKET')
        )

        # Initialize AI driver
        self.initialize_driver()

    def load_config(self):
        """Load configuration from config.yaml and environment variables"""
        load_dotenv()
        with open('config.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        # Replace environment variables in config
        provider_config = self.config[self.config['ai_provider']]
        provider_config['api_key'] = os.getenv(provider_config['api_key'].replace('${', '').replace('}', ''))

    def initialize_driver(self):
        """Initialize the AI driver based on configuration"""
        provider = self.config['ai_provider']
        if provider not in self.DRIVER_MAPPING:
            raise ValueError(f"Unsupported AI provider: {provider}")

        driver_class = self.DRIVER_MAPPING[provider]
        self.driver = driver_class()
        self.driver.initialize(self.config[provider])

    def encode_image(self) -> str:
        """Convert image to base64 encoding with resizing if needed"""
        # Open and resize image if necessary
        with Image.open(self.image_path) as img:
            # Convert to RGB if not already
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize if larger than MAX_IMAGE_SIZE while maintaining aspect ratio
            if img.size[0] > self.MAX_IMAGE_SIZE[0] or img.size[1] > self.MAX_IMAGE_SIZE[1]:
                img.thumbnail(self.MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)

            # Save to bytes
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            image_data = buffer.getvalue()

        return base64.b64encode(image_data).decode('utf-8')

    def upload_to_s3(self) -> str:
        """Upload image to S3 with UUID filename"""
        # Generate UUID filename while preserving extension
        _, ext = os.path.splitext(self.image_path)
        s3_key = f"food_images/{str(uuid.uuid4())}{ext}"

        # Upload file
        self.s3.upload_file(self.image_path, s3_key)

        # Construct and return S3 URL
        return f"https://{os.getenv('AWS_BUCKET')}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{s3_key}"

    def analyze(self) -> Tuple[str, str]:
        """Analyze the image and return (S3 URL, description)"""
        # Upload to S3
        s3_url = self.upload_to_s3()

        # Prepare image data
        image_data = self.encode_image()

        # Construct message for AI
        message_content = f"{self.prompt}\n"
        if self.hint:
            message_content += f"Additional context: {self.hint}\n"

        # Format messages based on provider
        provider = self.config['ai_provider']
        if provider == 'claude':
            messages = [{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message_content
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
        else:  # OpenAI
            messages = [{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message_content
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }]

        # Get AI description
        description = self.driver.generate_response(messages)

        return s3_url, description