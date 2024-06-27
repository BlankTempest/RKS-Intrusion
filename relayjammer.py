import socket
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import threading
import queue

class JammerRelayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jammer/Relay Interface")
        self.root.geometry("400x300") 

        self.status_label = tk.Label(root, text="Jammer Status: Inactive", fg="red")
        self.status_label.pack(pady=5)

        self.output_area = scrolledtext.ScrolledText(root, state='disabled', height=5, width=50)
        self.output_area.pack(padx=10, pady=10)

        self.intercepted_data_label = tk.Label(root, text="Intercepted Data:")
        self.intercepted_data_label.pack(pady=5)

        self.intercepted_data_display = tk.Text(root, height=5, width=50)
        self.intercepted_data_display.pack(padx=10, pady=10)

        self.toggle_jammer_button = tk.Button(root, text="Toggle Jammer", command=self.toggle_jammer)
        self.toggle_jammer_button.pack(pady=5)

        self.send_intercept_button = tk.Button(root, text="SEND INTERCEPT", command=self.send_intercept, state='disabled')
        self.send_intercept_button.pack(pady=5)

        self.arrow_image = ImageTk.PhotoImage(Image.open("arrow.png").resize((50, 50)))
        self.blank_image = ImageTk.PhotoImage(Image.open("blank.png").resize((50, 50)))
        self.jammer_active_image = ImageTk.PhotoImage(Image.open("img2.png").resize((50, 50)))
        self.jammer_inactive_image = ImageTk.PhotoImage(Image.open("img1.png").resize((50, 50)))

        self.left_arrow_label = tk.Label(root, image=self.blank_image)
        self.left_arrow_label.pack(side=tk.LEFT, padx=10)

        self.jammer_label = tk.Label(root, image=self.jammer_inactive_image)
        self.jammer_label.pack(side=tk.LEFT, padx=10)

        self.right_arrow_label = tk.Label(root, image=self.blank_image)
        self.right_arrow_label.pack(side=tk.LEFT, padx=10)

        self.jammer_socket = None
        self.car_socket = None
        self.relay_thread = None
        self.jamming_active = False
        self.message_queue = queue.Queue()

        self.start_relay()

    def toggle_jammer(self):
        self.jamming_active = not self.jamming_active
        status_text = "Active" if self.jamming_active else "Inactive"
        status_color = "green" if self.jamming_active else "red"
        self.status_label.config(text=f"Jammer Status: {status_text}", fg=status_color)
        self.jammer_label.config(image=self.jammer_active_image if self.jamming_active else self.jammer_inactive_image)
        self.send_intercept_button.config(state='normal' if self.jamming_active else 'disabled')
        self.output_area.configure(state='normal')
        self.output_area.insert(tk.END, f"Jammer is now {status_text}.\n")
        self.output_area.configure(state='disabled')
        self.output_area.see(tk.END)
        print(f"Jammer is now {status_text}.")

    def start_relay(self):
        self.relay_thread = threading.Thread(target=self.relay, daemon=True)
        self.relay_thread.start()

    def relay(self):
        fob_port = 12346
        car_address = "localhost"
        car_port = 12345
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as fob_socket:
            fob_socket.bind(("localhost", fob_port))
            fob_socket.listen()
            print(f"Relay is listening on port {fob_port}...")
            while True:
                conn, addr = fob_socket.accept()
                print(f"Connected to {addr}")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as car_socket:
                    car_socket.connect((car_address, car_port))
                    print(f"Connected to car {car_address}:{car_port}")
                    while True:
                        data = conn.recv(8192)
                        if not data:
                            break
                        if self.jamming_active:
                            self.message_queue.put(data)
                            self.display_intercepted_data(data)
                            print(f"Jammer intercepted {len(data)} bytes of data")
                        else:
                            while not self.message_queue.empty():
                                queued_data = self.message_queue.get()
                                car_socket.sendall(queued_data)
                                print(f"Relayed {len(queued_data)} bytes of queued data")
                            self.animate_arrows()
                            car_socket.sendall(data)
                            print(f"Relayed {len(data)} bytes of data")

    def animate_arrows(self):
        
        self.left_arrow_label.config(image=self.arrow_image)
        self.right_arrow_label.config(image=self.arrow_image)
        
        self.root.after(1000, self.clear_arrows)

    def clear_arrows(self):
        self.left_arrow_label.config(image=self.blank_image)
        self.right_arrow_label.config(image=self.blank_image)

    def display_intercepted_data(self, data):
        self.intercepted_data_display.insert(tk.END, data.decode() + "\n")

    def send_intercept(self):
        while not self.message_queue.empty():
            data2 = self.message_queue.get()
            print("ssssss",data2)
            
            car_address = "localhost"
            car_port = 12345
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as car_socket:
                        car_socket.connect((car_address, car_port))
                        print(f"Connected to car {car_address}:{car_port}")
                        
                                
                        car_socket.sendall(data2)
                        print(f"Relayed {len(data2)} bytes of data")
                    

if __name__ == "__main__":
    root = tk.Tk()
    app = JammerRelayApp(root)
    root.mainloop()
