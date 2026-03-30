"""
transport_robot.py — Transport Service Robot

Manages passenger pickup, cargo delivery, route optimisation,
and city traffic management functions.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .base_robot import Location, RobotType, ServiceRobot, Task


class TransportRobot(ServiceRobot):
    """
    A service robot specialised in city transport operations.

    Capabilities
    ------------
    passenger_transport, cargo_delivery, route_optimization,
    traffic_management
    """

    CAPABILITIES: List[str] = [
        "passenger_transport",
        "cargo_delivery",
        "route_optimization",
        "traffic_management",
    ]

    def __init__(
        self,
        name: str,
        *,
        robot_id: Optional[str] = None,
        initial_location: Optional[Location] = None,
        battery_level: float = 100.0,
        max_cargo_kg: float = 100.0,
        max_passengers: int = 4,
    ) -> None:
        super().__init__(
            name,
            RobotType.TRANSPORT,
            robot_id=robot_id,
            initial_location=initial_location,
            battery_level=battery_level,
        )
        self.max_cargo_kg: float = max_cargo_kg
        self.max_passengers: int = max_passengers
        self._delivery_log: List[Dict[str, Any]] = []
        self._passenger_log: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Transport operations
    # ------------------------------------------------------------------

    def plan_route(self, origin: Location, destination: Location) -> Dict[str, Any]:
        """
        Calculate an optimal route from *origin* to *destination*.

        Returns a placeholder route plan; real integration would call
        the city's traffic management API.
        """
        import math

        distance = math.sqrt(
            (destination.x - origin.x) ** 2 + (destination.y - origin.y) ** 2
        )

        return {
            "robot_id": self.robot_id,
            "origin": origin.to_dict(),
            "destination": destination.to_dict(),
            "estimated_distance_km": round(distance, 2),
            "estimated_time_minutes": round(distance * 2, 1),
            "waypoints": [],  # TODO: populate via city routing API
            "notes": "Placeholder route — integrate with city traffic management service.",
        }

    def pickup_passenger(
        self, passenger_id: str, location: Location
    ) -> Dict[str, Any]:
        """
        Pick up a passenger at *location*.

        Returns a pickup confirmation with task_id and ETA.
        """
        task = Task(
            description=f"Pickup passenger {passenger_id}",
            priority=4,
            metadata={"passenger_id": passenger_id, "location": location.to_dict()},
        )
        self.assign_task(task)

        record: Dict[str, Any] = {
            "task_id": task.task_id,
            "passenger_id": passenger_id,
            "robot_id": self.robot_id,
            "pickup_location": location.to_dict(),
            "eta_minutes": 5.0,  # Placeholder ETA
            "status": "en_route_to_passenger",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._passenger_log.append(record)
        return record

    def deliver_cargo(
        self, cargo_id: str, destination: Location, weight_kg: float = 0.0
    ) -> Dict[str, Any]:
        """
        Deliver cargo identified by *cargo_id* to *destination*.

        Parameters
        ----------
        cargo_id:
            Unique identifier of the cargo item.
        destination:
            Target delivery location.
        weight_kg:
            Weight of the cargo; raises ``ValueError`` if it exceeds
            the robot's capacity.
        """
        if weight_kg > self.max_cargo_kg:
            raise ValueError(
                f"Cargo weight {weight_kg} kg exceeds max capacity {self.max_cargo_kg} kg."
            )

        task = Task(
            description=f"Deliver cargo {cargo_id} to ({destination.x}, {destination.y})",
            priority=5,
            metadata={
                "cargo_id": cargo_id,
                "destination": destination.to_dict(),
                "weight_kg": weight_kg,
            },
        )
        self.assign_task(task)

        record: Dict[str, Any] = {
            "task_id": task.task_id,
            "cargo_id": cargo_id,
            "robot_id": self.robot_id,
            "destination": destination.to_dict(),
            "weight_kg": weight_kg,
            "status": "in_transit",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._delivery_log.append(record)
        return record

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "capabilities": self.CAPABILITIES,
                "max_cargo_kg": self.max_cargo_kg,
                "max_passengers": self.max_passengers,
                "deliveries_logged": len(self._delivery_log),
                "passengers_logged": len(self._passenger_log),
            }
        )
        return base
