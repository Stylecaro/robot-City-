"""
city_simulation.py — City-Level Simulation Interface
=====================================================
Provides a backend-friendly interface for simulating robot-city
operations before real-world deployment.

Connects to service-robots, payments, web3, and quantum-blockchain
to give a coherent simulation/game workflow.
"""

from __future__ import annotations

import uuid
import random
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class CityZone(str, Enum):
    """City zones available in the simulation."""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    MEDICAL = "medical"
    EDUCATIONAL = "educational"
    TRANSPORT_HUB = "transport_hub"
    SECURITY = "security"
    CONSTRUCTION = "construction"
    PARK = "park"
    CENTRAL = "central"


class SimEventType(str, Enum):
    """Types of simulation events that can occur."""
    ROBOT_DEPLOYED = "robot_deployed"
    ROBOT_TASK_COMPLETED = "robot_task_completed"
    INCIDENT_DETECTED = "incident_detected"
    INCIDENT_RESOLVED = "incident_resolved"
    PAYMENT_PROCESSED = "payment_processed"
    BUILDING_CONSTRUCTED = "building_constructed"
    CITIZEN_SERVED = "citizen_served"
    ZONE_STATUS_CHANGED = "zone_status_changed"
    SIMULATION_TICK = "simulation_tick"


@dataclass
class Citizen:
    """A simulated city citizen."""
    citizen_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Citizen"
    zone: CityZone = CityZone.RESIDENTIAL
    needs: List[str] = field(default_factory=list)  # e.g. ["medical", "transport"]
    satisfaction: float = 1.0  # 0.0 – 1.0

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["zone"] = self.zone.value
        return d


