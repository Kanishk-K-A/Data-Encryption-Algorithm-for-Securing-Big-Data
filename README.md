# Data-Encryption-Algorithm-for-Securing-Big-Data

---
## Overview

⚠️ This project is currently a work in progress.

This project simulates a secure Hadoop-like environment using Python, demonstrating how data can be safely stored and retrieved using encryption, key management, and user authentication.

It implements a simplified version of:

* HDFS (Hadoop Distributed File System)
* KMS (Key Management Server)
* Secure file upload/download with encryption
* GUI-based interaction with login/register system

---

## Features

* Simulated HDFS storage system (`hdfs_storage/`)
* Secure file upload & download through GUI
* Encryption of files before storage
* Key management using a KMS module
* Metadata tracking using `metadata.json`
* Logging system (`log.txt`)
* Automatic decrypted file output
* User authentication system (Login/Register)
* SQLite database for storing user credentials
* Password hashing using SHA-256

---

## Security Implementation

### Encryption Approach

* Symmetric Encryption (Fernet / AES-based) used to encrypt file data
* Asymmetric Encryption (RSA) used to encrypt the DEK (Data Encryption Key)
* Passwords stored securely using hashing (SHA-256)

---

### Key Flow

* DEK (Data Encryption Key) → encrypts file
* RSA → encrypts DEK → becomes EDEK
* EDEK stored in `metadata.json`
* Passwords → hashed → stored in database

---

## System Components

### KMS (Key Management Server)

* Generates DEK
* Encrypts DEK using RSA
* Decrypts DEK when required

---

### HDFS (Simulation)

* Stores encrypted files in `hdfs_storage/`
* Stores EDEK in `metadata.json`

---

### Client

* Handles:

  * File upload
  * File download
* Performs encryption & decryption

---

### GUI (Tkinter)

* Provides user-friendly interface
* Allows file selection and operations
* Displays success/error messages

---

### Authentication System

* Login and Registration interface
* User credentials stored in SQLite database (`users.db`)
* Passwords hashed using SHA-256 for security

---

## Project Structure

```
CRYPTO/
│
├── hdfs_storage/            # Simulated distributed storage
├── main.py                  # Core encryption logic (KMS, HDFS, Client)
├── gui.py                   # GUI + Login/Register system
├── users.db                 # SQLite database for users
├── metadata.json            # Stores encrypted keys (EDEK)
├── log.txt                  # Activity logs
├── decrypted_*              # Output files after decryption
```

---

## Working

### Login Flow

1. User enters username and password
2. Password is hashed using SHA-256
3. Verified against SQLite database
4. Access granted if valid

---

### Upload Flow

1. User selects file through GUI
2. KMS generates DEK
3. DEK is encrypted using RSA → EDEK
4. File is encrypted using DEK
5. Encrypted file stored in HDFS
6. EDEK stored in metadata

---

### Download Flow

1. Encrypted file + EDEK fetched
2. KMS decrypts EDEK → DEK
3. File decrypted using DEK
4. Output saved as `decrypted_<filename>`
