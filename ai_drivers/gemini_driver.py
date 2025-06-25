"""Google Gemini AI driver implementation for text-based chat using REST API."""

import requests
import json
from .base_driver import AIDriver
import logging

logger = logging.getLogger(__name__)

class GeminiDriver(AIDriver):
    """Google Gemini AI driver implementation using REST API for text-based chat."""

    def __init__(self):
        """Initialize default attributes."""
        super().__init__()
        self.api_key = None
        self.model = None
        self.max_tokens = None
        self.temperature = None
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def initialize(self, config):
        """Initialize the driver with configuration.

        Args:
            config (dict): Configuration with api_key, model, max_tokens, and temperature
        """
        logger.info(f"\nGemini Driver initializing with config: {config}")

        # Check if API key is provided
        self.api_key = config.get('api_key')
        if not self.api_key:
            raise ValueError(
                "Gemini API key is required. Please:\n"
                "1. Get your API key from https://ai.google.dev/\n"
                "2. Add GEMINI_API_KEY=your_key_here to your .env file\n"
                "3. Make sure your .env file is in the project root directory"
            )

        self.model = config.get('model', 'gemini-2.5-pro')
        self.max_tokens = config.get('max_tokens', 8192)
        self.temperature = config.get('temperature', 0.7)

        logger.info(
            "Gemini Driver initialized with model: %s, max_tokens: %s, temperature: %s",
            self.model,
            self.max_tokens,
            self.temperature,
        )

    def _parse_sse_line(self, line):
        """Parse a Server-Sent Events line.

        Args:
            line (str): SSE line to parse

        Returns:
            dict or None: Parsed JSON data or None if not a data line
        """
        line = line.strip()
        if line.startswith('data: '):
            data_content = line[6:]  # Remove 'data: ' prefix
            if data_content and data_content != '[DONE]':
                try:
                    return json.loads(data_content)
                except json.JSONDecodeError:
                    return None
        return None

    def generate_response(self, messages):
        """Generate a streaming response from Gemini using REST API.

        Args:
            messages (list): List of formatted message dictionaries

        Returns:
            str: Generated text response

        Raises:
            Exception: If API call fails
        """
        logger.info(f"\nGenerating response using model: {self.model}")
        try:
            # Convert messages to Gemini format
            contents = []

            # Handle system messages by prepending to the first user message
            system_message = None
            for msg in messages:
                if msg['role'] == 'system':
                    system_message = msg['content']
                    break

            # Convert conversation to Gemini format
            for msg in messages:
                if msg['role'] == 'user':
                    content = msg['content']
                    # Prepend system message to first user message if present
                    if system_message:
                        content = f"{system_message}\n\n{content}"
                        system_message = None  # Only prepend once

                    contents.append({
                        "role": "user",
                        "parts": [{"text": content}]
                    })
                elif msg['role'] == 'assistant':
                    contents.append({
                        "role": "model",
                        "parts": [{"text": msg['content']}]
                    })

            # Prepare the request payload
            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": self.temperature,
                    "maxOutputTokens": self.max_tokens,
                    "candidateCount": 1
                }
            }

            # Use streaming endpoint
            url = f"{self.base_url}/{self.model}:streamGenerateContent"
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "key": self.api_key,
                "alt": "sse"  # Request Server-Sent Events format
            }

            logger.info(f"Making streaming request to: {url}")

            # Make streaming request
            response = requests.post(
                url,
                headers=headers,
                params=params,
                json=payload,
                timeout=60,
                stream=True
            )

            if response.status_code != 200:
                error_msg = f"API request failed with status {response.status_code}: {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)

            # Process streaming response
            collected_text = []

            print("\nA: ", end="", flush=True)

            for line in response.iter_lines(decode_unicode=True):
                if line:
                    data = self._parse_sse_line(line)
                    if data and 'candidates' in data:
                        for candidate in data['candidates']:
                            if 'content' in candidate and 'parts' in candidate['content']:
                                for part in candidate['content']['parts']:
                                    if 'text' in part:
                                        text_chunk = part['text']
                                        print(text_chunk, end="", flush=True)
                                        collected_text.append(text_chunk)

            print()  # Add newline after streaming

            # Return the complete response
            full_response = ''.join(collected_text)
            return full_response.strip() if full_response else "I apologize, but I couldn't generate a response. Please try again."

        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            logger.error(f"\nError in generate_response: {str(e)}")
            raise e

    def get_default_max_tokens(self):
        """Get default maximum tokens for Gemini model.

        Returns:
            int: Default maximum tokens (8192)
        """
        return 8192