# Data-Encryption-Algorithm-for-Securing-Big-Data
# 🔐 Secure HDFS Encryption System (CryptoPro)

## 📌 Overview

This project simulates a **secure Hadoop-like environment** using Python, demonstrating how data can be safely stored and retrieved using encryption and key management techniques.

It implements a simplified version of:

* **HDFS (Hadoop Distributed File System)**
* **KMS (Key Management Server)**
* Secure file upload/download with encryption

---

## 🚀 Features

* Simulated HDFS storage system (`hdfs_storage/`)
* Secure file upload & download
* Encryption of files before storage
* Key management using a KMS module
* Metadata tracking using `metadata.json`
* Logging system (`log.txt`)
* Automatic decrypted file output

---

## 🔐 Security Implementation

### 🔹 Encryption Approach

* **Symmetric Encryption (Fernet / AES-based)** used to encrypt file data
* **Asymmetric Encryption (RSA)** used to encrypt the DEK (Data Encryption Key)

### 🔹 Key Flow

* DEK (Data Encryption Key) → encrypts file
* RSA → encrypts DEK → becomes EDEK
* EDEK stored in `metadata.json`

---

## 🧩 System Components

### 1️⃣ KMS (Key Management Server)

* Generates DEK
* Encrypts DEK using RSA
* Decrypts DEK when required

### 2️⃣ HDFS (Simulation)

* Stores encrypted files in `hdfs_storage/`
* Stores EDEK in `metadata.json`

### 3️⃣ Client

* Handles:

  * File upload
  * File download
* Performs encryption & decryption

---

## ⚙️ Project Structure

```
CRYPTOpro/
│
├── hdfs_storage/            # Simulated distributed storage
├── main.py                  # Main program (core logic)
├── metadata.json            # Stores encrypted keys (EDEK)
├── log.txt                  # Activity logs
├── decrypted_*.pdf          # Output files after decryption
```

---

## 🔄 How It Works

### 📥 Upload Flow

1. User selects file
2. KMS generates DEK
3. DEK is encrypted using RSA → EDEK
4. File is encrypted using DEK
5. Encrypted file stored in HDFS
6. EDEK stored in metadata

---

### 📤 Download Flow

1. Encrypted file + EDEK fetched
2. KMS decrypts EDEK → DEK
3. File decrypted using DEK
4. Output saved as `decrypted_<filename>`

---

## ▶️ How to Run

```bash
python main.py
```

Then choose:

* 1 → Upload file
* 2 → Download file
* 3 → Exit

---

## ⚠️ Work in Progress

This project is currently a **work in progress** and is intended for learning and demonstration purposes.

### Planned Improvements:

* Real distributed HDFS integration
* Persistent key storage for KMS
* User authentication system
* Better error handling
* Performance optimization
* UI / API interface

---

## 📌 Limitations

* KMS keys are not persisted (regenerated each run)
* Local file system used instead of real HDFS cluster
* No authentication/authorization layer
* Basic logging only

---

## 👨‍💻 Author

Kanishk K A

---

## 📄 Note

This project demonstrates the concepts of:

* Data at rest encryption
* Key management
* Secure file handling in distributed systems

It is not intended for production use.
