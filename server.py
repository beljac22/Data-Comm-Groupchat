import socket
import threading

HOST = '0.0.0.0'  # Accept connections from any IP
PORT = 12345      # IDK what port to use, so I just used 12345

clients = dict()
lock = threading.Lock()

def broadcast(message, source_socket):
    with lock:
        print(1)
        for client in clients.keys(): 
            print(2)
            # if client: #!= source_socket: Add this in when not using same computer
            #     print(3)
            try:
                print(4)
                client.sendall(message)
                print(f"[DEBUG] Broadcasted message: {message.decode()}")  # Debug print
            except Exception as e:
                print(f"[DEBUG] Failed to send message to a client: {e}")
                del clients[client]

def direct_message(message, recipient, sender):
    with lock:
        print(1)
        for item in clients.items(): 
            if item[1] == recipient or item[1] == sender:
                print(2)
                # if client: #!= source_socket: Add this in when not using same computer
                #     print(3)
                try:
                    print(4)
                    item[0].sendall(message)
                    print(f"[DEBUG] Broadcasted message: {message.decode()}")  # Debug print
                except Exception as e:
                    print(f"[DEBUG] Failed to send message to a client: {e}")
                    del clients[item[0]]

def handle_client(client_socket, addr):
    username = None
    print(f"[NEW CONNECTION] {addr} connected.")
    with lock:
        clients[client_socket] = None

    try:
        while True:
            print(f"[DEBUG] Waiting for message from {addr}...")  # Debug print
            message = client_socket.recv(1024)
            if not message:
                print(f"[DEBUG] No message received from {addr}, closing connection.")
                break
            if not username:
                print(f"parsing <{str(message)}>")
                username = message.decode()[:(message.decode()).index(":")]
                print(f"username is <{username}>")
                clients[client_socket] = username
            print(f"[DEBUG] Received message: {message.decode()}")
            dm_slice = str(message)[str(message).index(":")+2:]
            if dm_slice.strip()[0]=="@":
                recipient = dm_slice[1:dm_slice.index(" ")]
                print(f"SENDING A DIRECT MESSAGE TO <{recipient}> FROM <{username}>")
                #message is a direct message
                direct_message(message, recipient, username)
            else:
                broadcast(message, client_socket)
    except Exception as e:
        print(f"[ERROR] {addr} - {e}")
    finally:
        print(f"[DISCONNECT] {addr} disconnected.")
        with lock:
            del clients[client_socket]
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