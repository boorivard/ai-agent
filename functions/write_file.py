import os

def write_file(working_directory, file_path, content):
    try:
        #get working path, target directory, and check to see if target directory is valid
        working_dir_abs = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target = os.path.commonpath([working_dir_abs, target]) == working_dir_abs

        if not valid_target:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target), exist_ok=True)

        with open(target, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"