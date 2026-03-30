"""
pqc_wrapper.py — Post-Quantum Cryptography wrapper.

Real PQC signing (ML-DSA / Dilithium, FALCON, SPHINCS+) requires
either ``liboqs-python`` (``pip install liboqs``) or ``pqcrypto``
(``pip install pqcrypto``).  Until those libraries are installed, all
signing/verification operations return clearly marked placeholder results.

SHA3-256 hashing is fully implemented using the standard library.
"""

from __future__ import annotations

import hashlib
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class PQCAlgorithm(Enum):
    """Supported post-quantum cryptographic algorithms."""

    # NIST ML-DSA (formerly CRYSTALS-Dilithium) — signature schemes
    ML_DSA_44 = "ML-DSA-44"
    ML_DSA_65 = "ML-DSA-65"
    ML_DSA_87 = "ML-DSA-87"

    # NIST ML-KEM (formerly CRYSTALS-Kyber) — key encapsulation
    ML_KEM_512 = "ML-KEM-512"
    ML_KEM_768 = "ML-KEM-768"
    ML_KEM_1024 = "ML-KEM-1024"

    # Hash-based signature schemes
    SPHINCS_PLUS = "SPHINCS+"
    FALCON_512 = "FALCON-512"
    FALCON_1024 = "FALCON-1024"


@dataclass
class SignatureResult:
    """
    Result of a PQC signing operation.

    Attributes
    ----------
    algorithm:
        The PQC algorithm used.
    public_key_id:
        Identifier of the key used to sign.
    signature_hex:
        Hex-encoded signature bytes.
    message_hash:
        SHA3-256 hex digest of the signed message.
    timestamp:
        UTC time of signing.
    is_placeholder:
        ``True`` when the signature is a placeholder (not a real PQC
        signature).  Downstream code must check this flag.
    """

    algorithm: PQCAlgorithm
    public_key_id: str
    signature_hex: str
    message_hash: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_placeholder: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "algorithm": self.algorithm.value,
            "public_key_id": self.public_key_id,
            "signature_hex": self.signature_hex,
            "message_hash": self.message_hash,
            "timestamp": self.timestamp.isoformat(),
            "is_placeholder": self.is_placeholder,
        }


@dataclass
class VerificationResult:
    """
    Result of a PQC signature verification operation.

    Attributes
    ----------
    valid:
        ``True`` if the signature is verified (or placeholder-accepted).
    algorithm:
        The algorithm used for verification.
    message_hash:
        SHA3-256 hex digest of the message that was verified.
    timestamp:
        UTC time of verification.
    notes:
        Human-readable notes, e.g. placeholder warnings.
    """

    valid: bool
    algorithm: PQCAlgorithm
    message_hash: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "algorithm": self.algorithm.value,
            "message_hash": self.message_hash,
            "timestamp": self.timestamp.isoformat(),
            "notes": self.notes,
        }


class PQCWrapper:
    """
    High-level wrapper for post-quantum cryptographic operations.

    SHA3-256 hashing is fully functional (stdlib).  PQC signing and
    verification are placeholders until ``liboqs`` or ``pqcrypto`` is
    installed.

    Install real PQC support with::

        pip install liboqs       # Open Quantum Safe project
        # or
        pip install pqcrypto     # Python PQCrypto bindings
    """

    # ------------------------------------------------------------------
    # Hashing (fully implemented, stdlib only)
    # ------------------------------------------------------------------

    @staticmethod
    def hash_message(message: bytes) -> str:
        """
        Return the SHA3-256 hex digest of *message*.

        This is a real cryptographic hash, not a placeholder.
        """
        return hashlib.sha3_256(message).hexdigest()

    # ------------------------------------------------------------------
    # Signing (placeholder — requires PQC library)
    # ------------------------------------------------------------------

    def sign(
        self,
        message: bytes,
        key_id: str,
        algorithm: PQCAlgorithm = PQCAlgorithm.ML_DSA_65,
    ) -> SignatureResult:
        """
        Sign *message* with the key identified by *key_id*.

        .. note::
            **PLACEHOLDER** — Returns a simulated signature.
            For real PQC signing, install ``liboqs-python``::

                pip install liboqs

            Then replace this method body with::

                import oqs
                signer = oqs.Signature(algorithm.value)
                public_key = signer.generate_keypair()
                sig = signer.sign(message)

        Parameters
        ----------
        message:
            Raw bytes to sign.
        key_id:
            Identifier of the signing key (must be in the KeyManager).
        algorithm:
            PQC signature algorithm to use.
        """
        message_hash = self.hash_message(message)
        # Placeholder: use os.urandom to simulate a signature blob.
        placeholder_sig = os.urandom(64).hex()

        return SignatureResult(
            algorithm=algorithm,
            public_key_id=key_id,
            signature_hex=placeholder_sig,
            message_hash=message_hash,
            is_placeholder=True,
        )

    # ------------------------------------------------------------------
    # Verification (placeholder — requires PQC library)
    # ------------------------------------------------------------------

    def verify(
        self,
        message: bytes,
        signature_result: SignatureResult,
        public_key: bytes,
    ) -> VerificationResult:
        """
        Verify *signature_result* against *message* using *public_key*.

        .. note::
            **PLACEHOLDER** — Always returns ``valid=True`` for placeholder
            signatures, but logs a warning in ``notes``.
            For real verification, install ``liboqs-python``::

                pip install liboqs

            Then use::

                verifier = oqs.Signature(algorithm.value)
                valid = verifier.verify(message, bytes.fromhex(sig_hex), public_key)

        Parameters
        ----------
        message:
            The original message bytes that were signed.
        signature_result:
            The ``SignatureResult`` returned by ``sign()``.
        public_key:
            Raw public key bytes corresponding to the signing key.
        """
        message_hash = self.hash_message(message)
        hashes_match = message_hash == signature_result.message_hash

        if signature_result.is_placeholder:
            notes = (
                "PLACEHOLDER signature — not cryptographically verified.  "
                "Install liboqs (pip install liboqs) for real PQC verification."
            )
            return VerificationResult(
                valid=hashes_match,
                algorithm=signature_result.algorithm,
                message_hash=message_hash,
                notes=notes,
            )

        # TODO: real verification path (liboqs / pqcrypto)
        raise RuntimeError(
            "Real PQC verification requires liboqs-python.  "
            "Install with: pip install liboqs"
        )
