import tkinter as tk
from tkinter import scrolledtext

USERNAME = None

class STYLE:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

def send_message():
    global USERNAME
    if not USERNAME:
        return

    message = entry.get()
    if message.strip():
        chat_display.configure(state='normal')
        chat_display.insert(tk.END, r'\u001b[0;32m'+f"{USERNAME}: " + message + r'\u001b[0m' +"\n")
        chat_display.configure(state='disabled',)
        chat_display.see(tk.END)
        entry.delete(0, tk.END)

root = tk.Tk()
root.title("Chat Interface")
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


def show_popup_text_box(text=""):
    popup = tk.Toplevel()
    popup.geometry("100x50")
    popup.title("Popup Text Box")
    text_area = tk.Entry(popup)
    text_area.insert(tk.END, text)
    text_area.pack()
    ok_button = tk.Button(popup, text="Set Username", command=lambda: set_user(text_area.get(),popup))
    ok_button.pack()
    USERNAME = text_area.get()
    print("Username is ",USERNAME)
    assert not USERNAME, "Username is already set"

def set_user(username, parent):
    global USERNAME

    USERNAME = username.strip()
    assert username, "Username is already set"
    USERNAME = username.strip()
    parent.destroy()

# dispach a CPU thread to loop this shit slime nah mean?
def fetch_messages():
    pass

root.after(10, show_popup_text_box)
root.mainloop()

