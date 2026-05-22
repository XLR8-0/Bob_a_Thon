"""
Security Tools API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app.core.exceptions import ValidationError, ProcessingError
from app.services.crypto_service import CryptoService

router = APIRouter(prefix="/security", tags=["Security Tools"])


# Request/Response Models
class EncryptRequest(BaseModel):
    text: str = Field(..., description="Text to encrypt")
    key: str = Field(..., description="Encryption key")
    use_sample: bool = Field(False, description="Use sample data instead")


class DecryptRequest(BaseModel):
    encrypted_text: str = Field(..., description="Encrypted text to decrypt")
    key: str = Field(..., description="Decryption key")
    use_sample: bool = Field(False, description="Use sample data instead")


class CryptoResponse(BaseModel):
    success: bool
    result: str
    message: Optional[str] = None


class GenerateKeyResponse(BaseModel):
    success: bool
    key: str
    message: Optional[str] = None


class SampleDataResponse(BaseModel):
    success: bool
    sample_text: Optional[str] = None
    sample_key: Optional[str] = None
    sample_encrypted: Optional[str] = None


# Encrypt Text
@router.post("/encrypt", response_model=CryptoResponse)
async def encrypt_text(request: EncryptRequest) -> CryptoResponse:
    """Encrypt text using the provided key"""
    try:
        service = CryptoService()
        
        # Use sample data if requested
        if request.use_sample:
            text = service.get_sample_text()
            key = service.get_sample_key()
        else:
            text = request.text
            key = request.key
        
        if not text or not text.strip():
            raise ValidationError("Text to encrypt is required")
        
        if not key or not key.strip():
            raise ValidationError("Encryption key is required")
        
        result = service.encrypt(text=text, key=key)
        
        return CryptoResponse(
            success=True,
            result=result,
            message="Successfully encrypted text"
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")


# Decrypt Text
@router.post("/decrypt", response_model=CryptoResponse)
async def decrypt_text(request: DecryptRequest) -> CryptoResponse:
    """Decrypt encrypted text using the provided key"""
    try:
        service = CryptoService()
        
        # Use sample data if requested
        if request.use_sample:
            # First encrypt sample text to get encrypted version
            sample_text = service.get_sample_text()
            sample_key = service.get_sample_key()
            encrypted_text = service.encrypt(sample_text, sample_key)
            key = sample_key
        else:
            encrypted_text = request.encrypted_text
            key = request.key
        
        if not encrypted_text or not encrypted_text.strip():
            raise ValidationError("Encrypted text is required")
        
        if not key or not key.strip():
            raise ValidationError("Decryption key is required")
        
        result = service.decrypt(encrypted_text=encrypted_text, key=key)
        
        return CryptoResponse(
            success=True,
            result=result,
            message="Successfully decrypted text"
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")


# Generate Random Key
@router.get("/generate-key", response_model=GenerateKeyResponse)
async def generate_key() -> GenerateKeyResponse:
    """Generate a random encryption key"""
    try:
        service = CryptoService()
        key = service.generate_key()
        
        return GenerateKeyResponse(
            success=True,
            key=key,
            message="Successfully generated encryption key"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Key generation failed: {str(e)}")


# Get Sample Data
@router.get("/sample", response_model=SampleDataResponse)
async def get_sample_data() -> SampleDataResponse:
    """Get sample data for testing encryption/decryption"""
    try:
        service = CryptoService()
        sample_text = service.get_sample_text()
        sample_key = service.get_sample_key()
        
        # Generate sample encrypted text
        sample_encrypted = service.encrypt(sample_text, sample_key)
        
        return SampleDataResponse(
            success=True,
            sample_text=sample_text,
            sample_key=sample_key,
            sample_encrypted=sample_encrypted
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sample data: {str(e)}")


# Made with Bob