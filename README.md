# Claude Chat Application

A command-line chat application that uses Claude AI (via the Anthropic API) with persistent chat history.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project directory and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Start chatting with the AI. Your conversation will be stored in `chat.json`.

3. Type `QUIT` to exit the application.

## Features

- Persistent chat history stored in `chat.json`
- Timestamps for all messages
- Automatic context loading from previous conversations
- Simple command-line interface