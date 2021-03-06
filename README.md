# Yamdb API
Project with titles, scores, and reviews for it. Auth by jwt.

#### Stack: 
Python 3, Django 2.2, DRF, PyJWT

## How start project:

Clone a repository and go to command line:

```sh
git clone https://github.com/menyanet73/api_yamdb.git
```

```sh
cd api_yamdb
```

Create and activate virtual environment:

```sh
python3 -m venv env
```
For Windows:
```sh
source env/Scripts/activate  
```
For Linux:
```sh
source env/bin/activate  
```

Install dependencies from a file requirements.txt:

```sh
python3 -m pip install --upgrade pip
```

```sh
pip install -r requirements.txt
```

Apply migrations:


```sh
cd api_yamdb
```

```sh
python3 manage.py migrate
```

Start project:

```sh
python3 manage.py runserver
```

### Documentation of API will be aviable in
```sh
127.0.0.1:8000/redoc/
```
