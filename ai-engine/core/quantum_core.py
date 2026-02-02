"""
Quantum Core - Comunicación cuántica simulada para Ciudad Robot
Implementa entrelazamiento y transmisión segura entre nodos.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional
import random
import uuid


@dataclass
class QuantumNode:
    """Nodo cuántico dentro de la ciudad"""
    node_id: str
    name: str
    location: str
    status: str = "active"

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EntangledChannel:
    """Canal de entrelazamiento entre dos nodos"""
    channel_id: str
    node_a: str
    node_b: str
    fidelity: float
    created_at: str
    active: bool = True

    def to_dict(self) -> Dict:
        return asdict(self)


class QuantumCore:
    """Núcleo cuántico para comunicación entrelazada"""

    def __init__(self):
        self.nodes: Dict[str, QuantumNode] = {}
        self.channels: Dict[str, EntangledChannel] = {}
        self.central_city_node_id: str = self._create_central_node()

    def _create_central_node(self) -> str:
        node_id = str(uuid.uuid4())
        self.nodes[node_id] = QuantumNode(
            node_id=node_id,
            name="Central City",
            location="city_core"
        )
        return node_id

    def register_node(self, name: str, location: str) -> QuantumNode:
        node_id = str(uuid.uuid4())
        node = QuantumNode(node_id=node_id, name=name, location=location)
        self.nodes[node_id] = node
        return node

    def list_nodes(self) -> List[Dict]:
        return [n.to_dict() for n in self.nodes.values()]

    def create_entangled_channel(self, node_a: str, node_b: str, fidelity: float = 0.98) -> EntangledChannel:
        if node_a not in self.nodes or node_b not in self.nodes:
            raise ValueError("Nodo no encontrado")
        channel_id = str(uuid.uuid4())
        channel = EntangledChannel(
            channel_id=channel_id,
            node_a=node_a,
            node_b=node_b,
            fidelity=max(0.0, min(1.0, fidelity)),
            created_at=datetime.now().isoformat()
        )
        self.channels[channel_id] = channel
        return channel

    def list_channels(self) -> List[Dict]:
        return [c.to_dict() for c in self.channels.values()]

    def encode_message(self, message: str) -> List[int]:
        data = message.encode("utf-8")
        bits: List[int] = []
        for byte in data:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return bits

    def decode_message(self, bits: List[int]) -> str:
        usable_length = len(bits) - (len(bits) % 8)
        bytes_out = bytearray()
        for i in range(0, usable_length, 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | (bits[i + j] & 1)
            bytes_out.append(byte)
        try:
            return bytes_out.decode("utf-8", errors="replace")
        except Exception:
            return ""

    def transmit(self, channel_id: str, message: str, noise: float = 0.01) -> Dict:
        channel = self.channels.get(channel_id)
        if not channel or not channel.active:
            raise ValueError("Canal no disponible")

        bits = self.encode_message(message)
        if not bits:
            return {
                "channel_id": channel_id,
                "original": message,
                "received": "",
                "bit_error_rate": 0.0,
                "fidelity": channel.fidelity
            }

        error_probability = min(1.0, max(0.0, noise + (1.0 - channel.fidelity)))
        flipped = 0
        transmitted: List[int] = []
        for bit in bits:
            if random.random() < error_probability:
                transmitted.append(1 - bit)
                flipped += 1
            else:
                transmitted.append(bit)

        received = self.decode_message(transmitted)
        ber = flipped / len(bits)

        return {
            "channel_id": channel_id,
            "original": message,
            "received": received,
            "bit_error_rate": round(ber, 6),
            "fidelity": channel.fidelity
        }

    def transmit_to_central(self, channel_id: str, message: str, noise: float = 0.01) -> Dict:
        """Atajo para transmisión hacia el núcleo central"""
        result = self.transmit(channel_id, message, noise)
        result["target"] = "central_city"
        return result
