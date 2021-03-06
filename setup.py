#!/usr/bin/env python3

import pathlib
from setuptools import setup

# Get the dir housing the files
cwd = pathlib.Path(__file__).parent
readme = (cwd / "README.md").read_text()

setup(
    name="reme",
    version="1.0.3",
    description="A Discord bot that reminds you of things",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/martinak1/reme",
    author="martinak1",
    author_email="abc000100100011@gmail.com",
    license="BSD-3-Clause",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Chat",
        "Topic :: Games/Entertainment"
    ],
    packages=["reme"],
    include_package_data=True,
    install_requires=["discord.py>=1.3.1"],
    entry_points={
        "console_scripts": [
            "reme=reme.__main__:main"
        ]
    },
)
