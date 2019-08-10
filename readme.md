# MemoryCards
MemoryCards is a website which helps with learning using one of the spaced repetition algorithms. 
It allows its users to create decks of cards which they can then review. The website itself chooses which cards the user needs to review,
to improve retention.

## The website supports:
1. User created decks of cards to memorize
2. Viewing other peoples decks
3. Reviewing cards based on the [SM2](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2) algorithm

## Install
1. Clone this repository: https://github.com/ggasper/MemoryCards.git
2. Navigate into the `memorycards` directory
3. Create a new virtual environment using the `requirements.txt`.
   This is done with the command `pip install -r reqirements.txt`.
4. Setup the PostgreSQL database:
   * Install PostgreSQL as specified for your system. 
   * Run the following SQL commands to setup the server database:
	 ```sql
		CREATE DATABASE memorycards;
		CREATE USER memorycardsuser WITH PASSWORD 'password';
		ALTER ROLE memorycardsuser SET client_encoding TO 'utf8';
		ALTER ROLE memorycardsuser SET timezone TO 'UTC';
		ALTER ROLE memorycardsuser SET default_transaction_isolation TO 'read committed';
		GRANT all PRIVILEGES ON DATABASE memorycards TO memorycardsuser;
	 ```
5. Run all server migrations from inside the `memorycards` directory.
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Finally start the server.
   ```bash
   python manage.py runserver.py
   ```
