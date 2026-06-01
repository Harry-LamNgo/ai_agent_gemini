import os
import subprocess
from google.genai import types

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
        if args is not None and len(args) != 0:     # can use "if args:" due to Python treats both None and [] as falsy -- this is better because it's not care about order (always put the null check first)
            command.extend(args)
        
        '''
        ## rule for run_python_file:
        1. only allow the LLM to run code in a specific dir (working_directory == abs_work_dir)
            ---> cwd = abs_work_dir
        2. use a 30-second timeout to prevent it from running indefinitely
            ---> timeout = 30

        subprocess.run properties:
        args = command (the input positional arguments), cwd=abs_work_dir (set the dir the subprocess runs in)
        capture_output = True (tell python to capture both stdout and stderr from subprocess to use them)
        text = True (by default, subprocess return raw bytes - this setting decodes the output to strings using the default encoding -- usually UTF-8)
        '''

        completed_process = subprocess.run(command, cwd=abs_work_dir, capture_output=True , text=True, timeout=30)

        output_string: list[str] = []
        if completed_process.returncode != 0:
            output_string.append(f'Process exited with code {completed_process.returncode}')
        if completed_process.stdout == "" and completed_process.stderr == "":
            output_string.append(f'No output produced')
        if completed_process.stdout:
            output_string.append(f'STDOUT: {completed_process.stdout}')
        if completed_process.stderr:
            output_string.append(f'STDERR: {completed_process.stderr}')
        
        return "\n".join(output_string)
    except Exception as e:
        return f'Error: executing Python file: {e}'
    

# Schema of run_python_file

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified python file within a specified working directory, catching errors and console output with a strict 30-second execution timeout",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path or filename of the Python file to execute",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments. Omits if none are needed"
            ),
        },
        required=["file_path"],
    )
    
)