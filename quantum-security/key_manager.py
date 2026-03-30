"""
key_manager.py — Post-Quantum key bundle management.

.. important::
    **Private keys are NEVER stored in KeyBundle or KeyManager.**

    ``KeyBundle`` holds only the public key and metadata.  Private keys
    must remain in a hardware security module (HSM), secure enclave, or
    dedicated key-management service.

    The ``generate_key_bundle`` method is a placeholder; real key
    generation requires ``liboqs-python`` (``pip install liboqs``).
"""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pqc_wrapper import PQCAlgorithm


@dataclass
class KeyBundle:
    """
    A public-key bundle for a PQC key pair.

    .. warning::
        Only the *public* key is stored here.  The private key must be
        managed externally by a secure key-management service.

    Attributes
    ----------
    key_id:
        Unique identifier for this key pair.
    algorithm:
        The PQC algorithm the key was generated for.
    public_key_hex:
        Hex-encoded public key bytes (placeholder random bytes until a
        real PQC library is used).
    created_at:
        UTC timestamp of key generation.
    metadata:
        Optional free-form key/value data (labels, owner, etc.).
    """

    key_id: str
    algorithm: PQCAlgorithm
    public_key_hex: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    # NOTE: private_key is intentionally omitted — never store it here.

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "algorithm": self.algorithm.value,
            "public_key_hex": self.public_key_hex,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }


class KeyManager:
    """
    In-memory registry of PQC public-key bundles.

    All key-generation methods are placeholders.  For production use:

    1. Install ``liboqs-python``::

           pip install liboqs

    2. Replace the placeholder generation in ``generate_key_bundle`` with::

           import oqs
           kem = oqs.KeyEncapsulation(algorithm.value)
           public_key = kem.generate_keypair()  # private key stays in kem

    3. Store private keys in a hardware security module (HSM) or secure
       enclave — never in this registry.
    """

    def __init__(self) -> None:
        self._keys: Dict[str, KeyBundle] = {}

    # ------------------------------------------------------------------
    # Key lifecycle
    # ------------------------------------------------------------------

    def generate_key_bundle(
        self,
        key_id: str,
        algorithm: PQCAlgorithm,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> KeyBundle:
        """
        Generate a new key bundle for *algorithm*.

        .. note::
            **PLACEHOLDER** — The public key is random bytes, not a real
            PQC public key.  Replace with ``liboqs`` key generation for
            production use.

        Parameters
        ----------
        key_id:
            Caller-supplied identifier for this key.
        algorithm:
            PQC algorithm to generate keys for.
        metadata:
            Optional extra information (owner, purpose, etc.).
        """
        # Placeholder: simulate a public key with random bytes.
        placeholder_pubkey = os.urandom(128).hex()

        bundle = KeyBundle(
            key_id=key_id,
            algorithm=algorithm,
            public_key_hex=placeholder_pubkey,
            metadata=metadata or {"is_placeholder": True},
        )
        self._keys[key_id] = bundle
        return bundle

    def get_public_key(self, key_id: str) -> KeyBundle:
        """
        Retrieve the ``KeyBundle`` for *key_id*.

        Raises
        ------
        KeyError
            If no key with *key_id* is registered.
        """
        if key_id not in self._keys:
            raise KeyError(f"Key '{key_id}' not found.")
        return self._keys[key_id]

    def list_keys(self) -> List[str]:
        """Return a list of all registered key IDs."""
        return list(self._keys.keys())

    def rotate_key(self, key_id: str) -> KeyBundle:
        """
        Replace the key bundle for *key_id* with a freshly generated one.

        .. note::
            **PLACEHOLDER** — Generates a new random public key.  In
            production this would trigger new key generation in the HSM
            and invalidate the old key.

        Returns
        -------
        KeyBundle
            The new key bundle (same key_id, new public key + timestamp).
        """
        if key_id not in self._keys:
            raise KeyError(f"Key '{key_id}' not found — cannot rotate.")

        old = self._keys[key_id]
        new_bundle = KeyBundle(
            key_id=key_id,
            algorithm=old.algorithm,
            public_key_hex=os.urandom(128).hex(),
            metadata={**old.metadata, "rotated_at": datetime.now(timezone.utc).isoformat()},
        )
        self._keys[key_id] = new_bundle
        return new_bundle

    def delete_key(self, key_id: str) -> bool:
        """
        Remove a key bundle from the registry.

        Returns ``True`` if the key was present and deleted, ``False``
        if it was not found.
        """
        if key_id in self._keys:
            del self._keys[key_id]
            return True
        return False

    def get_stats(self) -> Dict[str, Any]:
        """Return aggregate statistics about stored keys."""
        by_algo: Dict[str, int] = {}
        for bundle in self._keys.values():
            algo = bundle.algorithm.value
            by_algo[algo] = by_algo.get(algo, 0) + 1
        return {"total_keys": len(self._keys), "by_algorithm": by_algo}
