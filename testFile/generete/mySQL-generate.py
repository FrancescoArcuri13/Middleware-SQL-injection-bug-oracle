import mysql.connector
from mysql.connector import Error
import random
import names

try:
    # Connection to database
    connection = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='TestMiddleware',
        password='TestMiddleware'
    )

    if connection.is_connected():
        # New DB
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS peopleDB")
        cursor.execute("USE peopleDB")

        # Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS people (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT,
                email VARCHAR(255)
            )
        """)

        # Delete old data
        cursor.execute("DELETE FROM people")


        # Generate data
        for _ in range(9):
            name = names.get_full_name()
            age = random.randint(18, 80)
            email = name.lower().replace(" ", ".") + "@example.com"
            cursor.execute("INSERT INTO people (name, age, email) VALUES (%s, %s, %s)", (name, age, email))

        cursor.execute("INSERT INTO people (name, age, email) VALUES (%s, %s, %s)",
                       ("Frédéric Vasseur", 55, "frédéric.vasseur@scuderriaferrari.com"))

        connection.commit()

except Error as e:
    print("Errore durante la connessione a MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connessione a MySQL chiusa")

