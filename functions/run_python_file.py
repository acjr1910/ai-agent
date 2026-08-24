import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the actual file, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "The list of args for that file execution",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]
        if args:
            command.extend(args)
        process = subprocess.run(
            command, timeout=30, text=True, capture_output=True, cwd=abs_working_dir
        )
        output = ""

        if process.returncode != 0:
            output += f"Process exited with code {process.returncode}\n"
        if not process.stderr and not process.stdout:
            output += "No output produced\n"
        if process.stdout:
            output += f"STDOUT: {process.stdout}"
        if process.stderr:
            output += f"STDERR: {process.stderr}"
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
