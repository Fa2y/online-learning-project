# olp
Bachelor Project (soutenance):Webapp to help online learning

## Instructions to run (Linux, python3):
- Make a virtual enviroment `python -m venv .` .
- Install the requirements using pip `pip install -r requirements.txt` .
- run migrations
```bash
$ python manage.py makemigrations
...
$ python manage.py migrate
```
- run server (port 8000)
```bash
$ python manage.py runserver
```
- To access admin side (/admin) you need an admin account, to make an admin account:
```bash
$ python manage.py createsuperuser
```
- To populate the database with a sample quizz (For this operation to run we need a user with the username "fa2y" or you can simply edit the python file "DB-Populate.py" with the suitable username)
```bash
$ python manage.py shell
>>> run DB-Populate.py
```

