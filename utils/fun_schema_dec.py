from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_file_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            )
        },
    ),
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description='Runs a python file and if the response is in the form STDOUT:\n{response.stdout} , and error \nSTDERR:\n{response.stderr}, if the process exits with 0 statuscode \nProcess exited with code {response.returncode} if no output "No output produced." is returned from the function',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the python file to run",
            )
        },
    ),
)


schama_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Wrties the string content inside a file in file_path directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write in",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write in the file",
            ),
        },
    ),
)

schama_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrives the file content in string format and Error: prefixed string if there is an error",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write in",
            ),
        },
    ),
)
