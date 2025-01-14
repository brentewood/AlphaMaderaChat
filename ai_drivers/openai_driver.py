from openai import OpenAI
from .base_driver import AIDriver

class OpenAIDriver(AIDriver):
    def initialize(self, config):
        print(f"\nOpenAI Driver initializing with config: {config}")
        self.client = OpenAI(api_key=config['api_key'])
        self.model = config.get('model', 'gpt-4o')
        self.max_tokens = config.get('max_tokens', 4096)
        print(f"OpenAI Driver initialized with model: {self.model}, max_tokens: {self.max_tokens}")

    def generate_response(self, messages):
        print(f"\nGenerating response using model: {self.model}")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=messages,
                stream=True  # Enable streaming
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
        return 4096