"""
event_ledger.py — Hybrid Event/Payment Ledger for Robot City
=============================================================
Records city service events, simulation events, and crypto payment
events in a chain-agnostic, normalized format.

Designed as a secure audit layer that sits above the real blockchains
(Ethereum, Solana, etc.) and the local QuantumBlockchain.

Supports pluggable chain backends via the ChainBackend protocol.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Event types
# ---------------------------------------------------------------------------

class EventCategory(str, Enum):
    """Top-level category for recorded events."""
    CITY_SERVICE = "city_service"       # Service-robot activity
    SIMULATION = "simulation"           # Simulation/game events
    PAYMENT = "payment"                 # Crypto payment events
    SECURITY = "security"               # Security incidents
    MAINTENANCE = "maintenance"         # Robot/infrastructure maintenance
    GOVERNANCE = "governance"           # Policy / configuration changes
    AUDIT = "audit"                     # Internal audit records


@dataclass
class EventRecord:
    """
    Normalized, chain-agnostic event record.

    Every event stored in the ledger is represented as an EventRecord
    before being committed to any backend.
    """
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    category: EventCategory = EventCategory.AUDIT
    event_type: str = ""          # e.g. "robot.task.completed"
    source_id: str = ""           # robot_id, user_id, invoice_id, etc.
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    chain_tx_hash: Optional[str] = None   # Set after on-chain recording
    chain_name: Optional[str] = None      # Which chain recorded this
    integrity_hash: str = ""              # SHA3-256 of normalized event

    def __post_init__(self) -> None:
        if not self.integrity_hash:
            self.integrity_hash = self._compute_integrity_hash()

    def _compute_integrity_hash(self) -> str:
        """Compute SHA3-256 over the canonical event fields (excluding mutable chain fields)."""
        canonical = json.dumps(
            {
                "event_id": self.event_id,
                "category": self.category.value if isinstance(self.category, EventCategory) else self.category,
                "event_type": self.event_type,
                "source_id": self.source_id,
                "payload": self.payload,
                "timestamp": self.timestamp,
            },
            sort_keys=True,
        ).encode()
        return hashlib.sha3_256(canonical).hexdigest()

    def verify_integrity(self) -> bool:
        """Return True if the stored integrity hash matches a fresh computation."""
        return self.integrity_hash == self._compute_integrity_hash()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["category"] = self.category.value if isinstance(self.category, EventCategory) else self.category
        return d


# ---------------------------------------------------------------------------
# Chain backend protocol (pluggable)
# ---------------------------------------------------------------------------

@runtime_checkable
class ChainBackend(Protocol):
    """
    Protocol for pluggable chain backends.

    Implement this protocol to record events on a real blockchain
    (Ethereum, Solana, etc.) or keep the default local-only ledger.
    """

    @property
    def backend_name(self) -> str:
        """Human-readable name of the backend (e.g. 'ethereum-mainnet')."""
        ...

    def record_event(self, event: EventRecord) -> str:
        """
        Persist the event to the chain.

        Returns:
            A transaction hash or reference ID (chain-specific).
        """
        ...

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an event by its event_id from the chain (if supported)."""
        ...


class LocalLedgerBackend:
    """
    Default in-memory backend — no external chain required.

    Suitable for development, testing, and the local quantum-blockchain layer.
    Replace or supplement with a real ChainBackend for production.
    """

    backend_name: str = "local"

    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def record_event(self, event: EventRecord) -> str:
        """Store the event locally and return a fake tx reference."""
        tx_ref = f"local-{event.event_id[:8]}"
        self._store[event.event_id] = event.to_dict()
        self._store[event.event_id]["_tx_ref"] = tx_ref
        return tx_ref

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        return self._store.get(event_id)

    def list_events(self) -> List[Dict[str, Any]]:
        return list(self._store.values())


