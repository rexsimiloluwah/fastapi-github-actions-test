# Introduction 
This is the reference Github repository for my recent blog post on [Master CI/CD Fundamentals using FastAPI, Github Actions, and Heroku]()

##  :beginner: About
This is a simple CRUDL API using FastAPI for managing a user's bucket list. An SQLite database was used for persistence via an SQLAlchemy ORM. The primary objective of this repo is to help beginners learn CI/CD with Github actions, Heroku, and unit testing. 

## :zap: Usage
###  :electric_plug: Installation
- Clone the Github repository 
- Create a virtual environment 
- Install the dependencies from the `requirements.txt` file 
```bash
$ pip install -r requirements.txt 
```
- Create a `.env` file and add your `JWT_SECRET_KEY` variable

###  :electric_plug: Run tests using pytest 
> The unit tests are available in the `src/tests` folder.
```bash
$ pytest 
```

### :zap: Run the app 
```bash 
$ cd src && python main.py
```
The application can be accessed on http://localhost:5000 

### :notebook: Documentation 
Go to http://localhost:5000/docs

>Other necceary information can be found in the blog post, Thanks for Reading!
