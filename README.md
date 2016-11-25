# DATABASES PROJECT
Here we are creating a website for our databases project at the GUC.
We will be using python Django framework for creating this website.
And we will use MySQL as our database.

In the settings.py file specify your DB info username, pass, etc
I needed to install this package: python-mysqldb

## IMPORTANT NOTICE
1) Make sure you copy settings_default.py into a new file named settings.py in the same directory.

2) Then change the attributes inside the settings.py file to match your computer's.

-- Change in the following area:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'school_system',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '',
    }
}

### AND

DB_USERNAME = 'root'

DB_PASSWORD = 'root'

DB_NAME = 'school_system'

DB_HOST = 'localhost'

3) run the following commands:

open a terminal inside the projects main directory
```python
python manage.py makemigrations
python manage.py migrate
```
and finally run server to test
```python
python manage.py runserver
```

if you wish to create a super user for the admin interface

use:
```python
python manage.py createsuperuser
```
if you wish to create a new app
use:
```python
python manage.py startapp <appname>
```

## GIT COMMANDS
For the initial pull:
```git
git clone https://github.com/ameniawy/databases_project.git
```

if you want to create a new branch:
```git
git checkout -b <branch_name>
```

if you want to switch to another existing branch:
```git
git checkout <branch_name>
```

when you want to save your work and upload:
```git
git add --all or git add .
git commit -m "add your commit message here"
git push origin <your_branch_name>
```

### NEVER PUSH TO MASTER UNTIL CONSULTING TEAM MATES
