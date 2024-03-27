import mysql.connector
from mysql.connector import Error
import time

from testFile.tools import random_string


def create_connection(port):
    connection_params = {
        'host': 'localhost',
        'port': port,
    }

    if port == 3306:
        # Aggiungi i parametri solo se la porta è 3306
        connection_params['user'] = 'TestMiddleware'
        connection_params['password'] = 'TestMiddleware'
        connection_params['database'] = 'peopleDB'

    return connection_params


def runTest(port, silent=True, include_commit=False):
    execution_time_ALL = time.perf_counter()
    execution_times = []
    max_retries = 10  # number of attempts in case of error

    # 0 Database Connection Time
    # 1 Select Query Time
    # 2 Delete Query Time
    # 3 Insert Query Time
    # 4 Error Query Time

    try:
        # Database Connection
        start_time = time.perf_counter()
        connection = mysql.connector.connect(**create_connection(port))

        if connection.is_connected():
            execution_times.append(time.perf_counter() - start_time)
            if not silent:
                print("Connection to DB on")

            # Select
            attempt = 0
            while attempt < max_retries:
                try:
                    # Selecting the tuple Frédéric Vasseur
                    with connection.cursor() as select_cursor:
                        query = "SELECT * FROM people WHERE name = %s"
                        start_time = time.perf_counter()
                        select_cursor.execute(query, ("Frédéric Vasseur",))
                        row = select_cursor.fetchone()
                    execution_times.append(time.perf_counter() - start_time)
                    if not silent:
                        print("Selected:", row)
                    break
                except mysql.connector.Error as op_err:
                    if not silent:
                        print(op_err)
                    attempt += 1
                    time.sleep(0.2)
                    if attempt >= max_retries:
                        raise op_err

            # Assuming ID is the first column
            id_to_delete = row[0]

            # Deleting the tuple
            attempt = 0
            while attempt < max_retries:
                try:
                    with connection.cursor() as delete_cursor:
                        delete_query = "DELETE FROM people WHERE id = " + str(id_to_delete)
                        start_time = time.perf_counter()
                        delete_cursor.execute(delete_query)
                        if include_commit:
                            connection.commit()
                        execution_times.append(time.perf_counter() - start_time)
                        if not include_commit:
                            connection.commit()
                    if not silent:
                        print('Delete: ', id_to_delete)
                    break
                except mysql.connector.Error as op_err:
                    if not silent:
                        print(op_err)
                    attempt += 1
                    time.sleep(0.2)
                    if attempt >= max_retries:
                        raise op_err

            # Inserting the tuple
            attempt = 0
            while attempt < max_retries:
                try:
                    with connection.cursor() as insert_cursor:
                        columns = ', '.join(['%s'] * len(row))
                        insert_query = f"INSERT INTO people VALUES ({columns})"
                        start_time = time.perf_counter()
                        insert_cursor.execute(insert_query, row)
                        if include_commit:
                            connection.commit()
                        execution_times.append(time.perf_counter() - start_time)
                        if not include_commit:
                            connection.commit()
                    if not silent:
                        print('Inserted: ', row)
                    break
                except mysql.connector.Error as op_err:
                    if not silent:
                        print(op_err)
                    attempt += 1
                    time.sleep(0.2)
                    if attempt >= max_retries:
                        raise op_err


            # Executing an erroneous query
            try:
                with connection.cursor() as error_cursor:
                    error_query = "SELECT * FROM people WHERE name = " + random_string(5)
                    # error_query = random_string(28)
                    start_time = time.perf_counter()
                    error_cursor.execute(error_query)
                    result = error_cursor.fetchall()
                    if include_commit:
                        connection.commit()
                    execution_times.append(time.perf_counter() - start_time)
                    if not include_commit:
                        connection.commit()
                    if not silent:
                        print(result)
            except mysql.connector.Error as err:
                execution_times.append(time.perf_counter() - start_time)
                if not silent:
                    print("Error: ", err)





    except Error as e:
        if not silent:
            print("Error during the connection to MySQL", e)
        execution_times = None
    finally:
        if connection.is_connected():
            connection.close()
            if not silent:
                print("Connection to MySQL closed")
    if not silent:
        print("Tempo totale di esecuzione: " + str(round((time.perf_counter() - execution_time_ALL)/60, 2)) + " minutes")
    return execution_times

if __name__ == "__main__":
    results = runTest(9092, False)
    print("Execution Times:", results)

