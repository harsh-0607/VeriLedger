import json
import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

class CryptoManager:
    @staticmethod
    def generate_key_pair() -> tuple[bytes, bytes]:
        """Generates a secp256r1 ECDSA key pair."""
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()

        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem_private, pem_public

    @staticmethod
    def sign_data(data: dict, private_key_pem: bytes) -> str:
        """Signs a deterministic JSON string representation of the data."""
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        
        # Sort keys to ensure deterministic serialization
        payload = json.dumps(data, sort_keys=True, separators=(',', ':')).encode('utf-8')
        
        signature = private_key.sign(
            payload,
            ec.ECDSA(hashes.SHA256())
        )
        return base64.b64encode(signature).decode('utf-8')

    @staticmethod
    def verify_signature(data: dict, signature_b64: str, public_key_pem: bytes) -> bool:
        """Verifies the ECDSA signature against the provided data and public key."""
        try:
            public_key = serialization.load_pem_public_key(public_key_pem)
            payload = json.dumps(data, sort_keys=True, separators=(',', ':')).encode('utf-8')
            signature = base64.b64decode(signature_b64)
            
            public_key.verify(
                signature,
                payload,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except (InvalidSignature, ValueError):
            return False
