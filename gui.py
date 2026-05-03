import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import hashlib

from main import KMS, HDFS, Client


# -------------------------------
# DATABASE SETUP
# -------------------------------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()


# -------------------------------
# HASH FUNCTION
# -------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------------------
# REGISTER WINDOW
# -------------------------------
def open_register_window():
    reg_win = tk.Toplevel()
    reg_win.title("Register")
    reg_win.geometry("300x200")

    tk.Label(reg_win, text="Create Account", font=("Arial", 14)).pack(pady=10)

    reg_user = tk.Entry(reg_win)
    reg_user.pack(pady=5)
    reg_user.insert(0, "Username")

    reg_pass = tk.Entry(reg_win, show="*")
    reg_pass.pack(pady=5)
    reg_pass.insert(0, "Password")

    def register_user():
        username = reg_user.get()
        password = reg_pass.get()

        if not username or not password:
            messagebox.showerror("Error", "Fields cannot be empty")
            return

        try:
            cursor.execute("INSERT INTO users VALUES (?, ?)",
                           (username, hash_password(password)))
            conn.commit()
            messagebox.showinfo("Success", "Registered successfully!")
            reg_win.destroy()
        except:
            messagebox.showerror("Error", "User already exists")

    tk.Button(reg_win, text="Register", command=register_user).pack(pady=10)


# -------------------------------
# MAIN APP
# -------------------------------
def open_main_app():
    login_window.destroy()

    global kms, hdfs, client
    kms = KMS()
    hdfs = HDFS()
    client = Client(kms, hdfs)

    app = tk.Tk()
    app.title("Secure HDFS System")
    app.geometry("400x300")

    def upload():
        filepath = filedialog.askopenfilename()
        if filepath:
            try:
                client.upload_file(filepath)
                messagebox.showinfo("Success", "File uploaded!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def download():
        filename = file_entry.get()
        if filename:
            try:
                client.download_file(filename)
                messagebox.showinfo("Success", "File downloaded!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    tk.Label(app, text="Upload File").pack(pady=5)
    tk.Button(app, text="Choose & Upload", command=upload).pack(pady=5)

    tk.Label(app, text="Download File").pack(pady=5)
    file_entry = tk.Entry(app)
    file_entry.pack(pady=5)

    tk.Button(app, text="Download", command=download).pack(pady=5)

    app.mainloop()


# -------------------------------
# LOGIN FUNCTION
# -------------------------------
def login():
    username = user_entry.get()
    password = hash_password(pass_entry.get())

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Success", "Login successful!")
        open_main_app()
    else:
        messagebox.showerror("Error", "Invalid credentials")


# -------------------------------
# LOGIN WINDOW (MAIN)
# -------------------------------
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("350x250")

tk.Label(login_window, text="Login", font=("Arial", 16)).pack(pady=10)

user_entry = tk.Entry(login_window)
user_entry.pack(pady=5)
user_entry.insert(0, "Username")

pass_entry = tk.Entry(login_window, show="*")
pass_entry.pack(pady=5)
pass_entry.insert(0, "Password")

tk.Button(login_window, text="Login", command=login).pack(pady=10)

# Register redirect
tk.Label(login_window, text="Not registered?").pack()
tk.Button(login_window, text="Click here to Register",
          command=open_register_window).pack(pady=5)

login_window.mainloop()
