# AI Chat Application

A command-line chat application that supports multiple AI providers (Claude, OpenAI, Grok) with persistent chat history and configurable settings.

## Purpose

This application serves as an educational tool and reference implementation for working with various AI chat APIs. It's designed to help:

- Students learning to integrate AI APIs into their applications
- Hobbyist developers exploring different AI chat providers
- Beginners getting started with AI development
- Anyone wanting to understand how to build chat applications with AI

Key learning opportunities:

- See how to structure API calls to different AI providers (Claude, GPT-4, Grok)
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
```

5. **Configure your preferred AI provider in `config.yaml`:**
   - Set `ai_provider` to `claude`, `openai`, or `grok`
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

3. Start chatting with the AI. Your conversation will be stored in `chat.json`.

4. Type `QUIT` to exit the application.

## Features

- **Multiple AI Providers:** Support for Claude, OpenAI GPT, and xAI Grok
- **Configurable Settings:** Easy switching between providers and model settings
- **Persistent Chat History:** Stored in `chat.json` with timestamps
- **Streaming Responses:** Real-time response generation
- **Environment Variables:** Secure API key management
- **Empty Message Prevention:** Input validation to ensure meaningful conversations

## Configuration

Edit `config.yaml` to customize:
- AI provider selection
- Model parameters (temperature, max_tokens)
- API endpoints and settings

## Supported Models

- **Claude:** claude-3-5-sonnet-latest or later
- **OpenAI:** gpt-4o or later
- **Grok:** grok-2-latest or later

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