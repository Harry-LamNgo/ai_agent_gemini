import os

### ---------------------------------------
# You only need those lines of code when run project from subdir or not root dir of project -- because sys.path is not include the root dir project

# import sys
# # Get current path of file (pwd)
# directory = os.path.abspath(__file__)
# # get the parent folder of file --> using 2 times os.path.dirname -> 1st: get dirname -> 2nd: dirname of the dirname in 1st
# parent_dir = os.path.dirname(os.path.dirname(directory))
# # Add the path to sys path list to impor file or functions
# sys.path.append(parent_dir)
### ---------------------------------------

from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_work_dir, file_path))
        if os.path.commonpath([abs_work_dir, abs_file_path]) != abs_work_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path, "r") as f:
            file_content_str = f.read(MAX_CHARS)
            
            # After reading MAX_CHARS, check if there is at least 1 more character in file content
            # if yes, f.read(1) return a string -> True -> combine already read content with the annoucment "truncated"
            # if no,  f.read(1) retrun empty string -> False -> DO NOT combine the annoucement "truncated"

            if f.read(1):
                file_content_str += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_str
    except Exception as e:
        return f'Error: {e}'
        

## Reason of MAX_CHARS and if f.read(1)
# limit the content of files that chatbot read --> if it read too much information --> mean spend more token API --> Free tier hit the limit