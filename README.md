Ensure Versions in Pip Requirements Files
------------------------------------------------------

## Purpose

Implement a GitHub action that checks the pip requirements file.

### Behavior
The GitHub action runs in a docker container that executes the Python script `main.py`.  If the check fails for any reason, the script will terminate with a non-0 exit code, triggering the GitHub workflow to fail.

### Requirement File Presence

Currently, the job fails unless exactly one requirements file is present.  The file should be in the root of the repository and may be named
* requirements.txt
* requirement.txt
  
This conforms with the location of the file in the SFL template.  If the project does not require the requirements file, the action can be ignored or disabled.

### Requirement File Validity
If a pip requirements file is present, we ensure that all versions are specified.  
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

   

