import sqlite3
import random
import names

# Connessione o creazione del database SQLite
conn = sqlite3.connect('SQLite/people.db')

try:
    # Creazione del cursore
    cursor = conn.cursor()

    # Creazione di una tabella
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # Generazione e inserimento di dati
    for _ in range(10):
        name = names.get_full_name()
        age = random.randint(18, 80)
        email = name.lower().replace(" ", ".") + "@example.com"
        cursor.execute("INSERT INTO people (name, age, email) VALUES (?, ?, ?)", (name, age, email))

    conn.commit()

except sqlite3.Error as e:
    print("Errore durante l'interazione con il database SQLite", e)
finally:
    if conn:
        conn.close()
        print("Connessione al database SQLite chiusa")

