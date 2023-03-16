from setuptools import setup

setup(
    name="pymirage",
    version="0.1.0",
    author="Shubham Singh",
    author_email="geekysubham@gmail.com",
    description="A virtual environment management tool with in Maya",
    long_description="PyMirage is a command-line tool for creating and managing virtual environments for Python projects.",
    url="https://github.com/imsubhamsingh/mirage",
    packages=["pymirage"],
    entry_points={
        "console_scripts": [
            "pymirage=pymirage.cli:main",
        ],
    },
)
