"""
Reads a pip requirements.txt file and ensures that every package specified
is accompanied by version information.

Uses the package requirements-parser: 
https://pypi.org/project/requirements-parser/

Ryan Murphy @ SFL Scientific
"""

import os
import sys

# Import requirements parser in a try block to provide a better warning
# if failure occurs here.
try:
    import requirements
except Exception as e:
    print("Failed to import parser: check installation into docker image.")
    print(e)

def main(in_file):

    if os.path.exists(in_file):
        with open(in_file, "r") as fd:
            for requirement in requirements.parse(fd):
                if not req_is_valid(requirement):
                    print("requirements.txt checker failed")
                    sys.exit(1)
    else:
        raise FileNotFoundError(f"Specified file not found: {in_file}")

    print("Success")
 

def req_is_valid(req):
    specs = req.specs
    if len(specs) < 1:
        return False

    for spec in specs:
        version_str = spec[1]
        valid = all([c.isdigit() or c == "." for c in version_str])
        if not valid:
            return False

    return True
    

if __name__ == "__main__":
    print(os.getcwd())
    print(os.listdir())
    main("requirements.txt")
