import inspect
import os
from google.genai import types
from .get_file_info import (
    get_file_info,
    get_file_content,
    run_python_file,
    write_file,
)


available_functions_to_call = {
    f.__name__: f
    for f in [get_file_info, get_file_content, run_python_file, write_file]
}


def call_function(function_call_part: types.FunctionCall, verbose=False):
    fn_name = function_call_part.name
    fn_args = dict(function_call_part.args)

    if fn_name not in available_functions_to_call:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fn_name,
                    response={"error": f"Unknown function: {fn_name}"},
                )
            ],
        )

    fn = available_functions_to_call[fn_name]

    fn_signature = inspect.signature(fn)
    params = list(fn_signature.parameters.values())

    # i will auto inject the working_directory whereever needed
    if params:
        first_param = params[0]
        if first_param.name == "working_directory" and first_param.name not in fn_args:
            fn_args[first_param.name] = os.getcwd()

    if verbose:
        print(f"Calling function: {fn_name}({fn_args})")
    else:
        print(f" - Calling function: {fn_name}")

    result = fn(**fn_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fn_name,
                response={"result": result},
            )
        ],
    )
