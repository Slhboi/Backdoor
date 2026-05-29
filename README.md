# Obfuscated RCE Backdoor Project

This project demonstrates a remote command execution (RCE) backdoor with persistence and obfuscation capabilities, designed for educational cybersecurity experimentation in a controlled lab environment.

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

The project includes a demonstration file named `VERY VERY CUTE CAT.jpeg.exe`, which represents a disguised executable used to demonstrate how social engineering and file masquerading can be used in malware delivery.

When executed in the lab environment:

1. A cat image is displayed to appear harmless.
2. A persistence component runs in the background and places the main payload in the startup directory under a different name.
3. The main backdoor payload attempts to connect to a listener socket to simulate remote access.

For safety, the included payloads are intentionally configured to be ineffective under normal conditions.

* The persistence script uses a hardcoded test directory.
* The backdoor uses a non-routable APIPA address, preventing real external communication unless deliberately modified in an authorized lab setup.

## Obfuscation

The newer version of this project includes obfuscation techniques to demonstrate how malware authors attempt to make static analysis harder.

Implemented obfuscation techniques include:

* String encryption
* Runtime string decryption
* Function and variable renaming
* Added control-flow noise
* Reduced readability of sensitive logic

These techniques were added for malware analysis practice and to understand how obfuscation affects detection, reverse engineering, and defensive investigation.

## Demonstration Video

A demonstration of the project is available here:

https://youtu.be/E399QfpxDNs

## Important Warning

Even though antivirus software may flag this file as malicious, this malware is incapable of causing harm unless the code is deliberately altered. This project is created strictly for educational purposes only.

* Do not use this project for any illegal activities.
* Unauthorized access to systems and data you do not own is illegal and unethical.
* Hacking, manipulation, or tampering with any systems or data without explicit permission is highly discouraged and could result in severe legal consequences.

Please use this knowledge responsibly, and only for learning and ethical hacking within legal boundaries.
