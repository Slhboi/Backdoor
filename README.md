# Obfuscated Remote Command Execution Payload

This project demonstrates a remote command execution payload with persistence and obfuscation capabilities, built for educational cybersecurity experimentation in a controlled lab environment.

The payload supports operations such as:

* **Accessing:** Establishing remote access to a lab machine
* **Manipulating:** Managing files and processes on the system
* **Modifying:** Changing files or basic system configurations
* **Downloading:** Retrieving files from the machine
* **Uploading:** Sending files to the machine
* **Encrypting/Decrypting:** Protecting files using encryption techniques
* **Persistence:** Maintaining access through a secondary executable that copies itself into the system startup folder
* **Obfuscation:** Applying techniques such as string encryption, function renaming, runtime decryption, and control-flow noise to make static analysis harder

The purpose of this project is to better understand how remote access payloads work, how persistence is commonly implemented, and how obfuscation affects malware analysis.

NOTE: This project was developed strictly for educational cybersecurity learning purposes.
