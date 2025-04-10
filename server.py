import socket
import threading

HOST = '0.0.0.0'  # Accept connections from any IP
PORT = 12345      # IDK what port to use, so I just used 12345

clients = []
lock = threading.Lock()

def broadcast(message, source_socket):
    with lock:
        print(1)
        for client in clients: 
            print(2)
            # if client: #!= source_socket: Add this in when not using same computer
            #     print(3)
            try:
                print(4)
                client.sendall(message)
                print(f"[DEBUG] Broadcasted message: {message.decode()}")  # Debug print
            except Exception as e:
                print(f"[DEBUG] Failed to send message to a client: {e}")
                clients.remove(client)

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    with lock:
        clients.append(client_socket)

    try:
        while True:
            print(f"[DEBUG] Waiting for message from {addr}...")  # Debug print
            message = client_socket.recv(1024)
            if not message:
                print(f"[DEBUG] No message received from {addr}, closing connection.")
                break
            print(f"[DEBUG] Received message: {message.decode()}")
            broadcast(message, client_socket)
    except Exception as e:
        print(f"[ERROR] {addr} - {e}")
    finally:
        print(f"[DISCONNECT] {addr} disconnected.")
        with lock:
            clients.remove(client_socket)
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is running on {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
    except KeyboardInterrupt:
        print("[SHUTDOWN] Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()