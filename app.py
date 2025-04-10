import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

USERNAME = None
client_socket = None
connected = False

def receive_messages():
    global connected
    while connected:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"[DEBUG] Received message: {message}")  # Debug print
            chat_display.configure(state='normal')
            chat_display.insert(tk.END, message + "\n")
            chat_display.configure(state='disabled')
            chat_display.see(tk.END)
        except Exception as e:
            print(f"[DEBUG] Error receiving message: {e}")
            break

def send_message():
    global USERNAME
    if not USERNAME or not connected:
        print("[DEBUG] Cannot send message: Not connected or username not set.")
        return

    message = entry.get()
    if message.strip():
        full_message = f"{USERNAME}: {message}"
        try:
            client_socket.sendall(full_message.encode())
            print(f"[DEBUG] Sent message: {full_message}")
        except Exception as e:
            chat_display.configure(state='normal')
            chat_display.insert(tk.END, f"[Error] Failed to send message: {e}\n")
            chat_display.configure(state='disabled')
        entry.delete(0, tk.END)

def set_user(username, parent):
    global USERNAME
    USERNAME = username.strip()
    if USERNAME:
        parent.destroy()
        connect_to_server()

def show_popup_text_box():
    popup = tk.Toplevel()
    popup.geometry("250x100")
    popup.title("Enter Your Name")

    label = tk.Label(popup, text="Enter your username:")
    label.pack(pady=(10, 0))

    text_area = tk.Entry(popup)
    text_area.pack(pady=5)
    text_area.focus()

    ok_button = tk.Button(popup, text="Set Username", command=lambda: set_user(text_area.get(), popup))
    ok_button.pack(pady=5)

def connect_to_server():
    global client_socket, connected
    try:
        server_ip = "127.0.0.1"  # Replace with actual IP, this is localhost
        server_port = 12345
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        connected = True

        print("[DEBUG] Starting receive_messages thread")  # Debug print
        threading.Thread(target=receive_messages, daemon=True).start()
        chat_display.configure(state='normal')
        chat_display.insert(tk.END, f"[Connected to {server_ip}:{server_port}]\n")
        chat_display.configure(state='disabled')

    except Exception as e:
        chat_display.configure(state='normal')
        chat_display.insert(tk.END, f"[Failed to connect to server: {e}]\n")
        chat_display.configure(state='disabled')

#GUI
root = tk.Tk()
root.title("TCP Group Chat")
root.geometry("400x500")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=20)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10, fill=tk.X)

entry = tk.Entry(input_frame)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

root.bind('<Return>', lambda _: send_message())

root.after(10, show_popup_text_box)
root.mainloop()
