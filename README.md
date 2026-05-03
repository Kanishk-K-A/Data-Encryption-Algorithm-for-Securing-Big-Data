# Data-Encryption-Algorithm-for-Securing-Big-Data
# Secure HDFS Encryption System 
## Overview

This project simulates a secure Hadoop-like environment using Python, demonstrating how data can be safely stored and retrieved using encryption and key management techniques.

It implements a simplified version of:

* HDFS (Hadoop Distributed File System)
* KMS (Key Management Server)
* Secure file upload/download with encryption

---

## Features

* Simulated HDFS storage system (`hdfs_storage/`)
* Secure file upload & download
* Encryption of files before storage
* Key management using a KMS module
* Metadata tracking using `metadata.json`
* Logging system (`log.txt`)
* Automatic decrypted file output

---

## Security Implementation

### Encryption Approach

* Symmetric Encryption (Fernet / AES-based) used to encrypt file data
* Asymmetric Encryption (RSA) used to encrypt the DEK (Data Encryption Key)

### Key Flow

* DEK (Data Encryption Key) → encrypts file
* RSA → encrypts DEK → becomes EDEK
* EDEK stored in `metadata.json`

---

## System Components

### KMS (Key Management Server)

* Generates DEK
* Encrypts DEK using RSA
* Decrypts DEK when required

### HDFS (Simulation)

* Stores encrypted files in `hdfs_storage/`
* Stores EDEK in `metadata.json`

### Client

* Handles:

  * File upload
  * File download
* Performs encryption & decryption

---

## Project Structure

```
CRYPTO/
│
├── hdfs_storage/            # Simulated distributed storage
├── main.py                  # Main program (core logic)
├── metadata.json            # Stores encrypted keys (EDEK)
├── log.txt                  # Activity logs
├── decrypted_*.pdf          # Output files after decryption
```

---

## Working

### Upload Flow

1. User selects file
2. KMS generates DEK
3. DEK is encrypted using RSA → EDEK
4. File is encrypted using DEK
5. Encrypted file stored in HDFS
6. EDEK stored in metadata

### Download Flow

1. Encrypted file + EDEK fetched
2. KMS decrypts EDEK → DEK
3. File decrypted using DEK
4. Output saved as `decrypted_<filename>`

---

## Work in Progress

This project is currently a **work in progress** and is intended for learning and demonstration purposes.

