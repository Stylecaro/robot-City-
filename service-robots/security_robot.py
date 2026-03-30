"""
security_robot.py — Security Service Robot

Named SecurityRobotService to avoid collision with the existing
security-system module in this project.

Handles city patrol routes, incident reporting, access control,
and threat detection.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .base_robot import Location, RobotType, ServiceRobot, Task


class SecurityRobotService(ServiceRobot):
    """
    A service robot specialised in city security operations.

    Capabilities
    ------------
    patrol, surveillance, threat_detection, access_control,
    incident_response
    """

    CAPABILITIES: List[str] = [
        "patrol",
        "surveillance",
        "threat_detection",
        "access_control",
        "incident_response",
    ]

    def __init__(
        self,
        name: str,
        *,
        robot_id: Optional[str] = None,
        initial_location: Optional[Location] = None,
        battery_level: float = 100.0,
    ) -> None:
        super().__init__(
            name,
            RobotType.SECURITY,
            robot_id=robot_id,
            initial_location=initial_location,
            battery_level=battery_level,
        )
        self._incident_log: List[Dict[str, Any]] = []
        self._patrol_route: List[Location] = []
        self._access_log: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Security operations
    # ------------------------------------------------------------------

    def start_patrol(self, route: List[Location]) -> Dict[str, Any]:
        """
        Begin patrolling a sequence of *route* waypoints.

        Parameters
        ----------
        route:
            Ordered list of city locations to visit.

        Returns
        -------
        dict
            Patrol session details including task_id.
        """
        self._patrol_route = route
        task = Task(
            description=f"Patrol route with {len(route)} waypoints",
            priority=5,
            metadata={"waypoints": [loc.to_dict() for loc in route]},
        )
        self.assign_task(task)

        return {
            "task_id": task.task_id,
            "robot_id": self.robot_id,
            "waypoints": len(route),
            "started_at": datetime.now(timezone.utc).isoformat(),
            "status": "patrolling",
        }

    def report_incident(
        self, incident_type: str, location: Location, severity: int
    ) -> Dict[str, Any]:
        """
        Log and respond to a security incident.

        Parameters
        ----------
        incident_type:
            E.g. ``"intrusion"``, ``"vandalism"``, ``"fire"``.
        location:
            Where the incident occurred.
        severity:
            1 (critical) … 5 (minor).

        Returns
        -------
        dict
            Incident record with a generated incident_id.
        """
        severity = max(1, min(5, severity))
        task = Task(
            description=f"Incident response: {incident_type} at {location.label or str(location)}",
            priority=severity,
            metadata={
                "incident_type": incident_type,
                "location": location.to_dict(),
                "severity": severity,
            },
        )
        self.assign_task(task)

        record: Dict[str, Any] = {
            "incident_id": task.task_id,
            "robot_id": self.robot_id,
            "incident_type": incident_type,
            "location": location.to_dict(),
            "severity": severity,
            "reported_at": datetime.now(timezone.utc).isoformat(),
            "status": "investigating",
        }
        self._incident_log.append(record)
        return record

    def check_access(self, entity_id: str, zone: str) -> Dict[str, Any]:
        """
        Verify whether *entity_id* is authorised for *zone*.

        Returns a placeholder access-control result; real integration
        would query the city access-control database.
        """
        # Placeholder: all checks return a simulated response.
        granted = True  # TODO: integrate with city ACL service
        record: Dict[str, Any] = {
            "entity_id": entity_id,
            "zone": zone,
            "robot_id": self.robot_id,
            "granted": granted,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "notes": "Placeholder — integrate with city access-control service.",
        }
        self._access_log.append(record)
        return record

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "capabilities": self.CAPABILITIES,
                "incidents_logged": len(self._incident_log),
                "patrol_waypoints": len(self._patrol_route),
                "access_checks": len(self._access_log),
            }
        )
        return base
