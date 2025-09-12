from pathlib import Path
from utils.get_file_info import get_file_info, get_file_content
from config.opts import MAX_FILE_CONTENT_LENGTH


def test_get_file_info_current_dir(tmp_path: Path) -> None:
    main: Path = tmp_path.joinpath("main.py")
    main.write_text("print('hello')")

    tests: Path = tmp_path.joinpath("tests.py")
    tests.write_text("print('testing...')")

    pkg: Path = tmp_path.joinpath("pkg")
    pkg.mkdir()

    result: str = get_file_info(str(tmp_path), str(tmp_path))

    assert f"- main.py: file_size={main.stat().st_size} bytes, is_dir=False" in result
    assert f"- tests.py: file_size={tests.stat().st_size} bytes, is_dir=False" in result
    assert f"- pkg: file_size={pkg.stat().st_size} bytes, is_dir=True" in result


def test_get_file_info_pkg_subdir(tmp_path: Path) -> None:
    pkg: Path = tmp_path.joinpath("pkg")
    pkg.mkdir()

    calc: Path = pkg.joinpath("calculator.py")
    calc.write_text("print('calc')")

    render: Path = pkg.joinpath("render.py")
    render.write_text("print('render')")

    result: str = get_file_info(str(tmp_path), str(pkg))

    assert (
        f"- calculator.py: file_size={calc.stat().st_size} bytes, is_dir=False"
        in result
    )
    assert (
        f"- render.py: file_size={render.stat().st_size} bytes, is_dir=False" in result
    )


def test_get_file_info_outside_absolute(tmp_path: Path) -> None:
    outside_dir: Path = Path("/bin")

    result: str = get_file_info(str(tmp_path), str(outside_dir))

    assert (
        f'Error: Cannot list "{outside_dir}" as it is outside the permitted working directory'
        in result
    )


def test_get_file_info_outside_relative(tmp_path: Path) -> None:
    parent_dir: Path = tmp_path.parent  # "../" relative to tmp_path

    result: str = get_file_info(str(tmp_path), str(parent_dir))

    assert (
        f'Error: Cannot list "{parent_dir}" as it is outside the permitted working directory'
        in result
    )


def test_get_file_content_truncating_properly() -> None:
    content = get_file_content("calculator", "lorem.txt")

    assert (
        f'\n[...File "lorem.txt" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
        in content
    )
