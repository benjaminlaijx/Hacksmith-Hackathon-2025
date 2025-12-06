import subprocess
import os
import sys
import platform

TASKS = [
    {
        "folder": "instascraper",
        "script": "instascraper.py",
        "venv": "venv"
    },
    {
        "folder": "geoclip-env",
        "script": "geoclip_pipeline.py",
        "venv": "geoclip-env"
    },
    {
        "folder": "geovisualise",
        "script": "geovisualise.py",
        "venv": "venv"
    }
]

def get_python_exe(venv_path):
    """
    Returns the path to the python executable inside a venv,
    handling Windows vs Mac/Linux differences.
    """
    if platform.system() == "Windows":
        exe_path = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        # Mac / Linux
        exe_path = os.path.join(venv_path, "bin", "python")
    
    if not os.path.exists(exe_path):
        raise FileNotFoundError(f"Python interpreter not found at: {exe_path}")
    
    return exe_path

def run_pipeline():
    for task in TASKS:        
        # 1. Build full paths
        # We assume the folder is in the same directory as this master script
        base_dir = os.getcwd()
        work_dir = os.path.join(base_dir, task['folder'])
        venv_dir = os.path.join(base_dir, task['venv'])

        try:
            # 2. Find the SPECIFIC python version for this task
            python_exe = get_python_exe(venv_dir)
            print(f"    Using Interpreter: {python_exe}")

            # 3. Run it
            # cwd=work_dir ensures the script runs "inside" its own folder
            subprocess.run(
                [python_exe, task['script']], 
                cwd=work_dir,  
                check=True
            )

        except FileNotFoundError as e:
            print(f"    !!! ERROR: {e}")
            return # Stop pipeline
        except subprocess.CalledProcessError as e:
            print(f"    !!! ERROR: Script crashed with code {e.returncode}")
            return # Stop pipeline
        except Exception as e:
            print(f"    !!! Unexpected Error: {e}")
            return

    print("\n--- PIPELINE FINISHED ---")

run_pipeline()