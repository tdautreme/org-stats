# What we need to run org-stats
- Python 3.6.8 https://www.python.org/downloads/release/python-368/
- PyGitHub and Art, install by running `pip install -r requirements.txt`.

# How to run it
```
usage: org-stats.py [-h] [-o ORG] [-u USERNAME] [-p PASSWORD] [-t ACCESS_TOKEN]

optional arguments:
  -h, --help            show this help message and exit
  -o ORG, --org ORG     GitHub target organization name
  -u USERNAME, --username USERNAME
                        Your GitHub username (Optional)
  -p PASSWORD, --password PASSWORD
                        Your GitHub password (Optional)
  -t ACCESS_TOKEN, --access-token ACCESS_TOKEN
                        Your GitHub access token (Optional)
                        
Exemple:
python3 org-stats.py -o Undefined-Team -u tdautreme -p this_is_my_password
python3 org-stats.py -o Undefined-Team -t my_secret_access_token
python3 org-stats.py -o Undefined-Team
```
# Why give username and password or access token?
You have to give your GitHub username and password or access token only if you want to show private organizations repos you have access to.

# What does it look like
![Example](https://i.ibb.co/ZHgMG7V/Pres.png)
