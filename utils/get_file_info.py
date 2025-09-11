import os

from pathlib import Path


def get_file_info(working_direcory: str, directory=".") -> str:
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    if not is_subdir(working_direcory, directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    return describe_directory(directory)


def describe_directory(path: str) -> str:
    base = Path(path)

    lines = []
    for item in base.iterdir():
        size = item.stat().st_size
        lines.append(f"- {item.name}: file_size={size} bytes, is_dir={item.is_dir()}")

    return "\n".join(lines)


def is_subdir(working_dir: str, target_dir: str) -> bool:
    work = Path(working_dir).resolve(strict=True)
    target = Path(target_dir).resolve(strict=True)
    return work in target.parents or work == target
