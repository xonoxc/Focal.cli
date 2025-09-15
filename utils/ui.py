from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.json import JSON

console = Console()


def print_user_message(message: str):
    """Prints the user message with a user icon."""
    console.print(Text(f" User: {message}", style="cyan"))


def print_model_response(message: str):
    """Prints the model's response with markdown formatting and a model icon."""
    console.print(Text("󰟍  Model:", style="green"))
    console.print(Markdown(message))


def print_function_call(function_name: str, args: dict):
    """Prints a function call with syntax highlighting."""
    arg_json = JSON.from_data(args)
    console.print(
        Panel(
            arg_json,
            title=f"[bold yellow]Function Call → {function_name}[/bold yellow]",
            border_style="yellow",
        )
    )


def print_tool_response(message: str | dict):
    """Prints the tool's response in a formatted panel."""
    if isinstance(message, dict):
        pretty = JSON.from_data(message)
        console.print(
            Panel(
                pretty,
                title="[bold magenta]Tool Response[/bold magenta]",
                border_style="magenta",
            )
        )

    else:
        console.print(
            Panel(
                message,
                title="[bold magenta]Tool Response[/bold magenta]",
                border_style="magenta",
            )
        )


def print_error(message: str):
    """Prints an error message in a formatted panel."""
    console.print(
        Panel(
            Text(message, style="bold red"),
            title="[bold red]Error[/bold red]",
            border_style="red",
        )
    )


def print_info(message: str):
    """Prints an informational message."""
    console.print(Text(f" {message}", style="blue"))
