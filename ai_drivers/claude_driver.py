from anthropic import Anthropic
from .base_driver import AIDriver

class ClaudeDriver(AIDriver):
    def initialize(self, config):
        self.client = Anthropic(api_key=config['api_key'])
        self.model = config.get('model', 'claude-3-sonnet-20240229')
        self.max_tokens = config.get('max_tokens', 32768)

    def generate_response(self, messages):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages
        )
        return response.content[0].text

    def get_default_max_tokens(self):
        return 32768