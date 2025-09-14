from cryptography.fernet import Fernet
import os
import sys
import json
import getpass
import base64
import argparse

# Starter code for cryptographic operations
def derive_key_from_password(password: str, salt: bytes = None) -> tuple:
    """
    Derive an encryption key from a password.
    Returns (key, salt) tuple.
    """
    if salt is None:
        salt = os.urandom(16)
    
    # Simple key derivation (already configured for security)
    key = base64.urlsafe_b64encode(
        (password + salt.hex())[:32].encode().ljust(32, b'0')
    )
    return key, salt

def encrypt_data(data: str, key: bytes) -> bytes:
    """Encrypt string data using Fernet (AES)"""
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes, key: bytes) -> str:
    """Decrypt data using Fernet (AES)"""
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()

# End starter code

VAULT_FILE = "passwords.vault"
SALT_FILE = "salt.key"

def init_vault(master_password):
    """Create a new password vault with the given master password"""
    if os.path.exists(VAULT_FILE):
        overwrite = input("Vault already exists. Overwrite? (y/N): ")
        if overwrite.lower() != 'y':
            print("Vault initialization cancelled.")
            return
    
    # Derive key and save salt
    key, salt = derive_key_from_password(master_password)
    
    # Create empty vault dictionary
    vault_data = {}
    
    try:
        # Encrypt and save vault
        encrypted_vault = encrypt_data(json.dumps(vault_data), key)
        
        with open(VAULT_FILE, 'wb') as f:
            f.write(encrypted_vault)
        
        with open(SALT_FILE, 'wb') as f:
            f.write(salt)
        
        print("✅ Vault created successfully!")
    except Exception as e:
        print(f"Error creating vault: {e}")
        sys.exit(1)

def load_vault(master_password):
    """Load and decrypt the vault using the master password"""
    if not os.path.exists(VAULT_FILE) or not os.path.exists(SALT_FILE):
        print("No vault found. Use 'init' to create one")
        return None
    
    try:
        # Load salt
        with open(SALT_FILE, 'rb') as f:
            salt = f.read()
        
        # Derive key from master password and salt
        key, _ = derive_key_from_password(master_password, salt)
        
        # Load and decrypt vault
        with open(VAULT_FILE, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = decrypt_data(encrypted_data, key)
        return json.loads(decrypted_data)
    
    except Exception:
        print("Incorrect master password")
        return None

def save_vault(vault_data, master_password):
    """Encrypt and save the vault data"""
    try:
        # Load salt
        with open(SALT_FILE, 'rb') as f:
            salt = f.read()
        
        # Derive key
        key, _ = derive_key_from_password(master_password, salt)
        
        # Encrypt and save
        encrypted_vault = encrypt_data(json.dumps(vault_data), key)
        
        with open(VAULT_FILE, 'wb') as f:
            f.write(encrypted_vault)
        
        return True
    except Exception as e:
        print(f"Error saving vault: {e}")
        return False

def add_password(website, username, password, master_password):
    """Add a new password entry to the vault"""
    # Input validation
    if not website or not username or not password:
        print("Error: Website, username, and password cannot be empty")
        return
    
    if len(website) > 200 or len(username) > 200 or len(password) > 200:
        print("Error: Input too long (max 200 characters)")
        return
    
    # Load vault
    vault_data = load_vault(master_password)
    if vault_data is None:
        return
    
    # Add new entry
    vault_data[website] = {
        'username': username,
        'password': password
    }
    
    # Save vault
    if save_vault(vault_data, master_password):
        print(f"  Password added for {website}")
    else:
        print("Failed to save password")

def get_password(website, master_password):
    """Retrieve password for a website"""
    # Input validation
    if not website:
        print("Error: Website cannot be empty")
        return
    
    # Load vault
    vault_data = load_vault(master_password)
    if vault_data is None:
        return
    
    # Check if website exists
    if website not in vault_data:
        print(f"No password found for {website}")
        return
    
    # Display credentials
    entry = vault_data[website]
    print(f"   {website} credentials:")
    print(f"   Username: {entry['username']}")
    print(f"   Password: {entry['password']}")

def list_websites(master_password):
    """List all websites in the vault"""
    # Load vault
    vault_data = load_vault(master_password)
    if vault_data is None:
        return
    
    if not vault_data:
        print("No passwords stored in vault")
        return
    
    print("📋 Stored passwords:")
    for website, entry in vault_data.items():
        print(f"   - {website} ({entry['username']})")

def main():
    parser = argparse.ArgumentParser(description="Password Vault - Secure Password Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Create a new password vault')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new password')
    add_parser.add_argument('website', help='Website name')
    add_parser.add_argument('username', help='Username')
    add_parser.add_argument('password', help='Password')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Retrieve a password')
    get_parser.add_argument('website', help='Website name')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all stored websites')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'init':
        master_password = getpass.getpass("Enter master password: ")
        confirm_password = getpass.getpass("Confirm master password: ")
        
        if master_password != confirm_password:
            print("Passwords do not match!")
            return
        
        if len(master_password) < 6:
            print("Master password must be at least 6 characters long")
            return
        
        init_vault(master_password)
    
    elif args.command == 'add':
        master_password = getpass.getpass("Enter master password: ")
        add_password(args.website, args.username, args.password, master_password)
    
    elif args.command == 'get':
        master_password = getpass.getpass("Enter master password: ")
        get_password(args.website, master_password)
    
    elif args.command == 'list':
        master_password = getpass.getpass("Enter master password: ")
        list_websites(master_password)

if __name__ == "__main__":
    main()