# Focal.CLI 

Focal is a command-line AI coding agent powered by the Gemini API. It can interact with your local filesystem to perform tasks such as listing files, reading and writing file content, and executing Python scripts. The agent is designed to be a helpful tool for developers, providing a conversational interface to automate and assist with coding-related tasks.

## Features

- **Conversational AI:** Interact with the agent using natural language prompts.
- **File System Operations:** The agent can list files, read file content, and write to files within the project's working directory.
- **Python Script Execution:** Execute Python scripts directly from the agent.
- **Command-Line Interface:** A rich and user-friendly command-line interface with formatted output.
- **Standalone Calculator:** The project also includes a standalone command-line calculator for evaluating mathematical expressions. (can be used for testing the agent)

## Getting Started

### Prerequisites

- Python 3.10 or higher
- `uv` package manager

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/xonoxc/Focal.cli.git
    cd Focal.cli
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies using `uv`:**
    ```bash
    uv pip install -r requirements.txt
    ```

### Configuration

1.  **Create a `.env` file** by copying the `sample.env` file:
    ```bash
    cp sample.env .env
    ```

2.  **Add your Gemini API key** to the `.env` file:
    ```
    GEMINI_API_KEY=your_api_key
    ```

## Usage

### AI Agent

To use the AI agent, run the `main.py` script with your prompt as an argument:

```bash
uv run python main.py "your prompt here"
```

For example:

```bash
uv run python main.py "list all the files in the calculator directory"
```

You can also enable verbose mode to see more detailed output:

```bash
uv run python main.py "your prompt here" --verbose
```

### Calculator

The project includes a standalone calculator that can be used from the command line:

```bash
python calculator/main.py "3 + 5"
```

## Project Structure

```
.
├── calculator/       # Standalone calculator application for testing the agent
├── config/           # Project configuration
├── main.py           # Main entry point for the AI agent
├── system/           # System prompts for the AI agent
├── tests/            # Tests for the utility functions
├── tests.py          # Additional tests
└── utils/            # Utility functions for the AI agent
```

-   **`calculator/`**: Contains the standalone calculator application for testing the agent.
-   **`config/`**: Contains configuration files for the project.
-   **`main.py`**: The main entry point for the AI coding agent.
-   **`system/`**: Contains the system prompt that defines the agent's behavior.
-   **`tests/`**: Contains tests for the file utility functions.
-   **`tests.py`**: Contains additional tests for the project.
-   **`utils/`**: Contains utility functions for the agent, including tools for file system operations and the user interface.

## Running Tests

To run the tests, use `pytest`:

```bash
pytest -v tests.py
```
