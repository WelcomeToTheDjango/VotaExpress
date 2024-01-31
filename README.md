# VotaExpress

## Create virtual environment

```bash
python3 -m venv venv
```

## Activate virtual environment
 
```bash
source venv/bin/activate
```

## Installing dependencies

```pip
pip3 install -r requirements.txt
```

## Creating a .ENV file

> For security reasons we don't disponibilize our SECRET_KEY here, but you can create your .env file in the root of the project using:

```bash
echo SECRET_KEY="your-secret-here" > .env
```

## Migrating data to the Database

> For now, we are using `db.sqlite3` for development purposes, when you run this command all migrations will be applied.

```bash
python3 manage.py migrate
```

## Starting server

> By default the `localhost:8000` will be used for live your server, but you can change it typing the port that you want in the end of the command.

```pip
python3 manage.py runserver <port-number>(optional)
```

## Tests (Optional)

> You don't need it for start using but we care about tests and we write a lot for keep a controlled environment.

```bash
python3 manage.py test
```

## Loading Pre-Database (Optional)

> If you need a example data, you can simply import a fixture that will populate the database.

```bash
python3 manage.py loaddata initdata.json
```
