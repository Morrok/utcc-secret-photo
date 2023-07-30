### How do I get set up?
- Summary of set up
  * create postgres database
  * create virtualenv for running this project with python version 3.6
  * going to project directory [utcc-secret-photo]
  * install library by running command: 
    ```
    pip install -r requirement.txt
    ```
  * create ".env" file in project directory to set environment variable for this project (can you follow in "env_example" file)
  * create database table for this project by running command: 
    ```
    python manage.py migrate secret_photo
    ```
  * crate default database table of Django Framework by running command: 
    ```
    python manage.py migrate
    ```
  * runserver by running command :
    ```
    python manage.py runserver:{port}
    ```