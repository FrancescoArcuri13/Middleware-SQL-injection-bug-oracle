import socket
import asyncio
from typing import Dict

import mysql.connector
import mysql_mimic.errors
from mysql_mimic import MysqlServer, AllowedResult
from mysql_mimic import Session
from mysql_mimic.connection import Connection
from mysql_mimic.session import Query

from testFile.tools import reset_db_timeout_to_default, set_db_timeout

# Middleware and server error
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'TestMiddleware'
DB_PASS = 'TestMiddleware'
DB_NAME = 'peopleDB'
ERROR_LOG_SERVER_HOST = 'localhost'
ERROR_LOG_SERVER_PORT = 9091

# Increase timeouts before starting long operations
increased_wait_timeout = 604800  # set to 1 week
increased_interactive_timeout = 604800


# Connection to DB and server error
db_conn = mysql.connector.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, database=DB_NAME)
set_db_timeout(db_conn, increased_wait_timeout, increased_interactive_timeout)

error_log_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
error_log_socket.connect((ERROR_LOG_SERVER_HOST, ERROR_LOG_SERVER_PORT))


class MyCustomSession(Session):
    def __init__(self):
        super().__init__()
        self.conn = db_conn

    async def connection(self) -> Connection:
        return await self.conn

    async def handle_query(self, sql: str, attrs: Dict[str, str]) -> AllowedResult:
        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            if cursor.description:
                columns = [c[0] for c in cursor.description]
                return rows, columns
            return None

        except mysql.connector.Error as err:
            log_error_to_server(str(err))
            raise mysql_mimic.errors.MysqlError(err)

        finally:
            cursor.close()

# Authentication
async def auth_handler(username, password):
    if username == "TestMiddleware" and password == "TestMiddleware":
        return True
    return False

async def start_server():
    try:
        middleware = MysqlServer(session_factory=MyCustomSession)
        #middleware.auth_handler = auth_handler

        await middleware.start_server(port=9092)
        await middleware.serve_forever()
    finally:
        reset_db_timeout_to_default(db_conn)
        db_conn.close()


def log_error_to_server(error_message):
    error_log_socket.sendall(error_message.encode())


if __name__ == '__main__':
    asyncio.run(start_server())



