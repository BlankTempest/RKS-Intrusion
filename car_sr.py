import socket
import sys
import tkinter as tk
from PIL import Image, ImageTk

class CarSystem:
    def __init__(self):
        self.valid_keys = set()
        self.locked = True
        self.max_length = 8

    def add_valid_key(self, key):
        self.valid_keys.add(key)

    def validate_key(self, key):
        #shift register
        if len(key) < self.max_length :
            return False
        
        start = 0
        end = self.max_length

        for i in range (len(key) - (self.max_length-1)):
            check = key[start:end]

            if check in self.valid_keys:
                self.locked = not self.locked
                return True
            else:
                start += 1
                end += 1
        return False

    def get_door_state(self):
        return "Locked" if self.locked else "Unlocked"

class CarGUI:
    def __init__(self, root, car):
        self.root = root
        self.car = car

        self.root.title("Car Lock/Unlock System")
        
        self.heading = tk.Label(root, text="CAR", font=("Helvetica", 24))
        self.heading.pack(pady=20)

        self.locked_image = ImageTk.PhotoImage(Image.open("locked_car.jpeg"))
        self.unlocked_image = ImageTk.PhotoImage(Image.open("unlocked_car.jpeg"))

        self.image_label = tk.Label(root, image=self.locked_image)
        self.image_label.pack(pady=20)

        self.status_label = tk.Label(root, text="Locked", font=("Helvetica", 16))
        self.status_label.pack(pady=10)

        self.update_image()

    def update_image(self):
        if self.car.locked:
            self.image_label.config(image=self.locked_image)
            self.status_label.config(text="Locked")
        else:
            self.image_label.config(image=self.unlocked_image)
            self.status_label.config(text="Unlocked")
        self.root.after(1000, self.update_image)

def start_car_system(car, gui):
    car_address = "localhost"
    car_port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((car_address, car_port))
        s.listen()
        s.settimeout(1)
        
        try:
            print("Car system is listening for key validation requests...")
            while True:
                try:
                    conn, addr = s.accept()
                    with conn:
                        key = conn.recv(8192).decode()
                        if car.validate_key(key):
                            print("Door state:", car.get_door_state())
                        gui.update_image()

                except socket.timeout:
                    pass

        except KeyboardInterrupt:
            print("\nExiting program...")
            sys.exit(0)

if __name__ == "__main__":
    car = CarSystem()
    car.add_valid_key("00110011")

    root = tk.Tk()
    gui = CarGUI(root, car)

    import threading
    threading.Thread(target=start_car_system, args=(car, gui), daemon=True).start()

    root.mainloop()
