import os
import subprocess

def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_work_dir, file_path))
        if os.path.commonpath([abs_work_dir, abs_file_path]) != abs_work_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", abs_file_path]
        if args != None and len(args) != 0:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=abs_work_dir, capture_output=True , text=True, timeout=30)

        output_string: list[str] = []
        if completed_process.returncode != 0:
            output_string.append(f'Process exited with code {completed_process.returncode}')
        if completed_process.stdout == "" and completed_process.stderr == "":
            output_string.append(f'No output produced')
        else:
            if completed_process.stdout != "":
                output_string.append(f'STDOUT: {completed_process.stdout}')
            if completed_process.stderr != "":
                output_string.append(f'STDERR: {completed_process.stderr}')
        
        return "\n".join(output_string)
    except Exception as e:
        return f'Error: executing Python file: {e}'