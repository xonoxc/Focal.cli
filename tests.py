from pathlib import Path
from utils.get_file_info import (
    get_file_info,
    write_file,
    run_python_file,
)


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


""" def test_get_file_content_truncating_properly() -> None:
    content = get_file_content("calculator", "lorem.txt")
    assert (
        f'\n[...File "lorem.txt" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
        in content
    )

    content_main = get_file_content("calculator", "main.py")
    assert isinstance(content_main, str)
    assert not content_main.startswith("Error:")

    content_pkg = get_file_content("calculator", "pkg/calculator.py")
    assert isinstance(content_pkg, str)
    assert not content_pkg.startswith("Error:")

    content_bin = get_file_content("calculator", "/bin/cat")
    assert content_bin.startswith("Error:")

    content_missing = get_file_content("calculator", "pkg/does_not_exist.py")
    assert content_missing.startswith("Error:")
"""


def test_write_file_functionality() -> None:
    content1 = "wait, this isn't lorem ipsum"
    result = write_file("calculator", "lorem.txt", content1)
    assert (
        result
        == f'Successfully wrote to "lorem.txt" ({len(content1)} characters written)'
    )

    content2 = "lorem ipsum dolor sit amet"
    result = write_file("calculator", "pkg/morelorem.txt", content2)
    assert (
        result
        == f'Successfully wrote to "pkg/morelorem.txt" ({len(content2)} characters written)'
    )

    content3 = "this should not be allowed"
    result = write_file("calculator", "/tmp/temp.txt", content3)
    assert result.startswith("Error:")


def test_run_python_file_functionality() -> None:
    result = run_python_file("calculator", "main.py")
    print(result)
    assert isinstance(result, str)

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    assert isinstance(result, str)

    result = run_python_file("calculator", "tests.py")
    print(result)
    assert isinstance(result, str)

    result = run_python_file("calculator", "../main.py")
    print(result)
    assert result.startswith("Error:")

    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    assert result.startswith("Error:")
