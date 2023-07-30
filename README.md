### How do I get set up?
- Summary of set up
  ** create virtualenv for running this project with python version 3.6
  ** going to project directory
  ** running command : pip install -r requirement.txt
  ** create .env file in project directory
  *** can you follow in env_example file
  ** running command : python manage.py migrate secret_photo
  *** Database should be created first before run migrate
  ** running command : python manage.py migrate
  \*\* runserver by running command : python manage.py runserver:port