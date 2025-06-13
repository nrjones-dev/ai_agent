import os
import subprocess


def run_python_file(working_directory, filepath):
    abs_working_dir = os.path.abspath(working_directory)
    abs_filepath = os.path.abspath(os.path.join(abs_working_dir, filepath))

    if not abs_filepath.startswith(abs_working_dir):
        return f'Error: Cannot execute "{filepath}" as it is outside the permitted working directory'
    if not os.path.exists(abs_filepath):
        return f'Error: File "{filepath}" not found.'
    if not filepath.endswith(".py"):
        return f'Error: "{filepath}" is not a Python file.'

    try:
        args = ["python3", abs_filepath]
        result = subprocess.run(
            args, capture_output=True, timeout=30, text=True, cwd=abs_working_dir
        )
        result_output = []

        if result.stdout:
            result_output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            result_output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            result_output.append(f"Error: process exited with code {result.returncode}")

        return "\n".join(result_output) if result_output else "No output produced."
    except Exception as e:
        return f"Error: executing python file: {e}"
