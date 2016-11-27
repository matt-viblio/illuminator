illuminator
===========

Vizualization tools for film scripts.

Local Development Notes
=======================

To locally develop:

1. Install Python's virtual environment tools: `sudo pip install virtualenv`'

2. Create a Python virtual environment: `virtualenv env`

3. Enter the environment: `source env/bin/activate`

4. Install dependencies into local environment: `pip install -r requirements.txt`

5. Install a local copy of PostgreSQL and follow the database notes below to clone the production database and get the data locally (these instructiions will only work if you are me).

Push Changes to Heroku
======================

Assuming you've previously set up git ass described at: https://devcenter.heroku.com/articles/git

Just run: `git push heroku heroku_deploy:master`

Otherwise first run:

```
heroku git:remote -a illuminator
```


Database Notes
==============

Docs on this:

https://devcenter.heroku.com/articles/heroku-postgres-import-export

We user Heroku's postgres services, and a postgres database for local development.

To back up locally the contents of the master database on Heroku, run:

```
heroku pg:backups capture --app illuminator
curl -o idb.backup `heroku pg:backups public-url --app illuminator`
```

To restore the contents of a backup to the local Postgres database, if there is already a `idb` schema that `djangouser` has access to, run:


```
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U djangouser -d idb idb.backup
```

If not you will first need to create one:

```
psql -U postgres
(postgres user password is 'password' on my machine)
CREATE USER djangouser PASSWORD 'djangouser';
(Note - the create user command is case sensitive because duh...)
CREATE DATABASE idb OWNER djangouser;
```

You can connect to the database as `djangouser` via the `psql` command line:

```
psql -h localhost -U djangouser idb
```


