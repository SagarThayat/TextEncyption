import tkinter as tk
from tkinter import ttk

# Import encryption modules
from aes_module import aes_encrypt, aes_decrypt
from rsa_module import rsa_encrypt, rsa_decrypt
from sha_module import sha256_hash

# ------------------ MAIN WINDOW ------------------
root = tk.Tk()
root.title("Text Encryption Tool")
root.geometry("820x520")

# 🔒 Disable resize (no maximize/minimize)
root.resizable(False, False)

root.configure(bg="#f4f6f7")

# ------------------ HEADER ------------------
header = tk.Label(
    root,
    text="Text Encryption Using Various Algorithms",
    bg="#2c3e50",
    fg="white",
    font=("Arial", 18, "bold"),
    pady=10
)
header.pack(fill="x")

# ------------------ INPUT FRAME ------------------
input_frame = tk.Frame(root, bg="#f4f6f7", pady=6)
input_frame.pack()

tk.Label(
    input_frame,
    text="Enter Plain Text:",
    bg="#f4f6f7",
    font=("Arial", 11, "bold")
).pack(anchor="w")

text_input = tk.Text(input_frame, height=4, width=95)
text_input.pack(pady=4)

# ------------------ CONTROL FRAME ------------------
control_frame = tk.Frame(root, bg="#f4f6f7", pady=6)
control_frame.pack()

tk.Label(control_frame, text="Algorithm:", bg="#f4f6f7").grid(row=0, column=0, padx=10)

algo = ttk.Combobox(
    control_frame,
    values=["AES", "RSA", "SHA-256"],
    state="readonly",
    width=15
)
algo.grid(row=0, column=1, padx=10)
algo.current(0)

# AES Secret Key
key_label = tk.Label(control_frame, text="Secret Key (AES):", bg="#f4f6f7")
key_entry = tk.Entry(control_frame, width=22, show="*")
key_label.grid(row=1, column=0, padx=10)
key_entry.grid(row=1, column=1, padx=10)

# ------------------ OUTPUT FRAME ------------------
output_frame = tk.Frame(root, bg="#f4f6f7", pady=6)
output_frame.pack()

tk.Label(
    output_frame,
    text="Encrypted / Hashed Output:",
    bg="#f4f6f7",
    font=("Arial", 11, "bold")
).pack(anchor="w")

output = tk.Text(output_frame, height=4, width=95, state="disabled")
output.pack(pady=4)

# ------------------ FUNCTIONS ------------------
def encrypt_or_hash():
    text = text_input.get("1.0", tk.END).strip()
    algorithm = algo.get()
    key = key_entry.get().strip()

    output.config(state="normal")
    output.delete("1.0", tk.END)

    if not text:
        output.insert(tk.END, "Please enter text first.")
        output.config(state="disabled")
        return

    try:
        if algorithm == "AES":
            if not key:
                raise ValueError("AES secret key required.")
            result = aes_encrypt(text, key)

        elif algorithm == "RSA":
            result = rsa_encrypt(text)

        elif algorithm == "SHA-256":
            result = sha256_hash(text)

        output.insert(tk.END, result)

    except Exception as e:
        output.insert(tk.END, f"Error: {e}")

    output.config(state="disabled")


def decrypt_text():
    output.config(state="normal")
    cipher_text = output.get("1.0", tk.END).strip()
    output.config(state="disabled")

    algorithm = algo.get()
    key = key_entry.get().strip()

    text_input.delete("1.0", tk.END)

    if not cipher_text:
        text_input.insert(tk.END, "No encrypted text to decrypt.")
        return

    try:
        if algorithm == "AES":
            result = aes_decrypt(cipher_text, key)
        elif algorithm == "RSA":
            result = rsa_decrypt(cipher_text)
        else:
            result = "SHA-256 hashing cannot be decrypted."

        text_input.insert(tk.END, result)

    except Exception:
        text_input.insert(tk.END, "Invalid key or corrupted data!")

# ------------------ ALGORITHM CHANGE HANDLER ------------------
def on_algorithm_change(event=None):
    selected_algo = algo.get()

    if selected_algo == "AES":
        encrypt_btn.config(text="Encrypt", bg="#27ae60")
        decrypt_btn.grid(row=0, column=3, padx=12)
        key_label.grid()
        key_entry.grid()

    elif selected_algo == "RSA":
        encrypt_btn.config(text="Encrypt", bg="#27ae60")
        decrypt_btn.grid(row=0, column=3, padx=12)
        key_label.grid_remove()
        key_entry.grid_remove()
        key_entry.delete(0, tk.END)

    elif selected_algo == "SHA-256":
        encrypt_btn.config(text="Hash", bg="#8e44ad")
        decrypt_btn.grid_remove()
        key_label.grid_remove()
        key_entry.grid_remove()
        key_entry.delete(0, tk.END)

algo.bind("<<ComboboxSelected>>", on_algorithm_change)

# ------------------ BUTTONS ------------------
encrypt_btn = tk.Button(
    control_frame,
    text="Encrypt",
    bg="#27ae60",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12,
    command=encrypt_or_hash
)
encrypt_btn.grid(row=0, column=2, padx=12)

decrypt_btn = tk.Button(
    control_frame,
    text="Decrypt",
    bg="#2980b9",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12,
    command=decrypt_text
)
decrypt_btn.grid(row=0, column=3, padx=12)

# ------------------ FOOTER ------------------
footer = tk.Label(
    root,
    text="AES (Symmetric) | RSA (Asymmetric) | SHA-256 (One-way Hashing)",
    bg="#ecf0f1",
    font=("Arial", 10),
    pady=4
)
footer.pack(fill="x", side="bottom")

# Initial UI state
on_algorithm_change()

# ------------------ START APP ------------------
root.mainloop()
