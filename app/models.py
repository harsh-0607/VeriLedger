from pydantic import BaseModel, Field
from typing import Dict, Any

class CredentialData(BaseModel):
    student_id: str = Field(..., description="Unique ID of the student")
    name: str = Field(..., description="Full name of the student")
    degree: str = Field(..., description="Degree obtained")
    graduation_year: int = Field(..., description="Year of graduation")

class IssueRequest(BaseModel):
    credential: CredentialData
    private_key_pem: str = Field(..., description="Issuer's private key in PEM format")

class VerifyRequest(BaseModel):
    credential: CredentialData
    signature: str = Field(..., description="Base64 encoded ECDSA signature")
    public_key_pem: str = Field(..., description="Issuer's public key in PEM format")
