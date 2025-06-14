from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file


def call_function(function_call_item, verbose=False):
    function_name = function_call_item.name
    function_args = function_call_item.args
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    available_functions = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    keyword_args = {**function_args} | {"working_directory": "./calculator"}

    if function_name not in available_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name, response={"error": f"Unknown function: {function_name}"}
                )
            ],
        )

    function_result = available_functions[function_name](**keyword_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
