### How do I get set up?
- Summary of set up
  * create postgres database
  * create virtualenv for running this project with python version 3.6
  * going to project directory [utcc-secret-photo]
  * running command to install library : 
    ```
    pip install -r requirement.txt
    ```
  * create .env file in project directory to set environment variable for this project (can you follow in env_example file)
  * running command create initial table for this project: 
    ```
    python manage.py migrate secret_photo
    ```
  * running command to migrate defualt table of Django Framework: 
    ```
    python manage.py migrate
    ```
  * runserver by running command :
    ```
    python manage.py runserver:port
    ```