import os

from google.genai import types


def write_file(working_directory, filepath, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, filepath))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{filepath}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        try:
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory {e}"

    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: "{filepath}" is a directory, not a file'

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{filepath}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing to file: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes a file with content, creating the file if it doesn't exist. Operation restrained to files within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filepath": types.Schema(
                type=types.Type.STRING,
                description="The filepath of the chosen file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.TYPE_UNSPECIFIED, description="The content that will be added to the file when written."
            ),
        },
    ),
)
