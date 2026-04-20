"""
InsurGuard Security Module
Implements RSA encryption and SHA-512 hashing for sensitive data protection
"""

import hashlib
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import base64


class InsurGuardSecurity:
    """Handles encryption and hashing for insurance data"""
    
    def __init__(self, key_size=2048):
        """Initialize RSA key pair"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def rsa_encrypt(self, plaintext: str) -> str:
        """
        Encrypt sensitive data using RSA public key
        
        Args:
            plaintext: Data to encrypt (User_ID or Personal_Health_Info)
            
        Returns:
            Base64-encoded encrypted data
        """
        ciphertext = self.public_key.encrypt(
            plaintext.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(ciphertext).decode()
    
    def rsa_decrypt(self, ciphertext_b64: str) -> str:
        """
        Decrypt RSA-encrypted data using private key
        
        Args:
            ciphertext_b64: Base64-encoded encrypted data
            
        Returns:
            Decrypted plaintext
        """
        ciphertext = base64.b64decode(ciphertext_b64)
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode()
    
    def sha512_hash(self, data: str) -> str:
        """
        Generate SHA-512 hash for data integrity verification
        
        Args:
            data: Data to hash (Claim_Records)
            
        Returns:
            SHA-512 hex digest
        """
        return hashlib.sha512(data.encode()).hexdigest()
    
    def verify_integrity(self, data: str, hash_value: str) -> bool:
        """
        Verify data integrity using SHA-512 hash
        
        Args:
            data: Original data
            hash_value: Expected hash value
            
        Returns:
            True if hash matches, False otherwise
        """
        return self.sha512_hash(data) == hash_value
    
    def get_public_key_pem(self) -> str:
        """Export public key in PEM format"""
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode()
    
    def get_private_key_pem(self) -> str:
        """Export private key in PEM format (for secure storage)"""
        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem.decode()


class DataProtectionManager:
    """Manages protection of sensitive dataframe columns"""
    
    def __init__(self):
        self.security = InsurGuardSecurity()
        self.encryption_registry = {}
        self.integrity_hashes = {}
    
    def protect_user_id(self, user_id: str) -> str:
        """Encrypt user ID using RSA"""
        encrypted = self.security.rsa_encrypt(str(user_id))
        self.encryption_registry[user_id] = encrypted
        return encrypted
    
    def protect_health_info(self, health_info: dict) -> str:
        """Encrypt personal health information"""
        health_json = json.dumps(health_info)
        encrypted = self.security.rsa_encrypt(health_json)
        return encrypted
    
    def protect_claim_records(self, claim_data: str) -> tuple:
        """
        Encrypt and hash claim records
        
        Returns:
            Tuple of (encrypted_data, sha512_hash)
        """
        encrypted = self.security.rsa_encrypt(claim_data)
        hash_value = self.security.sha512_hash(claim_data)
        self.integrity_hashes[claim_data] = hash_value
        return encrypted, hash_value
    
    def verify_claim_integrity(self, claim_data: str) -> bool:
        """Verify claim data hasn't been tampered with"""
        if claim_data not in self.integrity_hashes:
            return False
        return self.security.verify_integrity(
            claim_data,
            self.integrity_hashes[claim_data]
        )
