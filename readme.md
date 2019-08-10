```sql
CREATE DATABASE memorycards;
CREATE USER memorycardsuser WITH PASSWORD 'password';
ALTER ROLE memorycardsuser SET client_encoding TO 'utf8';
ALTER ROLE memorycardsuser SET timezone TO 'UTC';
ALTER ROLE memorycardsuser SET default_transaction_isolation TO 'read committed';
GRANT all PRIVILEGES ON DATABASE memorycards TO memorycardsuser;
```

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver.py
```
