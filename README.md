# Ecommerce API

REST API for Ecommerce website according to the requirements in the assignment.

## Quick Start

To get this project up and running locally on your computer:


* Set up the Python development environment.
   > **Note:** I want to recommend using a Python virtual environment.
   
* Create .env file in the project root directory and create variables used in settings.py.


* Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or `py -3` instead of `python` to start Python):
   ```
   pip3 install -r requirements.txt
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py createsuperuser # Create a superuser
   python3 manage.py runserver
   ```
  

* Open a browser to `http://127.0.0.1:8000.`
 

* Admin Site: `http://127.0.0.1:8000/admin`


* Create Staff Users, Department, Prdouct Categeory and Customer Category.


* Import this url in POSTMAN Desktop App and Test API.
https://www.getpostman.com/collections/f605154cffe574c41732


## Containerization(Docker)
```
sudo docker build --tag python-django .
sudo docker run --publish 8000:8000 python-django
```
