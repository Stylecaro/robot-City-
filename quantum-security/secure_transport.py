"""
secure_transport.py — Post-Quantum secure message transport.

Provides ``EncryptedMessage`` (the wire format) and ``SecureTransport``
(encrypt / decrypt / channel establishment).

All encryption/decryption operations are placeholders until
``liboqs-python`` (``pip install liboqs``) is installed.

Install real PQC support::

    pip install liboqs
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict

from .pqc_wrapper import PQCAlgorithm


@dataclass
class EncryptedMessage:
    """
    A PQC-encrypted message in wire format.

    Attributes
    ----------
    message_id:
        Auto-generated UUID for this message.
    algorithm:
        The KEM algorithm used (e.g. ML-KEM-768).
    ciphertext_hex:
        Hex-encoded ciphertext (placeholder random bytes until liboqs).
    sender_key_id:
        Key ID of the sender's key pair.
    recipient_key_id:
        Key ID of the recipient's key pair.
    timestamp:
        UTC time of encryption.
    is_placeholder:
        ``True`` when the ciphertext is not a real PQC ciphertext.
        Downstream consumers must check this flag.
    """

    algorithm: PQCAlgorithm
    sender_key_id: str
    recipient_key_id: str
    ciphertext_hex: str
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_placeholder: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "algorithm": self.algorithm.value,
            "ciphertext_hex": self.ciphertext_hex,
            "sender_key_id": self.sender_key_id,
            "recipient_key_id": self.recipient_key_id,
            "timestamp": self.timestamp.isoformat(),
            "is_placeholder": self.is_placeholder,
        }


class SecureTransport:
    """
    Handles PQC-encrypted message transport.

    All encrypt/decrypt operations are placeholders.  For real PQC
    encryption::

        pip install liboqs

    Then replace the placeholder bodies with::

        import oqs
        kem = oqs.KeyEncapsulation("ML-KEM-768")
        ciphertext, shared_secret = kem.encap_secret(recipient_public_key)
        # Use shared_secret with AES-GCM to encrypt the message.
    """

    # ------------------------------------------------------------------
    # Encryption (placeholder)
    # ------------------------------------------------------------------

    def encrypt(
        self,
        message: bytes,
        recipient_key_id: str,
        algorithm: PQCAlgorithm = PQCAlgorithm.ML_KEM_768,
        sender_key_id: str = "default_sender",
    ) -> EncryptedMessage:
        """
        Encrypt *message* for *recipient_key_id*.

        .. note::
            **PLACEHOLDER** — Returns a simulated ciphertext.
            Install ``liboqs`` for real ML-KEM encryption::

                pip install liboqs

        Parameters
        ----------
        message:
            Plaintext bytes to encrypt.
        recipient_key_id:
            ID of the recipient's public key (in the KeyManager).
        algorithm:
            KEM algorithm to use for key encapsulation.
        sender_key_id:
            ID of the sender's key pair.
        """
        # Placeholder: XOR message with random bytes and return as ciphertext.
        pad = os.urandom(len(message))
        ciphertext = bytes(a ^ b for a, b in zip(message, pad))

        return EncryptedMessage(
            algorithm=algorithm,
            sender_key_id=sender_key_id,
            recipient_key_id=recipient_key_id,
            ciphertext_hex=ciphertext.hex(),
            is_placeholder=True,
        )

    # ------------------------------------------------------------------
    # Decryption (placeholder)
    # ------------------------------------------------------------------

    def decrypt(
        self,
        encrypted_message: EncryptedMessage,
        private_key: bytes,
    ) -> bytes:
        """
        Decrypt *encrypted_message* using *private_key*.

        .. note::
            **PLACEHOLDER** — Cannot reverse the placeholder encryption
            without the original random pad.  Raises ``RuntimeError``
            if called on a placeholder message.

            Install ``liboqs`` for real ML-KEM decryption::

                pip install liboqs

        Parameters
        ----------
        encrypted_message:
            The ``EncryptedMessage`` to decrypt.
        private_key:
            Raw private key bytes (from HSM or secure enclave).
        """
        if encrypted_message.is_placeholder:
            raise RuntimeError(
                "Cannot decrypt a placeholder EncryptedMessage.  "
                "Install liboqs (pip install liboqs) for real PQC decryption."
            )

        # TODO: real ML-KEM decryption using liboqs
        raise RuntimeError(
            "decrypt requires liboqs-python.  Install with: pip install liboqs"
        )

    # ------------------------------------------------------------------
    # Channel establishment
    # ------------------------------------------------------------------

    def establish_secure_channel(
        self, sender_id: str, recipient_id: str
    ) -> Dict[str, Any]:
        """
        Simulate establishing a PQC-secured communication channel.

        Returns a dict describing the channel.  In a real system this
        would perform a KEM-based key exchange and return a session key
        identifier (not the key itself).

        .. note::
            **PLACEHOLDER** — No actual key exchange is performed.
        """
        channel_id = str(uuid.uuid4())
        return {
            "channel_id": channel_id,
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "algorithm": PQCAlgorithm.ML_KEM_768.value,
            "established_at": datetime.now(timezone.utc).isoformat(),
            "status": "placeholder",
            "notes": (
                "Placeholder channel — no real key exchange performed.  "
                "Install liboqs (pip install liboqs) for real ML-KEM handshake."
            ),
        }
