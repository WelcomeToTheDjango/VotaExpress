# VotaExpress

This is a repository for a web application that permits you to create polls in realtime

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

> By default the `http://127.0.0.1:8000` will be used for live your server, but you can change it typing the port that you want in the end of the command.

```pip
python3 manage.py runserver <port-number>(optional)
```

## Tests (Optional)

> You don't need it for start using but we care about tests and we write a lot for keep a controlled environment.

```bash
python3 manage.py test
```

## Loading Pre-Database (Optional)

> If you're looking for an example dataset, you can easily import a fixture to fill up the database.

```bash
python3 manage.py loaddata initdata.json
```

## Using Tailwind for Development

You need to have node installed, checkout the [node documentation]("https://nodejs.org/en")

The package.json includes tailwind, you can install it with
```bash
npm i
```
for run tailwind you can use the next command

```bash
npm run tailwind
```