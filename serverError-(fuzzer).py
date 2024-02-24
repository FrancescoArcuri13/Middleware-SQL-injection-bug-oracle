import socket

def start_error_log_server(host='localhost', port=9091):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Error log server in ascolto su {host}:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"Connessione da {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Errore ricevuto: {data.decode()}")

if __name__ == '__main__':
    start_error_log_server()
