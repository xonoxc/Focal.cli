from google.genai import types
from .fun_schema_dec import (
    schema_get_files_info,
    schama_write_file,
    schema_run_python_file,
    schama_get_file_content,
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schama_write_file,
        schama_get_file_content,
    ]
)
