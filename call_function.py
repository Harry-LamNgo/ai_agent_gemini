from google.genai import types
from collections.abc import Callable

from config import WORK_DIR
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file


# This is where all schemas of function store
# --> To organize the import function for main.py - having them gathered in one place is cleaner than scattering imports across files

# types.Tool from google.genai is a wrapper container that groups all FunctionDeclaration together
# generate_content does not accept raw list of FunctionDeclaration object --> it needs Tool

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, 
                           schema_write_file, schema_run_python_file]
)

# Create a dictionary of function (function_map) - this dict can help you to fast get the value (in this case is function) according to the key
# -> you can expand more functions in the future - without dict, you have to write at least 4 (more if there are more functions) if ... elif ... with the same pattern
# --> dict can give you the way to look up fast ------>> function_map[function_name](**args)
function_map: dict[str, Callable[..., str]] = {"get_file_content": get_file_content, "get_files_info": get_files_info
                                                , "write_file": write_file, "run_python_file": run_python_file}


def call_function(
        function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )],
        )
    
    # Create a shallow copy of args of function_call and named it args if function_call.args is NONE then args is empty dict {}
    args = dict(function_call.args) if function_call.args else {}

    ## Fixed Working Directory to ./calculator --> Whenever need change need to go to call_function.py to change <---- Misuse feature of call_function.py (Not recommend)
    # args["working_directory"] = "./calculator"

    # Better approach --> Create a global variable where users can config that affect whole system  --> Config.py is where to users manual change their configs
    # -> Import that variable from config.py
    args["working_directory"] = WORK_DIR

    function_result :str = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=function_name,
            response={"result": function_result}
        )],
    )