import json
import os
from .blockchain import Blockchain, Block

CHAIN_FILE = "ledger.json"
file_lock = threading.Lock()

class Storage:
    @staticmethod
    def save_chain(blockchain: Blockchain):
        with file_lock:
            with open(CHAIN_FILE, 'w') as f:
                json.dump([block.to_dict() for block in blockchain.chain], f, indent=4)

    @staticmethod
    def load_chain(blockchain: Blockchain):
        with file_lock:
            if not os.path.exists(CHAIN_FILE):
                 with open(CHAIN_FILE, 'w') as f:
                    json.dump([block.to_dict() for block in blockchain.chain], f, indent=4)
                return

        with open(CHAIN_FILE, 'r') as f:
            try:
                data = json.load(f)
                blockchain.chain = []
                for b_dict in data:
                    block = Block(
                        index=b_dict["index"],
                        timestamp=b_dict["timestamp"],
                        data=b_dict["data"],
                        previous_hash=b_dict["previous_hash"],
                        nonce=b_dict["nonce"]
                    )
                    block.hash = b_dict["hash"]
                    blockchain.chain.append(block)
            except json.JSONDecodeError:
                Storage.save_chain(blockchain)
