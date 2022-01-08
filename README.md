Ensure that versions are specified in pip requirements files
------------------------------------------------------

# Purpose

A GitHub action to check the pip requirements file.

## Requirements file validity
If a pip requirements file is present, we ensure that all versions are specified.  The requirements file should sit at the root of the repository and may be named
* requirements.txt
* requirement.txt

An example of a valid file is 

```
# My requirements file
astroid==2.8.3
certifi==2021.10.8  # We need this for reason x.
```

An invalid file would be

```
# My requirements file.  It's invalid because versions are not specified.
astroid
certifi==2021.10.8  # We need this for reason x.
```

It is permissible to use inequality specifications.  

## Requirements file presence

Currently, exactly one requirements file should be present and in the repo root.   

# Actions
The check is done with a python script.  If the check fails for any reason, the python script will terminate with a non-0 exit code, triggering the GitHub workflow to fail.
