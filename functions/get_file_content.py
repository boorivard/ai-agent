import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        #get working path, target directory, and check to see if target directory is valid
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
            
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        #open and read a maximum of 10000 characters from the file
        with open(target_dir, "r") as f:
            file_content = f.read(MAX_CHARS)
            #if file was truncated, add message at the end of returned string        
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content
    
    except Exception as e:
        return f"Error: {e}"