class QuantumBlockchainBackend:
    """
    Backend that records events to the local QuantumBlockchain.

    Wraps the existing quantum_blockchain.py and uses it as the
    immutable append-only store for city/payment events.
    """

    backend_name: str = "quantum-blockchain"

    def __init__(self) -> None:
        import sys, os
        sys.path.insert(0, os.path.dirname(__file__))
        from quantum_blockchain import QuantumBlockchain  # type: ignore
        self._chain = QuantumBlockchain(nombre="RobotCityEventLedger")

    def record_event(self, event: EventRecord) -> str:
        """Add the event as a new block in the quantum blockchain."""
        block = self._chain.add_block(event.to_dict())
        return block.quantum_hash[:16] if hasattr(block, "quantum_hash") else "qb-recorded"

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Search blocks for an event by event_id (linear scan)."""
        for block in self._chain.cadena:
            if isinstance(block.data, dict) and block.data.get("event_id") == event_id:
                return block.data
        return None

    def chain_state(self) -> dict:
        """Return the full quantum blockchain state."""
        return self._chain.get_chain_state()


# ---------------------------------------------------------------------------
# Event Ledger
# ---------------------------------------------------------------------------

class EventLedger:
    """
    Hybrid event/payment ledger for Robot City.

    Records normalized EventRecord objects to one or more ChainBackends.
    By default uses the LocalLedgerBackend. Add a QuantumBlockchainBackend
    or a real chain backend to persist events on-chain.

    Example::

        ledger = EventLedger()
        ledger.add_backend(QuantumBlockchainBackend())

        receipt = ledger.record(
            category=EventCategory.PAYMENT,
            event_type="payment.invoice.paid",
            source_id="invoice-abc123",
            payload={"asset": "ETH", "amount": 0.05, "tx_hash": "0x..."},
        )
    """

    def __init__(self) -> None:
        self._backends: List[Any] = [LocalLedgerBackend()]
        self._events: List[EventRecord] = []

    # --- Backend management ------------------------------------------------

    def add_backend(self, backend: Any) -> None:
        """Add a ChainBackend to receive all future events."""
        self._backends.append(backend)

    def remove_backend(self, backend_name: str) -> bool:
        before = len(self._backends)
        self._backends = [b for b in self._backends if getattr(b, "backend_name", "") != backend_name]
        return len(self._backends) < before

    def list_backends(self) -> List[str]:
        return [getattr(b, "backend_name", str(b)) for b in self._backends]

    # --- Event recording ---------------------------------------------------

    def record(
        self,
        category: EventCategory,
        event_type: str,
        source_id: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> EventRecord:
        """
        Create and persist a new EventRecord across all backends.

        Args:
            category: High-level event category.
            event_type: Dot-notation type string (e.g. 'robot.task.completed').
            source_id: Identifier of the entity that caused the event.
            payload: Arbitrary structured data for the event.

        Returns:
            The persisted EventRecord (with integrity_hash set).
        """
        event = EventRecord(
            category=category,
            event_type=event_type,
            source_id=source_id,
            payload=payload or {},
        )

        chain_results: Dict[str, str] = {}
        for backend in self._backends:
            try:
                tx_ref = backend.record_event(event)
                chain_results[getattr(backend, "backend_name", "unknown")] = tx_ref
            except Exception as exc:  # pragma: no cover
                chain_results[getattr(backend, "backend_name", "unknown")] = f"error: {exc}"

        # Attach first chain reference to event metadata
        if chain_results:
            first_backend = next(iter(chain_results))
            event.chain_name = first_backend
            event.chain_tx_hash = chain_results[first_backend]

        self._events.append(event)
        return event

    # --- Helpers for common event types ------------------------------------

    def record_robot_event(self, robot_id: str, action: str, details: Optional[Dict] = None) -> EventRecord:
        """Record a city-service robot event."""
        return self.record(
            category=EventCategory.CITY_SERVICE,
            event_type=f"robot.{action}",
            source_id=robot_id,
            payload=details or {},
        )

    def record_payment_event(self, invoice_id: str, status: str, details: Optional[Dict] = None) -> EventRecord:
        """Record a crypto payment event."""
        return self.record(
            category=EventCategory.PAYMENT,
            event_type=f"payment.{status}",
            source_id=invoice_id,
            payload=details or {},
        )

    def record_simulation_event(self, sim_id: str, event_type: str, details: Optional[Dict] = None) -> EventRecord:
        """Record a simulation/game event."""
        return self.record(
            category=EventCategory.SIMULATION,
            event_type=f"simulation.{event_type}",
            source_id=sim_id,
            payload=details or {},
        )

    # --- Query -------------------------------------------------------------

    def get_event(self, event_id: str) -> Optional[EventRecord]:
        for e in self._events:
            if e.event_id == event_id:
                return e
        return None

    def list_events(
        self,
        category: Optional[EventCategory] = None,
        limit: int = 100,
    ) -> List[EventRecord]:
        """Return events, optionally filtered by category, newest first."""
        events = self._events
        if category is not None:
            events = [e for e in events if e.category == category]
        return list(reversed(events))[:limit]

    def get_stats(self) -> Dict[str, Any]:
        """Return summary statistics about the ledger."""
        counts: Dict[str, int] = {}
        for e in self._events:
            cat = e.category.value if isinstance(e.category, EventCategory) else str(e.category)
            counts[cat] = counts.get(cat, 0) + 1
        return {
            "total_events": len(self._events),
            "by_category": counts,
            "backends": self.list_backends(),
        }


# ---------------------------------------------------------------------------
# Module-level default ledger
# ---------------------------------------------------------------------------

#: Global default EventLedger instance — import and use directly.
default_ledger = EventLedger()
