import socket
import sys

def relay(fob_port, car_address, car_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as fob_socket:
        fob_socket.bind(("localhost", fob_port))
        fob_socket.listen()

        print(f"Relay is listening on port {fob_port}...")

        while True:
            try:
                conn, addr = fob_socket.accept()
                print(f"Connected to {addr}")

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as car_socket:
                    car_socket.connect((car_address, car_port))
                    print(f"Connected to car {car_address}:{car_port}")

                    while True:
                        data = conn.recv(8192)
                        if not data or data == "":
                            break
                        print(data)
                        car_socket.sendall(data)
                        print(f"Relayed {len(data)} bytes of data")
            except KeyboardInterrupt:
                print("\nExiting program...")
                sys.exit(0)


if __name__ == "__main__":
    fob_port = 12346
    car_address = "localhost"
    car_port = 12345

    relay(fob_port, car_address, car_port)
