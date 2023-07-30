### How do I get set up?
- Summary of set up
  * create postgres database
  * create virtualenv for running this project with python version 3.6
  * going to project directory [utcc-secret-photo]
  * running command to install library : 
    ```
    pip install -r requirement.txt
    ```
  * create ".env" file in project directory to set environment variable for this project (can you follow in "env_example" file)
  * running command to create database table for this project by: 
    ```
    python manage.py migrate secret_photo
    ```
  * running command to crate default database table of Django Framework by: 
    ```
    python manage.py migrate
    ```
  * runserver by running command :
    ```
    python manage.py runserver:{port}
    ```