@dataclass
class SimEvent:
    """An event that occurred during the simulation."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: SimEventType = SimEventType.SIMULATION_TICK
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    zone: Optional[CityZone] = None
    source_id: str = ""          # robot_id, citizen_id, etc.
    description: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["event_type"] = self.event_type.value
        d["zone"] = self.zone.value if self.zone else None
        return d


@dataclass
class ZoneStatus:
    """Current status of a city zone."""
    zone: CityZone
    active_robots: int = 0
    citizens_present: int = 0
    incidents: int = 0
    satisfaction: float = 1.0
    last_updated: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["zone"] = self.zone.value
        return d


# ---------------------------------------------------------------------------
# City Simulation Engine
# ---------------------------------------------------------------------------

class CitySimulation:
    """
    City-level simulation engine.

    Orchestrates service robots, citizens, zone states, and events
    in a lightweight simulation loop. Designed to be run as a backend
    service that can feed data to the frontend 3D city view.

    Integration points:
    - ``service-robots/``: Use ServiceRobotRegistry to dispatch robots.
    - ``payments/``: Use CryptoPaymentService for in-sim payments.
    - ``quantum-blockchain/``: Use EventLedger to persist sim events.
    - Frontend 3D: Expose ``get_city_state()`` via the REST API.

    Example::

        sim = CitySimulation(city_name="Ciudad Robot Alpha")
        sim.initialize(num_citizens=50)
        sim.tick()  # advance one simulation step
        state = sim.get_city_state()
    """

    def __init__(self, city_name: str = "Ciudad Robot") -> None:
        self.city_name = city_name
        self.simulation_id = str(uuid.uuid4())
        self.tick_count = 0
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.is_running = False

        self.citizens: Dict[str, Citizen] = {}
        self.zones: Dict[CityZone, ZoneStatus] = {
            zone: ZoneStatus(zone=zone) for zone in CityZone
        }
        self.events: List[SimEvent] = []
        self.robot_deployments: List[Dict[str, Any]] = []

        # Optional integrations (set after construction)
        self.robot_registry: Optional[Any] = None   # ServiceRobotRegistry
        self.payment_service: Optional[Any] = None  # CryptoPaymentService
        self.event_ledger: Optional[Any] = None     # EventLedger

    # --- Setup -------------------------------------------------------------

    def initialize(self, num_citizens: int = 20) -> None:
        """Populate the simulation with citizens and mark it as running."""
        self._generate_citizens(num_citizens)
        self.is_running = True
        self._emit_event(
            SimEventType.SIMULATION_TICK,
            description=f"Simulation '{self.city_name}' initialized with {num_citizens} citizens.",
            payload={"num_citizens": num_citizens},
        )

    def attach_robot_registry(self, registry: Any) -> None:
        """Attach a ServiceRobotRegistry for robot dispatch."""
        self.robot_registry = registry

    def attach_payment_service(self, service: Any) -> None:
        """Attach a CryptoPaymentService for payment simulation."""
        self.payment_service = service

    def attach_event_ledger(self, ledger: Any) -> None:
        """Attach an EventLedger to persist simulation events on-chain."""
        self.event_ledger = ledger

    # --- Simulation loop ---------------------------------------------------

    def tick(self) -> Dict[str, Any]:
        """
        Advance the simulation by one tick.

        Returns a summary of what happened during this tick.
        """
        if not self.is_running:
            return {"error": "Simulation is not running. Call initialize() first."}

        self.tick_count += 1
        tick_events: List[Dict[str, Any]] = []

        # 1. Update citizen needs
        for citizen in self.citizens.values():
            if random.random() < 0.15:  # 15% chance a citizen develops a need
                need_type = random.choice(["medical", "transport", "commercial", "educational"])
                if need_type not in citizen.needs:
                    citizen.needs.append(need_type)

        # 2. Attempt to serve citizens with available robots
        for citizen in self.citizens.values():
            for need in list(citizen.needs):
                robot_type_map = {
                    "medical": "medical",
                    "transport": "transport",
                    "commercial": "commerce",
                    "educational": "education",
                }
                robot_type = robot_type_map.get(need, "security")
                served = self._try_serve_citizen(citizen, need, robot_type)
                if served:
                    citizen.needs.remove(need)
                    citizen.satisfaction = min(1.0, citizen.satisfaction + 0.05)
                    tick_events.append({
                        "type": SimEventType.CITIZEN_SERVED.value,
                        "citizen_id": citizen.citizen_id,
                        "service": need,
                    })

        # 3. Random incident (5% chance per tick)
        if random.random() < 0.05:
            incident = self._generate_incident()
            tick_events.append(incident)

        # 4. Update zone statistics
        self._update_zone_stats()

        # 5. Emit a tick event
        tick_event = self._emit_event(
            SimEventType.SIMULATION_TICK,
            description=f"Tick #{self.tick_count} completed.",
            payload={"tick": self.tick_count, "events": len(tick_events)},
        )
        tick_events.append(tick_event.to_dict())

        return {
            "tick": self.tick_count,
            "events": tick_events,
            "summary": self._quick_summary(),
        }

    # --- Queries -----------------------------------------------------------

    def get_city_state(self) -> Dict[str, Any]:
        """
        Return the full current state of the simulation.

        This is the primary endpoint for the frontend 3D city viewer.
        """
        return {
            "simulation_id": self.simulation_id,
            "city_name": self.city_name,
            "is_running": self.is_running,
            "tick_count": self.tick_count,
            "started_at": self.started_at,
            "citizens": {
                "total": len(self.citizens),
                "with_needs": sum(1 for c in self.citizens.values() if c.needs),
                "avg_satisfaction": self._avg_satisfaction(),
            },
            "zones": {z.value: self.zones[z].to_dict() for z in CityZone},
            "recent_events": [e.to_dict() for e in self.events[-20:]],
            "robot_deployments": self.robot_deployments[-10:],
        }

    def get_zone_state(self, zone: CityZone) -> Dict[str, Any]:
        """Return the state of a specific zone."""
        status = self.zones.get(zone)
        citizens_in_zone = [c.to_dict() for c in self.citizens.values() if c.zone == zone]
        return {
            "zone_status": status.to_dict() if status else {},
            "citizens": citizens_in_zone,
        }

    def get_event_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Return the most recent simulation events."""
        return [e.to_dict() for e in reversed(self.events[-limit:])]

    def get_stats(self) -> Dict[str, Any]:
        """Return high-level simulation statistics."""
        return {
            "simulation_id": self.simulation_id,
            "city_name": self.city_name,
            "tick_count": self.tick_count,
            "total_citizens": len(self.citizens),
            "total_events": len(self.events),
            "robot_deployments": len(self.robot_deployments),
            "avg_satisfaction": self._avg_satisfaction(),
        }

    # --- Internal helpers --------------------------------------------------

    def _generate_citizens(self, count: int) -> None:
        zones = list(CityZone)
        for i in range(count):
            citizen = Citizen(
                name=f"Citizen-{i+1:03d}",
                zone=random.choice(zones),
            )
            self.citizens[citizen.citizen_id] = citizen

    def _try_serve_citizen(self, citizen: Citizen, need: str, robot_type: str) -> bool:
        """Attempt to serve a citizen need using an available robot."""
        if self.robot_registry is not None:
            try:
                result = self.robot_registry.dispatch_robot(robot_type, f"serve_citizen_{need}")
                if result.get("success"):
                    self.robot_deployments.append({
                        "robot_id": result.get("robot_id"),
                        "robot_type": robot_type,
                        "citizen_id": citizen.citizen_id,
                        "service": need,
                        "zone": citizen.zone.value,
                    })
                    self._emit_event(
                        SimEventType.CITIZEN_SERVED,
                        zone=citizen.zone,
                        source_id=result.get("robot_id", "unknown"),
                        description=f"Robot served citizen {need} need in {citizen.zone.value}",
                        payload={"citizen_id": citizen.citizen_id, "service": need},
                    )
                    return True
            except Exception:
                pass
        # Fallback: simulate service delivery without a real robot registry
        return random.random() < 0.7

    def _generate_incident(self) -> Dict[str, Any]:
        """Generate a random city incident."""
        zone = random.choice(list(CityZone))
        incident_types = ["traffic_jam", "medical_emergency", "power_outage", "suspicious_activity"]
        incident = random.choice(incident_types)

        event = self._emit_event(
            SimEventType.INCIDENT_DETECTED,
            zone=zone,
            source_id="system",
            description=f"Incident '{incident}' detected in {zone.value}",
            payload={"incident_type": incident, "zone": zone.value, "severity": random.choice(["low", "medium", "high"])},
        )
        self.zones[zone].incidents += 1

        return event.to_dict()

    def _update_zone_stats(self) -> None:
        """Recompute zone statistics from citizens and recent events."""
        for zone in CityZone:
            citizens_in_zone = [c for c in self.citizens.values() if c.zone == zone]
            self.zones[zone].citizens_present = len(citizens_in_zone)
            if citizens_in_zone:
                avg_sat = sum(c.satisfaction for c in citizens_in_zone) / len(citizens_in_zone)
                self.zones[zone].satisfaction = round(avg_sat, 3)

    def _emit_event(
        self,
        event_type: SimEventType,
        zone: Optional[CityZone] = None,
        source_id: str = "simulation",
        description: str = "",
        payload: Optional[Dict] = None,
    ) -> SimEvent:
        event = SimEvent(
            event_type=event_type,
            zone=zone,
            source_id=source_id,
            description=description,
            payload=payload or {},
        )
        self.events.append(event)

        # Forward to event ledger if attached
        if self.event_ledger is not None:
            try:
                self.event_ledger.record_simulation_event(
                    sim_id=self.simulation_id,
                    event_type=event_type.value,
                    details=event.to_dict(),
                )
            except Exception:
                pass

        return event

    def _avg_satisfaction(self) -> float:
        if not self.citizens:
            return 1.0
        return round(sum(c.satisfaction for c in self.citizens.values()) / len(self.citizens), 3)

    def _quick_summary(self) -> Dict[str, Any]:
        return {
            "total_citizens": len(self.citizens),
            "avg_satisfaction": self._avg_satisfaction(),
            "citizens_with_needs": sum(1 for c in self.citizens.values() if c.needs),
        }
