import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

        is_target_dir_valid = (
            os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
        )

        if not is_target_dir_valid:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        for item in os.listdir(target_dir):
            path = os.path.join(target_dir, item)
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            print(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return

    except Exception as e:
        return f'Error: "{e}"'
