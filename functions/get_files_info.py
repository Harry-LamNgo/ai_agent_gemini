import os
from google.genai import types

def get_files_info(working_directory: str, directory: str=".") -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

        # using commonpath to check the target_dir is within the abs_working_dir --> check target_dir valid
        # compare them to return TRUE or FALSE
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir


        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        print(f'Success: "{directory}" is within the working directory')
        result_list: list[str] = []

        # ** If using os.listdir --> the return of this is a list of files exist in target dir --> we need to use .join to combine the target_dir path and filename
        ## --> This create a complete file_path for us to use OS.PATH.GETSIZE and OS.PATH.ISDIR

        # list_files = os.listdir(target_dir)
        # print(list_files)
        
        # for file in list_files:
        #     file_path = "/".join([target_dir, file])
        #     result_line = f" - {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}"
        #     result_list.append(result_line)
   
        

        # ** If using os.scandir --> the return of this is an object with information of file in target dir --> we need write write code using with (recommend for easy template)
        ## --> We can directly use the methods and properties of that object. However, you need understand clearly how to call them

        # entry_files = os.scandir(target_dir)
        # print(entry_files)

        with os.scandir(target_dir) as entries:
            for entry in entries:
                result_line = f' - {entry.name}: file_size={entry.stat().st_size}, is_dir={entry.is_dir()}'
                result_list.append(result_line)
        return "\n".join(result_list)
       

    except Exception as e:
        return f"Error: {e}"
    

# Schema of get_files_info

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)