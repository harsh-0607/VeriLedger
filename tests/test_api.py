from fastapi.testclient import TestClient
from app.main import app
from app.crypto import CryptoManager

client = TestClient(app)

def test_issue_and_verify_flow():
    # 1. Generate keys
    priv, pub = CryptoManager.generate_key_pair()
    priv_str = priv.decode('utf-8')
    pub_str = pub.decode('utf-8')
    
    credential = {
        "student_id": "123",
        "name": "Charlie",
        "degree": "Math",
        "graduation_year": 2026
    }
    
    # 2. Issue credential
    issue_resp = client.post("/issue", json={
        "credential": credential,
        "private_key_pem": priv_str
    })
    assert issue_resp.status_code == 200
    signature = issue_resp.json()["signature"]
    
    # 3. Verify credential
    verify_resp = client.post("/verify", json={
        "credential": credential,
        "signature": signature,
        "public_key_pem": pub_str
    })
    
    assert verify_resp.status_code == 200
    assert verify_resp.json()["valid"] is True
