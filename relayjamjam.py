import socket
import tkinter as tk

intercepted_key = ""
jammer_active = False

def jam_keys(car_address, car_port, jammer_port):
    global intercepted_key

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as jammer_socket:
        jammer_socket.bind(("localhost", jammer_port))
        jammer_socket.listen()

        print("Jammer is active and intercepting key signals...")
        car_socket = None

        while True:
            conn, addr = jammer_socket.accept()
            print("Connected to remote fob:", addr)
        
            while True:
                key = conn.recv(1024).decode()
                if not key:
                    break
                print("Intercepted key:", key)
                intercepted_key = key

                if jammer_active:
                    key = "00000000"
                
                if car_socket is None:
                    car_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    car_socket.connect((car_address, car_port))
                    print("Connected to car")

                try:
                    car_socket.sendall(key.encode())
                except ConnectionAbortedError:
                    #Reconnecting
                    car_socket.close()
                    car_socket = None
                    break

def send_key_to_car():
    global intercepted_key
    car_address = "localhost"
    car_port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as car_socket:
        car_socket.connect((car_address, car_port))
        car_socket.sendall(intercepted_key.encode())
        print("Intercepted key sent to car:", intercepted_key)

def toggle_jammer():
    global jammer_active
    jammer_active = not jammer_active
    if jammer_active:
        print("Jammer activated")
    else:
        print("Jammer deactivated")

if __name__ == "__main__":
    car_address = "localhost"
    car_port = 12345
    jammer_port = 12346

    import threading
    jammer_thread = threading.Thread(target=jam_keys, args=(car_address, car_port, jammer_port))
    jammer_thread.daemon = True
    jammer_thread.start()

    root = tk.Tk()
    root.title("Jammer Control")

    lbl_intercepted_key = tk.Label(root, text="Intercepted Key: ", font=("Helvetica", 12))
    lbl_intercepted_key.pack(pady=10)

    btn_send_key = tk.Button(root, text="Send Intercepted Key to Car", command=send_key_to_car)
    btn_send_key.pack(pady=10)

    btn_toggle_jammer = tk.Button(root, text="Toggle Jammer", command=toggle_jammer)
    btn_toggle_jammer.pack(pady=10)

    root.mainloop()
