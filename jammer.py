import socket

def jam_keys(car_address, car_port, jammer_port):
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


if __name__ == "__main__":
    car_address = "localhost"
    car_port = 12345
    jammer_port = 12346
    jam_keys(car_address, car_port, jammer_port)
