import json
import os
import datetime
import yaml
from dotenv import load_dotenv
from ai_drivers.claude_driver import ClaudeDriver
from ai_drivers.openai_driver import OpenAIDriver

class AIChat:
    DRIVER_MAPPING = {
        'claude': ClaudeDriver,
        'openai': OpenAIDriver
    }

    def __init__(self):
        self.load_config()
        self.initialize_driver()
        self.history = self.load_chat_history()
        self.messages = []

    def load_config(self):
        load_dotenv()
        with open('config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)

        # Replace environment variables in config
        provider_config = self.config[self.config['ai_provider']]
        provider_config['api_key'] = os.getenv(provider_config['api_key'].replace('${', '').replace('}', ''))

    def initialize_driver(self):
        provider = self.config['ai_provider']
        if provider not in self.DRIVER_MAPPING:
            raise ValueError(f"Unsupported AI provider: {provider}")

        driver_class = self.DRIVER_MAPPING[provider]
        self.driver = driver_class()
        self.driver.initialize(self.config[provider])

    def load_initial_prompt(self):
        try:
            with open('assistant.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def load_chat_history(self):
        try:
            with open('chat.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"messages": []}

    def save_chat_history(self, history):
        with open('chat.json', 'w') as f:
            json.dump(history, f, indent=2)

    def format_message(self, role, content):
        return {
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def process_initial_prompt(self):
        initial_prompt = self.load_initial_prompt()
        if initial_prompt and not self.history["messages"]:
            try:
                assistant_response = self.driver.generate_response(
                    [{"role": "user", "content": initial_prompt}]
                )

                user_message = self.format_message("user", initial_prompt)
                assistant_message = self.format_message("assistant", assistant_response)

                self.history["messages"].extend([user_message, assistant_message])
                self.save_chat_history(self.history)

                self.messages.extend([
                    {"role": "user", "content": initial_prompt},
                    {"role": "assistant", "content": assistant_response}
                ])

                print("\nInitial prompt from assistant.txt processed.")
                print("-" * 50)
            except Exception as e:
                print(f"\nError processing initial prompt: {str(e)}")

    def run(self):
        self.process_initial_prompt()

        # Load existing chat history into messages
        if self.history["messages"]:
            for msg in self.history["messages"]:
                self.messages.append({"role": msg["role"], "content": msg["content"]})

        print(f"Chat started using {self.config['ai_provider'].upper()}. Type 'QUIT' to exit.")
        print("-" * 50)

        while True:
            user_input = input("\nYou: ").strip()

            if user_input.upper() == "QUIT":
                break

            # Add user message to history
            user_message = self.format_message("user", user_input)
            self.history["messages"].append(user_message)
            self.save_chat_history(self.history)

            # Prepare messages for API call
            self.messages.append({"role": "user", "content": user_input})

            try:
                assistant_response = self.driver.generate_response(self.messages)
                print(f"\nAssistant: {assistant_response}")

                # Add assistant message to history
                assistant_message = self.format_message("assistant", assistant_response)
                self.history["messages"].append(assistant_message)
                self.save_chat_history(self.history)

                # Update messages for next iteration
                self.messages.append({"role": "assistant", "content": assistant_response})

            except Exception as e:
                print(f"\nError: {str(e)}")

def main():
    chat = AIChat()
    chat.run()

if __name__ == "__main__":
    main()