# Quantum Security — Post-Quantum Cryptography Foundation

Provides quantum-resistant cryptographic primitives for Robot City.

---

## Supported Algorithms

| Category | Algorithm | NIST Status |
|---|---|---|
| Digital Signature | ML-DSA-44 (Dilithium 2) | FIPS 204 (2024) |
| Digital Signature | ML-DSA-65 (Dilithium 3) | FIPS 204 (2024) |
| Digital Signature | ML-DSA-87 (Dilithium 5) | FIPS 204 (2024) |
| Key Encapsulation | ML-KEM-512 (Kyber 512) | FIPS 203 (2024) |
| Key Encapsulation | ML-KEM-768 (Kyber 768) | FIPS 203 (2024) |
| Key Encapsulation | ML-KEM-1024 (Kyber 1024) | FIPS 203 (2024) |
| Hash-based Signature | SPHINCS+ | FIPS 205 (2024) |
| Lattice Signature | FALCON-512 | Round 3 finalist |
| Lattice Signature | FALCON-1024 | Round 3 finalist |

---

## Current Status

| Component | Status | Notes |
|---|---|---|
| `PQCWrapper.hash_message` | ✅ **Real** | SHA3-256 via stdlib hashlib |
| `PQCWrapper.sign` | ⚠️ Placeholder | Requires `liboqs` |
| `PQCWrapper.verify` | ⚠️ Placeholder | Requires `liboqs` |
| `KeyManager.generate_key_bundle` | ⚠️ Placeholder | Requires `liboqs` |
| `SecureTransport.encrypt` | ⚠️ Placeholder | Requires `liboqs` |
| `SecureTransport.decrypt` | ⚠️ Placeholder | Requires `liboqs` |

---

## Quick Start

### Hashing (works now — no extra libraries needed)

```python
from quantum_security import PQCWrapper

pqc = PQCWrapper()
digest = pqc.hash_message(b"Robot City transaction data")
print(digest)  # SHA3-256 hex string
```

### Signing (placeholder)

```python
from quantum_security import PQCWrapper, PQCAlgorithm, KeyManager

km = KeyManager()
bundle = km.generate_key_bundle("robot_42_signing_key", PQCAlgorithm.ML_DSA_65)

pqc = PQCWrapper()
result = pqc.sign(b"my important message", key_id=bundle.key_id)
print(result.is_placeholder)   # True — install liboqs for real signing
print(result.to_dict())
```

### Key Management

```python
from quantum_security import KeyManager, PQCAlgorithm

km = KeyManager()

# Generate (placeholder keypair)
bundle = km.generate_key_bundle("key1", PQCAlgorithm.ML_KEM_768)

# List
print(km.list_keys())

# Rotate
new_bundle = km.rotate_key("key1")

# Stats
print(km.get_stats())
```

### Secure Transport (placeholder)

```python
from quantum_security import SecureTransport, PQCAlgorithm

transport = SecureTransport()
channel = transport.establish_secure_channel("robot_A", "robot_B")
print(channel)

# Encrypt (placeholder ciphertext)
msg = transport.encrypt(b"secret payload", recipient_key_id="robot_B_key")
print(msg.is_placeholder)  # True
```

---

## Activating Real PQC (liboqs-python)

```bash
# Install the Open Quantum Safe library
pip install liboqs
```

Then update `pqc_wrapper.py` signing to:

```python
import oqs
signer = oqs.Signature("ML-DSA-65")
public_key = signer.generate_keypair()
signature = signer.sign(message)
```

And `secure_transport.py` encryption to:

```python
import oqs
kem = oqs.KeyEncapsulation("ML-KEM-768")
ciphertext, shared_secret = kem.encap_secret(recipient_public_key)
# Use shared_secret with AES-256-GCM to encrypt message
```

---

## Security Notes

1. **Never store private keys** — `KeyBundle` holds public keys only.
2. **Check `is_placeholder`** — Before trusting any signature or ciphertext, verify this flag is `False`.
3. **SHA3-256 is real** — `PQCWrapper.hash_message` is a genuine cryptographic hash.
4. **HSM integration** — For production, key generation and signing should happen inside a Hardware Security Module.

---

## Module Structure

```
quantum-security/
├── __init__.py           # Public API
├── pqc_wrapper.py        # PQCWrapper, PQCAlgorithm, SignatureResult, VerificationResult
├── key_manager.py        # KeyManager, KeyBundle
└── secure_transport.py   # SecureTransport, EncryptedMessage
```
