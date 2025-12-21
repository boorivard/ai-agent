import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        #get working path, target directory, and check to see if target directory is valid
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        #create list of content in target directory
        target_dir_contents = os.listdir(target_dir)
        files_info = []
        #iterate through each item and add a string of the name, size, and if it is a directory to a list
        for filename in target_dir_contents:
            filepath = os.path.join(target_dir, filename)
            files_info.append(f"- {filename}: file_size={os.path.getsize(filepath)}, is_dir={os.path.isdir(filepath)}")
        #return a joined list of all the items in the directory with newline as the delimiter
        return "\n".join(files_info)
    except Exception as e:
        return f"Error: {e}"
    


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