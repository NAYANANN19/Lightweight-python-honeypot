import socket
import datetime
import threading
def write_log(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("honeypot_activity.log", "a") as log:
        log.write(f"[{timestamp}] {text}\n")
def handle_client(connection, address):
    ip = address[0]
    write_log(f"Connection received from {ip}")
    banner = "Welcome to Secure Server v1.4\n"
    connection.send(banner.encode())
    try:
        data = connection.recv(2048)
        if data:
            decoded = data.decode(errors="ignore").strip()
            write_log(f"Received from {ip}: {decoded}")
    except Exception as error:
        write_log(f"Error handling {ip}: {error}")
    connection.close()
    write_log(f"Closed connection with {ip}")
def start_honeypot(port=5500):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"Honeypot started on port {port}")
    write_log(f"Honeypot started on port {port}")
    while True:
        client_conn, client_addr = server.accept()
        t = threading.Thread(target=handle_client, args=(client_conn, client_addr))
        t.start()
if __name__ == "__main__":
    start_honeypot()
