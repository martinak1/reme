#!/usr/bin/env python3

"""
Exit Codes

    1 - Reme not found in pip list ie it has not been installed correctly
    2 - Pip list exited with a non zero code ie something went wrong calling pip
    3 - Calling reme -h exited with a non zero code ie something went wrong calling reme
"""

import subprocess
from reme.reme import Reme

# check if pip recognizes reme as being installed
try:
    output = subprocess.run("pip list", capture_output=True, shell=True, encoding="utf-8")

    if not output.check_returncode() and "reme" in output.stdout:
        print("Reme has been located in Pip output")
    else:
        print(f"\nReme has not been installed. This is what was returned: \n\n{output.stdout}")
        exit(1)

except subprocess.CalledProcessError as e:
    print(f"Pip closed with a non zero code -> {e}")
    exit(2)

# Try to call reme to print the help docstring
try: 
    output = subprocess.run("reme -h", capture_output=True, shell=True)
    output.check_returncode()
    print("Reme helpdoc was printed without error")
    print("Build was successfull")

except subprocess.CalledProcessError as e:
    print(f"Reme closed with a non zero code -> {e}. \nThis is what was returned: \n\n{output.stdout}")
    exit(3)
