import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        abs_target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))
        if os.path.commonpath([abs_work_dir, abs_target_file]) != abs_work_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted directory'
        
        if os.path.isdir(abs_target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # To ensure that all parent dir of file_path exist -> Using os.path.dirname to get the parent dir name
        # Then check if parent dir of target file exist --> if NOT, then create the parent dir -> ensure program not crash
        parent_dir_target_file = os.path.dirname(abs_target_file)
        os.makedirs(parent_dir_target_file, exist_ok=True)

        with open(abs_target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {e}'