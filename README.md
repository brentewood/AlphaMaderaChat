# AI Chat Application

A command-line chat application that supports multiple AI providers (Claude, OpenAI, Grok, Gemini) with persistent chat history and configurable settings. This application is provided courtesy of AlphaMadera, LLC (https://alphamadera.com), and is not intended for production use.

## Purpose

This application serves as an educational tool and reference implementation for working with various AI chat APIs. It's designed to help:

- Students learning to integrate AI APIs into their applications
- Hobbyist developers exploring different AI chat providers
- Beginners getting started with AI development
- Anyone wanting to understand how to build chat applications with AI

Key learning opportunities:

- See how to structure API calls to different AI providers (Claude, GPT-4, Grok, Gemini)
- Learn about handling streaming responses for real-time chat
- Understand configuration management and API key security
- Explore chat history persistence and state management
- Compare different AI models and their capabilities

The code is thoroughly documented and follows best practices, making it an ideal starting point for learning AI integration.

## Setup

1. **Create a virtual environment:**
```bash
python -m venv venv
```

2. **Activate the virtual environment:**

   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   venv\Scripts\activate
   ```

3. **Install the required dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file in the project directory and add your API keys:**
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GROK_API_KEY=your_grok_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

   **To get your API keys:**
   - **Anthropic (Claude):** Visit https://console.anthropic.com/ to get your API key
   - **OpenAI (GPT):** Visit https://platform.openai.com/api-keys to get your API key
   - **xAI (Grok):** Visit https://console.x.ai/ to get your API key
   - **Google (Gemini):** Visit https://ai.google.dev/ to get your API key

5. **Configure your preferred AI provider in `config.yaml`:**
   - Set `ai_provider` to `claude`, `openai`, `grok`, or `gemini`
   - Adjust model settings, temperature, and max_tokens as needed

## Usage

1. **Make sure your virtual environment is activated:**
```bash
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

2. **Run the application:**
```bash
python app.py
```

3. Start chatting with the AI. Your conversation will be stored in `chat.json`. In fact you can switch between providers and models by editing the `config.yaml` file and the chat history will remain. Since the chat history is stored in a JSON file, you can easily edit it by hand to add or remove messages.

4. Type `QUIT` to exit the application.

## Features

- **Multiple AI Providers:** Support for Claude, OpenAI GPT, xAI Grok, and Google Gemini
- **Configurable Settings:** Easy switching between providers and model settings
- **Persistent Chat History:** Stored in `chat.json` with timestamps
- **Streaming Responses:** Real-time response generation for all providers
- **Environment Variables:** Secure API key management
- **Empty Message Prevention:** Input validation to ensure meaningful conversations

## Configuration

Edit `config.yaml` to customize:
- AI provider selection
- Model parameters (temperature, max_tokens)
- API endpoints and settings

## Supported Models

- **Claude:** claude-3-5-sonnet-latest or later (streaming via SDK)
- **OpenAI:** gpt-4o or later (streaming via SDK)
- **Grok:** grok-2-latest or later (streaming via SDK)
- **Gemini:** gemini-2.5-pro or later (streaming via REST API)

## Notes

- The default model for each provider is set in the `config.yaml` file.
- The default max tokens for each provider is set in the `config.yaml` file.
- The default temperature for each provider is set in the `config.yaml` file.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Extending the Application

This application is designed to be extensible and easy to modify. You can:

- Add support for new AI providers
- Add support for new models
- Add support for new features (e.g. image support, audio support, etc.)
- Add support for new languages
- Add support for new platforms

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## Contact

For any questions or feedback, please contact me at [brent@alphamadera.com](mailto:brent@alphamadera.com).