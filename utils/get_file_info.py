import os
import subprocess

from pathlib import Path
from config.opts import MAX_FILE_CONTENT_LENGTH


def get_file_info(working_directory: str, directory=".") -> str:
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    try:
        if not is_subdir(working_directory, directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except FileNotFoundError:
        return f"Error: Path does not exist: {directory}"
    except PermissionError:
        return f"Error: Permission denied"

    return describe_directory(directory)


def describe_directory(path: str) -> str:
    base = Path(path)
    lines = []

    try:
        for item in base.iterdir():
            try:
                size = item.stat().st_size
                lines.append(
                    f"- {item.name}: file_size={size} bytes, is_dir={item.is_dir()}"
                )
            except (PermissionError, FileNotFoundError) as e:
                lines.append(f"- {item.name}: Error accessing file info ({e})")

    except PermissionError:
        return f"Error: Permission denied"

    return "\n".join(lines)


def is_subdir(working_dir: str, target_dir: str) -> bool:
    try:
        work = Path(working_dir).resolve(strict=True)
        target = Path(target_dir).resolve(strict=True)
    except FileNotFoundError:
        raise
    except PermissionError:
        raise

    return work in target.parents or work == target


def is_subpath(working_directory: str, file_path: str) -> bool:
    try:
        Path(file_path).resolve().relative_to(Path(working_directory).resolve())
        return True
    except ValueError:
        return False


def get_file_content(working_directory: str, file_path: str) -> str:
    complete_path = os.path.join(working_directory, file_path)

    if not is_subpath(working_directory, complete_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(complete_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(complete_path, "r", encoding="utf-8") as f:
            content = f.read(
                MAX_FILE_CONTENT_LENGTH + 1
            )  # reading one extra character to check for truncation

            if len(content) > MAX_FILE_CONTENT_LENGTH:
                content = (
                    content[:MAX_FILE_CONTENT_LENGTH]
                    + f'\n[...File "{file_path}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
                )

            return content

    except PermissionError:
        return f'Error: Permission denied reading "{file_path}"'
    except OSError as e:
        return f'Error: An unexpected I/O error occurred reading "{file_path}": {e}'
    except UnicodeDecodeError:
        return f'Error: Failed to decode "{file_path}" as UTF-8 text'


def write_file(working_directory: str, file_path: str, content: str) -> str:
    complete_path = os.path.join(working_directory, file_path)

    if not is_subpath(working_directory, complete_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        with open(complete_path, "w") as f:
            f.write(content)
    except PermissionError:
        return f'Error: Cannot write "{file_path}" no permissions to write to the file'
    except IsADirectoryError:
        return f"Error: Cannot write the file path {file_path} is a directory"
    except OSError as e:
        return f"Some other I/O error occurred: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


def run_python_file(working_directory: str, file_path: str, args=[]) -> str:
    complete_path = os.path.join(working_directory, file_path)

    if not is_subpath(working_directory, complete_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(complete_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        response = subprocess.run(
            ["python3", complete_path, *args],
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30,
        )

        output = ""
        if response.stdout:
            output += f"STDOUT:\n{response.stdout}"

        if response.stderr:
            output += f"\nSTDERR:\n{response.stderr}"

        if response.returncode != 0:
            output += f"\nProcess exited with code {response.returncode}"

        if not output.strip():
            output = "No output produced."

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
