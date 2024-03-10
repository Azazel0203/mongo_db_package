import os
from pathlib import Path

package_name = "mongodb_connect"

list_of_files=[
    ".github/workflows/ci.yaml",
    "src/__init__.py",
    f"src/{package_name}/__init__.py",
    f"src/{package_name}/mongodb_crud.py",
    "tests/__init__.py",
    "tests/unit/__init__.py", # unit testing
    "tests/unit/unit.py", # for test cases
    "tests/integration/__init__.py", 
    "tests/integration/int.py", # for integration tests
    "init_setup.sh",
    "requirements.txt", # this will be installed on the user side
    "requirements_dev.txt", # this will be the ting to install for development side
    "setup.py",
    "setup.cfg",
    "pyproject.toml",
    "tox.ini",
    "experiment/experiments.ipynb"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass # create an empty file