#!/usr/bin/env python3

import subprocess

found = subprocess.check_output(["pip","list"]).decode('utf-8')

if "reme" in found:
    print("Reme has been located")
else:
    print("Reme has not been installed")
    exit(1)