
from app.crypto import CryptoManager

def test_sign_and_verify():
    priv, pub = CryptoManager.generate_key_pair()
    data = {"student": "Alice", "degree": "CS"}
    
    signature = CryptoManager.sign_data(data, priv)
    assert signature is not None
    
    is_valid = CryptoManager.verify_signature(data, signature, pub)
    assert is_valid is True

def test_invalid_signature():
    priv1, _ = CryptoManager.generate_key_pair()
    _, pub2 = CryptoManager.generate_key_pair()
    data = {"student": "Bob"}
    
    signature = CryptoManager.sign_data(data, priv1)
    is_valid = CryptoManager.verify_signature(data, signature, pub2) # Wrong public key
    assert is_valid is False
