from anthropic import Anthropic
from .base_driver import AIDriver

class ClaudeDriver(AIDriver):
    def initialize(self, config):
        print(f"\nClaude Driver initializing with config: {config}")
        self.client = Anthropic(api_key=config['api_key'])
        self.model = config.get('model', 'claude-3-sonnet-20240229')
        self.max_tokens = config.get('max_tokens', 32768)
        print(f"Claude Driver initialized with model: {self.model}, max_tokens: {self.max_tokens}")

    def generate_response(self, messages):
        print(f"\nGenerating response using model: {self.model}")
        try:
            # Convert and clean messages format
            formatted_messages = []
            for msg in messages:
                if msg.get('content'):  # Only include messages with content
                    formatted_messages.append({
                        "role": "assistant" if msg['role'] == 'assistant' else "user",
                        "content": msg['content']
                    })

            if not formatted_messages:
                raise ValueError("No valid messages to send")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=formatted_messages,
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
        return 32768