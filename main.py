import subprocess
import os
import sys
import platform
import argparse

parser = argparse.ArgumentParser(description="Master Orchestrator")
parser.add_argument("--target", type=str, required=True, help="Username to scrape")
# Add more if needed, e.g., --count 10
args = parser.parse_args()

# Store the captured argument
TARGET_USER = args.target

TASKS = [
    {
        "folder": "instascraper",
        "script": "instascraper.py",
        "venv": "venv"
    },
    {
        "folder": "",
        "script": "geoclip-env/geoclip_pipeline.py",
        "venv": "geoclip_venv"
    },
    {
        "folder": "",
        "script": "geovisualise/geovisualise.py",
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
    base_dir = os.getcwd()
    work_dir = os.path.join(base_dir, TASKS[0]['folder'])
    venv_dir = os.path.join(base_dir, TASKS[0]['venv'])

    try:
        # 2. Find the SPECIFIC python version for this task
        python_exe = get_python_exe(venv_dir)
        print(f"    Using Interpreter: {python_exe}")

        command = [
            python_exe,      # The Python Interpreter
            TASKS[0]['script'],     # The Script
            "--target",      # The Argument Flag
            TARGET_USER   # The Value
        ]

        print(f"Running command: {command}")

        # 3. Run it
        subprocess.run(
            command, 
            cwd=work_dir, # Run inside the subfolder
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
    
    base_dir = os.getcwd()
    work_dir = os.path.join(base_dir, TASKS[1]['folder'])
    venv_dir = os.path.join(base_dir, TASKS[1]['venv'])

    try:
        # 2. Find the SPECIFIC python version for this task
        python_exe = get_python_exe(venv_dir)
        print(f"    Using Interpreter: {python_exe}")

        # 3. Run it
        # cwd=work_dir ensures the script runs "inside" its own folder
        subprocess.run(
            [python_exe, TASKS[1]['script']], 
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
    
    base_dir = os.getcwd()
    work_dir = os.path.join(base_dir, TASKS[2]['folder'])
    venv_dir = os.path.join(base_dir, TASKS[2]['venv'])

    try:
        # 2. Find the SPECIFIC python version for this task
        python_exe = get_python_exe(venv_dir)
        print(f"    Using Interpreter: {python_exe}")

        # 3. Run it
        # cwd=work_dir ensures the script runs "inside" its own folder
        subprocess.run(
            [python_exe, TASKS[2]['script']], 
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