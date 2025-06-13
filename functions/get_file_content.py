import os

from config import CHAR_LIMIT


def get_file_content(working_directory, filepath):
    abs_working_dir = os.path.abspath(working_directory)
    abs_filepath = os.path.abspath(os.path.join(abs_working_dir, filepath))

    if not abs_filepath.startswith(abs_working_dir):
        return f"Error: Cannot read {filepath} as it is outside the permitted working directory"
    if not os.path.isfile(abs_filepath):
        return f'Error: File not found or is not a regular file: "{filepath}"'

    try:
        with open(abs_filepath, "r") as file:
            file_content = file.read(CHAR_LIMIT)
            if len(file.read()) > CHAR_LIMIT:
                return (
                    file_content
                    + f" [...File '{filepath}' truncated at {CHAR_LIMIT} characters]",
                )

            return file_content
    except Exception as e:
        return f"Error: {e}"
