import re
import hashlib
import requests
import tkinter as tk
from tkinter import messagebox

# -----------------------------
# Password Strength Checker
# -----------------------------
def check_password_strength(password):
    length_error = len(password) < 8
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    digit_error = re.search(r"\d", password) is None
    special_char_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None
    
    errors = [length_error, uppercase_error, lowercase_error, digit_error, special_char_error]
    
    if all(not e for e in errors):
        return "✅ Strong Password"
    elif sum(errors) <= 2:
        return "⚠️ Medium Strength Password"
    else:
        return "❌ Weak Password"

# -----------------------------
# Check if password was leaked
# -----------------------------
def check_pwned(password):
    sha1pwd = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = sha1pwd[:5]
    suffix = sha1pwd[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "⚠️ Could not check breach status"
    
    hashes = (line.split(":") for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return f"❌ Found in data breaches {count} times!"
    return "✅ Not found in known breaches."

# -----------------------------
# GUI Function
# -----------------------------
def check_password():
    pwd = entry.get()
    if not pwd:
        messagebox.showwarning("Input Error", "Please enter a password!")
        return
    
    strength = check_password_strength(pwd)
    breach = check_pwned(pwd)
    
    result_label.config(text=f"{strength}\n{breach}", fg="blue")

# -----------------------------
# Tkinter UI Setup
# -----------------------------
root = tk.Tk()
root.title("🔐 Password Checker")
root.geometry("400x250")
root.resizable(False, False)

# Heading
heading = tk.Label(root, text="🔑 Password Strength & Breach Checker", font=("Arial", 12, "bold"))
heading.pack(pady=10)

# Input
entry = tk.Entry(root, show="*", width=30, font=("Arial", 12))
entry.pack(pady=10)

# Button
check_btn = tk.Button(root, text="Check Password", command=check_password, font=("Arial", 11), bg="green", fg="white")
check_btn.pack(pady=5)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 11), wraplength=350, justify="center")
result_label.pack(pady=20)

# Run App
root.mainloop()
