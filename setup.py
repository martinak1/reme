import pathlib
from setuptools import setup

# Get the dir housing the files
cwd: str = str(pathlib.Path(__file__).parent)
readme: str = f"{cwd}/README.md"

setup(
    name="reme",
    version="1.0.0",
    description="A Discord bot that reminds you of things",
    long_description=readme,
    url="https://github.com/martinak1/reme",
    author="martinak1",
    license="BSD-3-Clause",
    classifiers=[
        "License :: OSI Approved :: BSD 3 Clause License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    packages=["reme"],
    include_package_data=True,
    install_requires=["discord>=1.3.1"],
    entry_points={
        "console_scripts": ["reme=reader.__init__:main"]
    },
)