import hashlib
import json
from fastapi import FastAPI, HTTPException
from .models import IssueRequest, VerifyRequest
from .crypto import CryptoManager
from .blockchain import Blockchain
from .storage import Storage

app = FastAPI(title="VeriLedger API", description="Decentralized Credential Verification System")
blockchain = Blockchain(difficulty=3)

@app.on_event("startup")
def startup_event():
    Storage.load_chain(blockchain)

@app.post("/issue")
def issue_credential(req: IssueRequest):
    data_dict = req.credential.model_dump()
    
    try:
        # Sign the credential
        signature = CryptoManager.sign_data(data_dict, req.private_key_pem.encode('utf-8'))
        
        # Package the ledger payload
         data_bytes = json.dumps(data_dict, sort_keys=True).encode('utf-8')
        credential_hash = hashlib.sha256(data_bytes).hexdigest()
        
        # Package the ledger payload
        ledger_entry = {
            "credential_hash": credential_hash,
            "signature": signature
        }
        
        # Add to immutable ledger
        new_block = blockchain.add_block(ledger_entry)
        Storage.save_chain(blockchain)
        
        return {
            "message": "Credential issued and logged to blockchain successfully.",
            "signature": signature,
            "block_index": new_block.index
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/verify")
def verify_credential(req: VerifyRequest):
    data_dict = req.credential.model_dump()
    
    is_valid_crypto = CryptoManager.verify_signature(
        data_dict, 
        req.signature, 
        req.public_key_pem.encode('utf-8')
    )
    
    if not is_valid_crypto:
        return {"valid": False, "reason": "Cryptographic signature is invalid."}

    # Verify chain integrity
    if not blockchain.is_chain_valid():
        return {"valid": False, "reason": "Blockchain integrity compromised."}

    # Search ledger for the signature to ensure it wasn't revoked/omitted
    found = any(block.data.get("signature") == req.signature for block in blockchain.chain)
    
    if not found:
        return {"valid": False, "reason": "Credential not found on the immutable ledger."}

    return {"valid": True, "reason": "Credential is mathematically verified and present on the ledger."}

@app.get("/chain")
def get_chain():
    return {
        "chain": [block.to_dict() for block in blockchain.chain],
        "is_valid": blockchain.is_chain_valid(),
        "length": len(blockchain.chain)
    }

@app.get("/keys/generate")
def generate_keys():
    """Utility endpoint to generate keypairs for testing purposes."""
    priv, pub = CryptoManager.generate_key_pair()
    return {
        "private_key": priv.decode('utf-8'),
        "public_key": pub.decode('utf-8')
    }
