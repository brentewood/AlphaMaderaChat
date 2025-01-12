from openai import OpenAI
from .base_driver import AIDriver

class OpenAIDriver(AIDriver):
    def initialize(self, config):
        self.client = OpenAI(api_key=config['api_key'])
        self.model = config.get('model', 'gpt-4-turbo-preview')
        self.max_tokens = config.get('max_tokens', 4096)

    def generate_response(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages
        )
        return response.choices[0].message.content

    def get_default_max_tokens(self):
        return 4096