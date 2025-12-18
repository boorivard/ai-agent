import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        #get working path, target directory, and check to see if target directory is valid
        working_dir_abs = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target = os.path.commonpath([working_dir_abs, target]) == working_dir_abs

        if not valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target.endswith('py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target]

        if args:
            command.extend(args)

        completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_string = ""

        if completed_process.returncode != 0:
            output_string += f"Process exited with code {completed_process.returncode}"
        if not completed_process.stderr  and not completed_process.stdout:
            output_string += "No output produced"
        else:
            if completed_process.stdout:
                output_string += f"STDOUT: {completed_process.stdout}\n"
            if completed_process.stderr:
                output_string += f"STDERR: {completed_process.stderr}\n"

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"