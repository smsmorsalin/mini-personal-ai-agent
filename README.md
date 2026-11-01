# Mini Personal AI Agent

A beginner-friendly, tool-using AI assistant built with Python and the
OpenAI API. The project demonstrates how an LLM can understand a
request, choose an available tool, receive the tool's result, and
produce a final response.

> **Development setup:** OpenCode is used as the AI coding assistant,
> with the OpenAI GPT-6 Astra model selected in OpenCode. OpenCode helps
> develop this project; it is not the runtime engine of the Python
> application. The application itself calls the OpenAI API using the
> official Python SDK.

## Features

-   **AI chat** --- respond to natural-language questions.
-   **Calculator tool** --- perform supported arithmetic operations.
-   **Date and time tool** --- retrieve the computer's current date and
    time.
-   **Notes reader tool** --- read the contents of `notes.txt`.
-   **Conversation continuity** --- keep context between turns during
    the current session using response IDs.

## How it works

1.  The user enters a message in the terminal.
2.  The Python application sends the message and tool descriptions to
    the OpenAI Responses API.
3.  The model decides whether it can answer directly or needs a tool.
4.  If a tool is needed, the model returns a function-call request.
5.  Python validates the requested tool name, executes the corresponding
    local function, and collects its result.
6.  The application sends the tool result back to the model.
7.  The model generates a final response for the user.

``` text
User
  |
  v
Python application (main.py)
  |
  v
OpenAI Responses API <----> AI model
  |
  | tool-call request
  v
Python tool dispatcher
  |
  +---- calculator()
  |
  +---- get_datetime()
  |
  +---- read_notes()
  |
  v
Tool result sent back to the model
  |
  v
Final response to the user
```

The model does not directly run local Python code. It requests a tool
call; the application executes the function and returns its output.

## Project structure

``` text
mini-ai-agent/
├── main.py          # Starts the chat and manages the agent/tool-call loop
├── tools.py         # Contains the calculator, date/time, and file-reader tools
├── notes.txt        # Sample text file the agent can read
├── .env             # Stores the OpenAI API key (never commit this file)
├── .gitignore       # Excludes secrets and local environment files
└── README.md
```

## Requirements

-   Python 3.10 or newer
-   An OpenAI API account with API access
-   An API key and access to a model supported by your API account
-   Internet access when making API requests

**Important:** A ChatGPT subscription and OpenAI API billing are
separate. Using a model in OpenCode does not automatically provide an
API key or API credits to this Python application.

## Setup

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR-USERNAME/mini-ai-agent.git
cd mini-ai-agent
```

Replace `YOUR-USERNAME` with your GitHub username and adjust the
repository name if needed.

### 2. Create and activate a virtual environment

Linux / macOS:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` bash
pip install openai python-dotenv
```

If you maintain a `requirements.txt`, you can instead install with:

``` bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a file named `.env` in the project root:

``` env
OPENAI_API_KEY=your_openai_api_key_here
```

Do not add quotation marks unless your environment requires them. Never
share this key or commit `.env` to GitHub.

### 5. Configure the model

Check the model setting in `main.py`. Use a model identifier that is
actually available to your OpenAI API account. The model selected inside
OpenCode is a separate setting and may not be a valid API model
identifier for this application.

### 6. Run the agent

``` bash
python main.py
```

Type `exit` or `quit` to end the session.

## Example prompts

Try these prompts in the terminal:

``` text
Calculate 500 multiplied by 25.
What is the current date and time?
Read my notes and summarize my project.
What programming languages are mentioned in my notes?
```

The agent should select the relevant tool when needed. Exact responses
and tool-selection behavior can vary by model.

## Available tools

  Tool             Purpose
  ---------------- ---------------------------------------------
  `calculator`     Evaluates supported arithmetic expressions.
  `get_datetime`   Returns the local computer date and time.
  `read_notes`     Reads the sample `notes.txt` file.

## Security notes

-   Keep `.env` out of version control.
-   If an API key is accidentally published, revoke it and create a new
    one.
-   Only expose tools that are safe for the agent to call.
-   Validate tool arguments and restrict file access. Do not let an LLM
    choose arbitrary file paths or execute arbitrary shell commands.
-   Add authentication and authorization before connecting the agent to
    private systems or databases.
-   Review tool actions before allowing the agent to modify or delete
    important data.

## Current limitations

-   The agent is a small learning project, not a production-ready
    autonomous system.
-   Tool execution is limited to the functions explicitly registered in
    the application.
-   Conversation context is maintained for the current running session;
    it is not persistent long-term memory.
-   The file reader is intended for the sample notes file, not
    unrestricted filesystem access.
-   API requests require internet access and may incur usage charges.

## Learning goals

This project is intended to help beginners understand:

-   Large Language Models (LLMs)
-   Prompting and system instructions
-   Function calling / tool calling
-   Agent loops (decide → act → observe → respond)
-   Conversation context
-   Separating the AI model from the tools it can use

## Possible future improvements

-   Add a tool that safely creates a text file.
-   Add persistent conversation memory.
-   Add a web-search tool with appropriate source handling.
-   Add a simple web interface.
-   Add PDF reading and retrieval-augmented generation (RAG).
-   Connect the agent to a Django application through
    permission-controlled APIs.

------------------------------------------------------------------------

**Built as a hands-on learning project to understand how AI agents use
tools.**
