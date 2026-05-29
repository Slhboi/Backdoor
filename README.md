# Obfuscated RCE Backdoor Project

This project demonstrates an obfuscated remote command execution (RCE) backdoor with persistence capabilities, designed for educational cybersecurity experimentation in a controlled lab environment.

The system supports operations such as:

* **Accessing:** Establishing remote access to a lab machine.
* **Manipulating:** Managing files and processes on the system.
* **Modifying:** Changing system configurations or files.
* **Downloading:** Retrieving files from the machine.
* **Uploading:** Sending files to the machine.
* **Encrypting/Decrypting:** Encrypting and decrypting files using encryption techniques.
* **Persistence:** Using a secondary executable to copy the main payload into the startup folder, allowing it to run automatically when the machine starts.
* **Obfuscation:** Applying techniques such as string encryption, runtime decryption, function renaming, and control-flow noise to make static malware analysis more difficult.

## Attack Demonstration

The obfuscated version uses a loader-style setup to demonstrate how payload hiding and runtime decryption can work in a controlled lab environment.

The project includes an executable named `print_hello_world.exe`, which is intentionally named to appear harmless as part of the social engineering demonstration.

When `print_hello_world.exe` is executed:

1. The embedded stub is loaded and executed.
2. The stub decrypts both the main payload and the persistence component at runtime.
3. After decryption, the persistence component begins execution and attempts to place the payload in the startup directory.
4. The main backdoor payload then begins execution and attempts to connect to the configured listener socket.
5. At the same time, the program displays the message:

```text
This literally just prints hello world, I don't know what you were expecting
```

This is used to make the executable appear like a harmless joke program while the actual payload logic is handled in the background by the decrypted components.

## Obfuscation

The newer version of this project includes obfuscation techniques to demonstrate how malware authors attempt to make static analysis harder.

Implemented obfuscation techniques include:

* String encryption
* Runtime string decryption
* Function and variable renaming
* Control-flow noise
* Reduced readability of sensitive logic

These techniques were added for malware analysis practice and to understand how obfuscation affects detection, reverse engineering, and defensive investigation.

## Safety Notes

For demonstration purposes, the included payloads are intentionally configured to be ineffective under normal conditions.

The project is intended to be analyzed and tested only inside a safe, isolated, and authorized lab environment.

## Demonstration Video

A demonstration of the project is available here:

https://youtu.be/E399QfpxDNs

## Important Warning

Even though antivirus software may flag this file as malicious, this malware is incapable of causing harm unless the code is deliberately altered. This project is created strictly for educational purposes only.

* Do not use this project for any illegal activities.
* Unauthorized access to systems and data you do not own is illegal and unethical.
* Hacking, manipulation, or tampering with any systems or data without explicit permission is highly discouraged and could result in severe legal consequences.

Please use this knowledge responsibly, and only for learning and ethical hacking within legal boundaries.
