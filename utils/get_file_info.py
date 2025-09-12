import os

from pathlib import Path


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
