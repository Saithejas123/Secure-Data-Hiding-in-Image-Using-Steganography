import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

def decrypt_image(image_path, entered_password):
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Unable to read the image file.")
        return

    c = {i: chr(i) for i in range(255)}

    # Retrieve message length
    message_length = img[0, 0, 0]
    if message_length == 0:
        messagebox.showerror("Error", "No encrypted message found!")
        return

    message = ""
    n, m, z = 0, 1, 0  # Start from second pixel

    for _ in range(message_length):
        message += c.get(img[n, m, z], "?")  # Default to '?'
        z = (z + 1) % 3
        if z == 0:
            m += 1
            if m >= img.shape[1]:
                m = 0
                n += 1

    # Check message format
    if ":" not in message:
        messagebox.showerror("Error", "Decryption failed! Data may be corrupted.")
        return

    # Split password and message
    stored_password, decrypted_message = message.split(":", 1)

    if stored_password == entered_password:
        messagebox.showinfo("Decrypted Message", decrypted_message)
    else:
        messagebox.showerror("Error", "Incorrect Password")

def browse_file():
    file_path = filedialog.askopenfilename()
    entry_image_path.delete(0, tk.END)
    entry_image_path.insert(0, file_path)

def decrypt_action():
    image_path = entry_image_path.get()
    entered_password = entry_password.get()
    decrypt_image(image_path, entered_password)

# GUI Setup
root = tk.Tk()
root.title("Image Decryption")
root.geometry("500x400")
root.configure(bg="#2C3E50")

tk.Label(root, text="Select Encrypted Image:", bg="#2C3E50", fg="white").pack()
entry_image_path = tk.Entry(root, width=50)
entry_image_path.pack()
tk.Button(root, text="Browse", command=browse_file, bg="#1ABC9C", fg="white").pack()

tk.Label(root, text="Enter Password:", bg="#2C3E50", fg="white").pack()
entry_password = tk.Entry(root, show="*", width=50)
entry_password.pack()

tk.Button(root, text="Decrypt", command=decrypt_action, bg="#E74C3C", fg="white").pack()

root.mainloop()
