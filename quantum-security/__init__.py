"""
quantum-security — Post-Quantum Security Foundation
Provides quantum-resistant cryptography wrappers, signing/verification
abstractions, key management abstractions, and secure transport helpers.
Note: Some implementations are placeholders pending real PQC library integration.
"""
from pqc_wrapper import PQCWrapper, PQCAlgorithm, SignatureResult, VerificationResult
from key_manager import KeyManager, KeyBundle
from secure_transport import SecureTransport, EncryptedMessage

__all__ = [
    "PQCWrapper",
    "PQCAlgorithm",
    "SignatureResult",
    "VerificationResult",
    "KeyManager",
    "KeyBundle",
    "SecureTransport",
    "EncryptedMessage",
]
