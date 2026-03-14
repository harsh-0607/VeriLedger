
from app.blockchain import Blockchain

def test_blockchain_integrity():
    bc = Blockchain(difficulty=2)
    bc.add_block({"data": "block 1"})
    bc.add_block({"data": "block 2"})
    
    assert bc.is_chain_valid() is True

def test_blockchain_tampering():
    bc = Blockchain(difficulty=2)
    bc.add_block({"data": "block 1"})
    
    # Tamper with block data
    bc.chain[1].data = {"data": "tampered"}
    assert bc.is_chain_valid() is False
