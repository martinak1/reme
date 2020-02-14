#!/usr/bin/env python3

from subprocess import Popen, PIPE

output, err = Popen(["pip","list"], stdout=PIPE, stderr=PIPE)

if "reme" in found:
    print("Reme has been located")
else:
    print("Reme has not been installed")
    exit(1)

help_dock = subprocess.check_output(["reme", "-h"]).decode('utf-8')