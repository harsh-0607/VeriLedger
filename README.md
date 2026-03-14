# VeriLedger

A decentralized Python-based credential verification system using ECDSA signatures and an immutable blockchain ledger. Built with Python 3.12+ and FastAPI.

## The Trust Triangle in VeriLedger

The system operates strictly on the principles of Decentralized Identity (DID), implementing the **Trust Triangle**:

1. **Issuer (University):** Generates a cryptographic keypair. They hash and sign the student's degree data using their Private Key, issuing the raw data + the signature to the Holder. They also write the hashed signature to the `VeriLedger` (Blockchain) to anchor it in time and prove it hasn't been revoked.
2. **Holder (Student):** Receives the raw JSON data and the Base64 signature. They *own* this data and present it securely to potential employers.
3. **Verifier (Employer):** The employer receives the JSON data and the signature from the Holder. Using the API (`/verify`), the employer fetches the University's known Public Key, mathematically verifies the ECDSA signature, and queries the Immutable Ledger to ensure the credential hasn't been tampered with or revoked since issuance.

Because of this architecture, **no central database** needs to be queried by the employer to view the private student records. The blockchain only stores cryptographic proofs (signatures/hashes), ensuring 100% GDPR compliance and data privacy while guaranteeing authenticity.

## Architectural Limitations

### Single-Node Storage (ledger.json)
This project uses a local `ledger.json` file for persistent storage. This is perfectly suited for local development, portfolio demonstration, and running Uvicorn with a single worker.

**Production Deployment Note:** 
If you intend to deploy this system to cloud platforms (like AWS, Heroku, or Docker) using multiple workers (e.g., `uvicorn main:app --workers 4`), the `ledger.json` approach will face concurrency limitations. A simple `threading.Lock()` cannot prevent race conditions across separate multi-processing workers. For a true multi-node or multi-worker production environment, you must replace `app/storage.py` with a robust database (such as PostgreSQL or MongoDB) that handles concurrent ACID transactions natively.

## Getting Started

### Prerequisites
- Python 3.12+
- `pip install -r requirements.txt`

### Running the App
```bash
uvicorn app.main:app --reload
```

### Running Tests
```bash
pytest
```