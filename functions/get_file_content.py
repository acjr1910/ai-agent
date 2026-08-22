import os
from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        is_target_file_path = (
            os.path.commonpath([abs_working_dir, target_file_path]) == abs_working_dir
        )
        is_file = os.path.isfile(target_file_path)

        if not is_target_file_path:
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not is_file:
            f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            if f.read(1):
                file_content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
