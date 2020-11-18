# CS50 Study

This is CS50 Study - a question bank application that will help you learn the CS50 material.

### Sign Up

To access the CS50 Study, you need to create a new user account. During registration, you must provide:
- a username, 
- an email,
- a password.

## Sign In

Once you have created a user account, you can sign in to start using the application. To sign in, you need to type your email and password provided during registration.  

### Questions

Once you have logged in, you can view the questions in the question bank and start learning. For each question, you can view:
- the answer, 
- the question category and difficulty, 
- who added the question to the question bank and when.

You can **view** and **edit** the existing questions, as well as **add** new questions. 

To add a new question, you need to provide the following information:
- the question,
- the answer to your question, 
- the difficulty of the question (easy, medium or difficult),
- the appropriate question category. 

### Categories

Each question belongs to a particular category. The list of categories includes:
1. General
2. Scratch
3. C
4. Python
5. SQL
6. HTML
7. CSS
8. JavaScript
9. Algorithms
10. Data Structure

### Searching

CS50 Study also provides search functionality that offers the users a way to quickly find relevant content.  

### Sign Out

Once you have finished using the CS50 Study, you can sign out.


## Setup for Local Development

### Tech Stack

The tech stack includes the following:

* **Python3** and **Flask** - the server language and server framework
* **SQLAlchemy ORM** - the ORM library
* **PostgreSQL** - the database
* **Flask-Migrate** - for creating and running schema migrations
* **HTML**, **CSS** and **JavaScript** - the technologies used to create the frontend

### Installing Dependencies

#### Python 3

Follow instructions to install the latest version of Python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PostgreSQL

Follow instructions to install the latest version of [PostgreSQL](https://www.postgresql.org/download/) for your platform

#### Virtual Environment

It is recommended to work within a virtual environment. This keeps the dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

If you are using Python 3.3 or newer, the `venv` module is the preferred way to create and manage virtual environments. `venv` is included in the Python standard library and requires no additional installation.
To create a virtual environment using `venv`, navigate to the root directory and run:
```bash
python3 -m venv venv
. venv/bin/activate
```
The `venv` folder should be added to `.gitignore`.

#### PIP Dependencies

Install dependencies by navigating to the root directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

### Running the server locally

To run the server, execute from within the root directory:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

### Database Local Setup
With PostgreSQL running, restore a database using the `cs50.psql` file provided. From the root directory in the Terminal run:
```bash
dropdb --if-exists cs50
createdb cs50
psql cs50 < cs50.psql
```

## Testing locally
To run the tests, execute from within the root directory:
```
dropdb --if-exists cs50_test
createdb cs50_test
psql cs50_test < cs50.psql
python test_app.py
```
The `HtmlTestRunner` package is used to generate human-readable HTML test reports showing the results of the tests of the CS50 Study. 
The HTML test reports from different test runs can be found in the `test-results` directory.

## CS50 Study API

The CS50 Study API includes the following endpoints:

- POST /register
- POST /login
- GET /logout
- GET /questions
- GET /questions/`<int:question_id>`
- POST /questions/add
- PATCH /questions/`<int:question_id>`/edit
- POST /questions/search
- GET /categories


## Error Handling

The CS50 Study API will return the following error types when requests fail: 
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 405: Method Not Allowed
- 409: Conflict
- 422: Unprocessable Request