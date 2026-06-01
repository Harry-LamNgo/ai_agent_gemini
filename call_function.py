from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

# This is where all schemas of function store
# --> To organize the import function for main.py - having them gathered in one place is cleaner than scattering imports across files

# types.Tool from google.genai is a wrapper container that groups all FunctionDeclaration together
# generate_content does not accept raw list of FunctionDeclaration object --> it needs Tool

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, 
                           schema_write_file, schema_run_python_file]
)