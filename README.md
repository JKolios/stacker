Stacker
====================

Opens iTerm tabs and connects via SSH to all instances in an AWS Opsworks stack.
Requires a recent OSX version, Python2 and iTerm.

Installation
---------------------

- pip install -r requirements.txt
- aws configure (Opsworks seems to require region: us-east-1 to work)
- edit conf.json as needed

Usage
---------------------

$ python stacker.py STACK_NAME [COMPONENT_SUBSTRING]
