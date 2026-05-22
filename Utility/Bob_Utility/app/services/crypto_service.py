"""
Cryptography Service
Provides encryption and decryption functionality
"""

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from typing import Optional
from app.services.base import BaseService
from app.core.exceptions import ValidationError, ProcessingError


class CryptoService(BaseService):
    """Service for encryption and decryption operations"""
    
    def __init__(self):
        super().__init__()
        self.logger.info("Initialized CryptoService")
    
    def _derive_key(self, password: str, salt: Optional[bytes] = None) -> tuple[bytes, bytes]:
        """
        Derive a key from password using PBKDF2
        
        Args:
            password: Password to derive key from
            salt: Salt for key derivation (generated if not provided)
            
        Returns:
            Tuple of (derived_key, salt)
        """
        if salt is None:
            salt = b'enterprise_payload_toolkit_salt_2024'  # Fixed salt for consistency
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def encrypt(self, text: str, key: str) -> str:
        """
        Encrypt text using the provided key
        
        Args:
            text: Plain text to encrypt
            key: Encryption key (password)
            
        Returns:
            Encrypted text (base64 encoded)
            
        Raises:
            ValidationError: If text or key is empty
            ProcessingError: If encryption fails
        """
        try:
            if not text or not text.strip():
                raise ValidationError("Text to encrypt cannot be empty")
            
            if not key or not key.strip():
                raise ValidationError("Encryption key cannot be empty")
            
            # Derive key from password
            derived_key, _ = self._derive_key(key)
            
            # Create Fernet cipher
            cipher = Fernet(derived_key)
            
            # Encrypt the text
            encrypted_bytes = cipher.encrypt(text.encode('utf-8'))
            
            # Return base64 encoded string
            encrypted_text = encrypted_bytes.decode('utf-8')
            
            self.logger.info("Successfully encrypted text")
            return encrypted_text
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"Encryption failed: {str(e)}")
            raise ProcessingError(f"Failed to encrypt text: {str(e)}")
    
    def decrypt(self, encrypted_text: str, key: str) -> str:
        """
        Decrypt encrypted text using the provided key
        
        Args:
            encrypted_text: Encrypted text (base64 encoded)
            key: Decryption key (password)
            
        Returns:
            Decrypted plain text
            
        Raises:
            ValidationError: If encrypted_text or key is empty
            ProcessingError: If decryption fails
        """
        try:
            if not encrypted_text or not encrypted_text.strip():
                raise ValidationError("Encrypted text cannot be empty")
            
            if not key or not key.strip():
                raise ValidationError("Decryption key cannot be empty")
            
            # Derive key from password
            derived_key, _ = self._derive_key(key)
            
            # Create Fernet cipher
            cipher = Fernet(derived_key)
            
            # Decrypt the text
            decrypted_bytes = cipher.decrypt(encrypted_text.encode('utf-8'))
            
            # Return decoded string
            decrypted_text = decrypted_bytes.decode('utf-8')
            
            self.logger.info("Successfully decrypted text")
            return decrypted_text
            
        except ValidationError:
            raise
        except Exception as e:
            self.logger.error(f"Decryption failed: {str(e)}")
            raise ProcessingError(f"Failed to decrypt text: {str(e)}")
    
    def generate_key(self) -> str:
        """
        Generate a random encryption key
        
        Returns:
            Random key as base64 string
        """
        try:
            key = Fernet.generate_key()
            self.logger.info("Successfully generated encryption key")
            return key.decode('utf-8')
        except Exception as e:
            self.logger.error(f"Key generation failed: {str(e)}")
            raise ProcessingError(f"Failed to generate key: {str(e)}")
    
    def get_sample_text(self) -> str:
        """Get sample text for testing"""
        return "This is a secret message that needs to be encrypted for security purposes."
    
    def get_sample_key(self) -> str:
        """Get sample key for testing"""
        return "MySecretKey123!"


# Made with Bob