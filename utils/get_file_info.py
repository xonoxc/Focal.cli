import os

from pathlib import Path
from config.opts import MAX_FILE_CONTENT_LENGTH


def get_file_info(working_direcory: str, directory=".") -> str:
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    try:
        if not is_subdir(working_direcory, directory):
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
    if not is_subpath(working_directory, file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_FILE_CONTENT_LENGTH)

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
