"""Chat application module for interacting with AI models through a command-line interface."""

import json
import os
import datetime
import yaml
from dotenv import load_dotenv
from ai_drivers.claude_driver import ClaudeDriver
from ai_drivers.openai_driver import OpenAIDriver

class AIChat:
    """Chat interface for interacting with AI models.

    Supports multiple AI providers and handles message history and configuration."""

    DRIVER_MAPPING = {
        'claude': ClaudeDriver,
        'openai': OpenAIDriver
    }

    def __init__(self):
        """Initialize chat interface with configuration and history."""
        self.load_config()
        self.initialize_driver()
        self.history = self.load_chat_history()
        self.messages = []

    def load_config(self):
        """Load configuration from config.yaml and replace environment variables."""
        load_dotenv()
        print("\nLoading configuration...")
        with open('config.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
            print("Loaded config:", self.config)

        # Replace environment variables in config
        provider_config = self.config[self.config['ai_provider']]
        print("Provider config before env vars:", provider_config)
        provider_config['api_key'] = os.getenv(provider_config['api_key'].replace('${', '').replace('}', ''))
        print("Provider config after env vars:", provider_config)

    def initialize_driver(self):
        """Initialize the AI driver based on the configured provider."""
        provider = self.config['ai_provider']
        print("\nInitializing", provider, "driver...")
        if provider not in self.DRIVER_MAPPING:
            raise ValueError(f"Unsupported AI provider: {provider}")

        driver_class = self.DRIVER_MAPPING[provider]
        self.driver = driver_class()
        print("Initializing driver with config:", self.config[provider])
        self.driver.initialize(self.config[provider])

    def load_initial_prompt(self):
        """Load initial prompt from assistant.txt if it exists."""
        try:
            with open('assistant.txt', 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def load_chat_history(self):
        """Load chat history from chat.json or initialize an empty history."""
        try:
            with open('chat.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"messages": []}

    def save_chat_history(self, history):
        """Save chat history to chat.json.

        Args:
            history (dict): Chat history to save
        """
        with open('chat.json', 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)

    def format_message(self, role, content):
        """Format a message with role, content, and timestamp.

        Args:
            role (str): Message role (user/assistant)
            content (str): Message content

        Returns:
            dict: Formatted message
        """
        return {
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def process_initial_prompt(self):
        """Process the initial prompt if it exists and no chat history is present."""
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
            except json.JSONDecodeError as e:
                print("\nJSON parsing error:", str(e))
            except yaml.YAMLError as e:
                print("\nYAML parsing error:", str(e))
            except (IOError, OSError) as e:
                print("\nI/O error:", str(e))
            except KeyError as e:
                print("\nConfiguration key error:", str(e))
            except ValueError as e:
                print("\nValue error:", str(e))

    def run(self):
        """Main loop for the chat application."""
        self.process_initial_prompt()

        # Load existing chat history into messages
        if self.history["messages"]:
            for msg in self.history["messages"]:
                self.messages.append({"role": msg["role"], "content": msg["content"]})

        print("Chat started using", self.config['ai_provider'].upper(), "Type 'QUIT' to exit.")
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
                print("\nAssistant:")
                assistant_response = self.driver.generate_response(self.messages)

                # Add assistant message to history
                assistant_message = self.format_message("assistant", assistant_response)
                self.history["messages"].append(assistant_message)
                self.save_chat_history(self.history)

                # Update messages for next iteration
                self.messages.append({"role": "assistant", "content": assistant_response})

            except json.JSONDecodeError as e:
                print("\nJSON parsing error:", str(e))
            except yaml.YAMLError as e:
                print("\nYAML parsing error:", str(e))
            except (IOError, OSError) as e:
                print("\nI/O error:", str(e))
            except KeyError as e:
                print("\nConfiguration key error:", str(e))
            except ValueError as e:
                print("\nValue error:", str(e))

def main():
    """Main function to run the chat application."""
    chat = AIChat()
    chat.run()

if __name__ == "__main__":
    main()