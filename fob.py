import socket
import tkinter as tk

def send_key_to_car(key):
    car_address = "localhost"
    car_port = 12346
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((car_address, car_port))
        s.sendall(key.encode())

def change_image():
    button.config(image=image_beep)
    root.after(250, revert_image)

def revert_image():
    button.config(image=image_boop)

def on_button_press():
    key = input_entry.get()
    send_key_to_car(key)
    change_image()

root = tk.Tk()
root.title("Fob")

image_beep = tk.PhotoImage(file="fob_beep.png")
image_boop = tk.PhotoImage(file="fob_boop.png")

button = tk.Button(root, image=image_boop, command=on_button_press)
button.pack()

input_entry = tk.Entry(root)
input_entry.pack()

root.mainloop()

