Backdoor Project

Project Overview

This project is designed to perform basic backdoor functionalities on a target machine. It allows for various operations such as:

- Accessing: Gaining access to the victim's machine.
- Manipulating: Modifying or controlling files and processes on the victim's machine.
- Modifying: Changing system configurations or files.
- Downloading: Retrieving files from the victim's machine.
- Uploading: Sending files to the victim's machine.
- Encrypting/Decrypting: Securely encrypting and decrypting files using various encryption techniques.
- Persistence: Using the `persistent.py` script, the backdoor malware can be copied into the startup folder of the victim's machine, making it persistent and ensuring it runs automatically whenever the victim's machine is powered on.

Steps to Analyze the Attack

Included in the project is a file called `VERY VERY CUTE CAT.jpeg.exe`, which is an example of a disguised malicious image that could be sent to a victim. While the victim might think this is just a harmless image, in reality, it is a WinRAR archive containing two other executable files running in the background.

When the victim clicks on this "image":
1. An image of a cat will be displayed.
2. After the victim closes the image, `persistent.exe` will run in the background, copying the main payload (`backdoor.exe`) into the startup directory and renaming it to `caughtme.exe`. This ensures that the backdoor remains active as long as the victim's machine is powered on.
3. The main payload, `backdoor.exe`, will then run and attempt to connect to a listener socket, allowing a hacker to gain access to the victim's machine.

Important Notes for Analysis:
- For demonstration purposes, both payloads (`persistent.exe` and `backdoor.exe`) are designed to be ineffective under normal conditions:
  - The `persistent.exe` script assumes the user's directory is `localadmin`. If the actual user directory is different, the script will not function.
  - The `backdoor.exe` is configured to connect to the IP address `169.254.0.1`, which is an APIPA address and will not facilitate any actual connection.

To activate the exploit for testing:
- Update the directory in `persistent.py` to match your actual startup directory (you can find this by pressing Win+R and typing "shell:startup").
- Change the IP address in `Listener.py` and `Backdoor.py` to valid addresses that can communicate with each other.

**Important Warning**

Even though your antivirus might flag this file as malicious, this malware is incapable of causing harm unless the code is deliberately altered. This project is created strictly for educational purposes only.

- Do not use this project for any illegal activities.
- Unauthorized access to systems and data you do not own is illegal and unethical.
- Hacking, manipulation, or tampering with any systems or data without explicit permission is highly discouraged and could result in severe legal consequences.

Please use this knowledge responsibly, and only for learning and ethical hacking within legal boundaries.


