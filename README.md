# MemoryCards
MemoryCards is a website that aids in memorization with the help of flashcards. The website allows the creation and sharing of decks of cards, 
while also controlling how often users need to review certain cards in a specific deck to improve retention.

## The website supports
1. User created decks of cards to memorize
2. Sharing decks
3. Saving your favourite decks for simpler access
3. Reviewing cards based on the [SM2](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2) algorithm
4. MathJax

## Install
1. Clone this repository: https://github.com/ggasper/MemoryCards.git
2. Navigate into the `memorycards` directory
3. Install the python packages using `requirements.txt`.
   This is done with the command `pip install -r reqirements.txt`. It's also recommended that you install the packages inside a virtual environment like `venv`.
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
6. Finally, start the server.
   ```bash
   python manage.py runserver.py
   ```
