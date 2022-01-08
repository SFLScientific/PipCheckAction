"""Ensure every package version in a pip requirements file is specified.

Uses the package requirements-parser:
https://pypi.org/project/requirements-parser/

It is assumed that exactly one requirements file is in the root dir of the
repo, and is named either "requirements.txt" or "requirement.txt".

If no such file is found, we raise an error for these reasons:
 - If there is a requirements file, then the SFL template assumes it is
   in the root.
 - If a dev really wants a repo with NO requirements.txt file, they can
  always disable the check.

If more than one file is found, a NotImplementedError is raised.

Ryan Murphy @ SFL Scientific
"""

import glob
import sys

# Import requirements parser in a try block with a message to assist debugging.
try:
    import requirements
except Exception as e:
    print("Failed to import parser: check installation into docker image.")
    print(e)

# Constant: match requirements.txt or requirement.txt in repo root directory
REQUIREMENTS_GLOB = "requirement*.txt"


def main(requirements_glob=REQUIREMENTS_GLOB):
    """Search for a requirements.txt file, verify versions are specified.

    If the requirements file does not meet requirements, exit with
    return code 1.  Else return with return code 0.

    Args:
        requirements_glob (str): String to pass to glob.glob.  Specifies
                                 which matches should be considered a
                                 requirements.txt file.

    Raises:
        RuntimeError: if no requirements file is found
        NotImplementedError: if more than one requirement file is found
    """
    #
    # Search for a requirements file at repo root.
    #
    requirements_files = glob.glob(requirements_glob)

    # If one is found, store it in a variable
    if len(requirements_files) == 1:
        requirements_file = requirements_files[0]

    # If none are found, raise Runtime Error
    elif len(requirements_files) == 0:
        raise RuntimeError(
            "Neither requirements.txt nor requirement.txt found at repo root. Disable check if desired."
        )

    # If > 1 are found, raise not implemented error
    else:
        raise NotImplementedError(
            f"At least two requirements.txt files found: {requirements_files}"
        )

    #
    # Parse the requirements file and check for errors
    #
    with open(requirements_file, "r") as file_obj:
        # Iterate over requirements and check if they are valid.
        for requirement in requirements.parse(file_obj):
            if not requirement_is_valid(requirement):
                print("Requirement checker failed: specify all versions.")
                print(requirement.line)
                sys.exit(1)

    print("All lines of the requirement file passed.")


def requirement_is_valid(req):
    """Check whether versions are specified in the input.

    Args:
        req of type Requirements.
    """
    # Extract the version specifications
    specs = req.specs

    # If no specifications, return false
    if len(specs) < 1:
        print("No specification.")
        return False

    # For all specifications, make sure the version
    #  is specified and conforms to expectations of having digits and dots
    #  (e.g., version 42.1337)
    for spec in specs:
        # Pull out the version string, the second element of the spec.
        version_str = spec[1]
        valid = all(char.isdigit() or char == "." for char in version_str)
        if not valid:
            print(f"Unexpected specification string: {version_str}")
            return False

    return True


if __name__ == "__main__":
    main()
