import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# -------------------------------
# KMS (Key Management Server)
# -------------------------------
class KMS:
    def __init__(self):
        print("[KMS] Initializing Key Management Server...")

        # RSA Keys (for encrypting DEK)
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def generate_DEK(self):
        print("[KMS] Generating Data Encryption Key (DEK)")
        return Fernet.generate_key()

    def encrypt_DEK(self, dek):
        print("[KMS] Encrypting DEK -> EDEK using RSA")
        edek = self.public_key.encrypt(
            dek,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return edek

    def decrypt_DEK(self, edek):
        print("[KMS] Decrypting EDEK -> DEK")
        dek = self.private_key.decrypt(
            edek,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return dek


# -------------------------------
# HDFS Simulation
# -------------------------------
class HDFS:
    def __init__(self):
        self.storage_path = "hdfs_storage"
        self.meta_file = "metadata.json"

        os.makedirs(self.storage_path, exist_ok=True)

        if not os.path.exists(self.meta_file):
            with open(self.meta_file, "w") as f:
                json.dump({}, f)

    def write(self, filename, encrypted_data, edek):
        print("[HDFS] Writing encrypted file to storage")

        # Save encrypted file
        with open(os.path.join(self.storage_path, filename), "wb") as f:
            f.write(encrypted_data)

        # Save metadata (EDEK)
        with open(self.meta_file, "r") as f:
            metadata = json.load(f)

        metadata[filename] = base64.b64encode(edek).decode()

        with open(self.meta_file, "w") as f:
            json.dump(metadata, f, indent=4)

    def read(self, filename):
        print("[HDFS] Reading encrypted file from storage")

        with open(os.path.join(self.storage_path, filename), "rb") as f:
            encrypted_data = f.read()

        with open(self.meta_file, "r") as f:
            metadata = json.load(f)

        edek = base64.b64decode(metadata[filename])

        return encrypted_data, edek


# -------------------------------
# Client
# -------------------------------
class Client:
    def __init__(self, kms, hdfs):
        self.kms = kms
        self.hdfs = hdfs

    def upload_file(self, filepath):
        print("\n--- UPLOAD PROCESS ---")

        filename = os.path.basename(filepath)

        # Read file
        with open(filepath, "rb") as f:
            data = f.read()

        # Step 1: Generate DEK
        dek = self.kms.generate_DEK()

        # Step 2: Encrypt DEK -> EDEK
        edek = self.kms.encrypt_DEK(dek)

        # Step 3: Encrypt file using DEK
        cipher = Fernet(dek)
        encrypted_data = cipher.encrypt(data)

        # Step 4: Store in HDFS
        self.hdfs.write(filename, encrypted_data, edek)

        print("[CLIENT] File uploaded securely!")

    def download_file(self, filename):
        print("\n--- DOWNLOAD PROCESS ---")

        # Step 1: Get encrypted data + EDEK
        encrypted_data, edek = self.hdfs.read(filename)

        # Step 2: Decrypt EDEK -> DEK
        dek = self.kms.decrypt_DEK(edek)

        # Step 3: Decrypt data
        cipher = Fernet(dek)
        decrypted_data = cipher.decrypt(encrypted_data)

        # Save output file
        output_file = "decrypted_" + filename
        with open(output_file, "wb") as f:
            f.write(decrypted_data)

        print(f"[CLIENT] File downloaded and saved as {output_file}")


# -------------------------------
# Logger (extra feature)
# -------------------------------
def log_event(message):
    with open("log.txt", "a") as f:
        f.write(message + "\n")


# -------------------------------
# Main Program
# -------------------------------
if __name__ == "__main__":
    print("===== SECURE HDFS ENCRYPTION SYSTEM =====")

    kms = KMS()
    hdfs = HDFS()
    client = Client(kms, hdfs)

    while True:
        print("\n1. Upload File")
        print("2. Download File")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            path = input("Enter file path: ")
            client.upload_file(path)
            log_event("File uploaded: " + path)

        elif choice == "2":
            filename = input("Enter filename: ")
            client.download_file(filename)
            log_event("File downloaded: " + filename)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")
