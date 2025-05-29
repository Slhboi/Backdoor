import base64

if __name__ == "__main__":
    while True: 
        msg = input("Enter: ")
        print(base64.b64encode(msg.encode()).decode())