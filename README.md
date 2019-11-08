# What we need to run org-stats
- Python 3.6.8 https://www.python.org/downloads/release/python-368/
- PyGithub 1.44.1 lib (pip3 install PyGithub==1.44.1) https://github.com/PyGithub/PyGithub
- art 4.2 lib (pip3 install art==4.2) https://github.com/sepandhaghighi/art

# How to run it
```
usage: test.py [-h] [-o ORG] [-u USERNAME] [-p PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  -o ORG, --org ORG     Github target organization name
  -u USERNAME, --username USERNAME
                        Your github username (Optional)
  -p PASSWORD, --password PASSWORD
                        Your github password (Optional)
                        
Exemple:
python3 org-stats -o Undefined-Team -u tdautreme -p this_is_my_password
python3 org-stats -o Undefined-Team
```
# Why give username and password ?
You have to give your github username and password to show private organizations repos you have access
