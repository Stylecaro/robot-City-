"""
medical_robot.py — Medical Service Robot

Handles city medical emergencies, patient diagnostics,
medication delivery, and ongoing patient monitoring.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .base_robot import Location, RobotType, ServiceRobot, Task


class MedicalRobot(ServiceRobot):
    """
    A service robot specialised in medical city services.

    Capabilities
    ------------
    first_aid, diagnostics, medication_delivery,
    patient_monitoring, emergency_response
    """

    CAPABILITIES: List[str] = [
        "first_aid",
        "diagnostics",
        "medication_delivery",
        "patient_monitoring",
        "emergency_response",
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
            RobotType.MEDICAL,
            robot_id=robot_id,
            initial_location=initial_location,
            battery_level=battery_level,
        )
        self._active_patients: Dict[str, Dict[str, Any]] = {}
        self._incident_log: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Medical operations
    # ------------------------------------------------------------------

    def respond_emergency(self, location: Location, severity: int) -> Dict[str, Any]:
        """
        Dispatch the robot to an emergency at *location*.

        Parameters
        ----------
        location:
            City coordinates of the emergency.
        severity:
            Triage level 1 (critical) … 5 (minor).

        Returns
        -------
        dict
            Dispatch record with ETA estimate and task_id.
        """
        severity = max(1, min(5, severity))
        task = Task(
            description=f"Emergency response at ({location.x}, {location.y})",
            priority=severity,
            metadata={"location": location.to_dict(), "severity": severity},
        )
        self.assign_task(task)
        self.update_location(location)

        record: Dict[str, Any] = {
            "task_id": task.task_id,
            "robot_id": self.robot_id,
            "location": location.to_dict(),
            "severity": severity,
            "eta_minutes": round(severity * 1.5, 1),
            "dispatched_at": datetime.now(timezone.utc).isoformat(),
        }
        self._incident_log.append(record)
        return record

    def run_diagnostics(self, patient_id: str) -> Dict[str, Any]:
        """
        Run a basic diagnostic scan for *patient_id*.

        Returns a placeholder diagnostic report; real integration would
        connect to medical sensor APIs.
        """
        task = Task(
            description=f"Diagnostics for patient {patient_id}",
            priority=3,
            metadata={"patient_id": patient_id},
        )
        self.assign_task(task)

        report: Dict[str, Any] = {
            "task_id": task.task_id,
            "patient_id": patient_id,
            "robot_id": self.robot_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "vitals": {
                "heart_rate": "normal",
                "blood_pressure": "normal",
                "oxygen_saturation": "normal",
                "temperature": "normal",
            },
            "notes": "Placeholder diagnostic — connect to medical sensor API for real data.",
        }
        self._active_patients[patient_id] = report
        return report

    def deliver_medication(
        self, patient_id: str, medication: str
    ) -> Dict[str, Any]:
        """
        Deliver *medication* to *patient_id*.

        Returns a delivery confirmation record.
        """
        task = Task(
            description=f"Deliver {medication} to patient {patient_id}",
            priority=2,
            metadata={"patient_id": patient_id, "medication": medication},
        )
        self.assign_task(task)

        return {
            "task_id": task.task_id,
            "patient_id": patient_id,
            "medication": medication,
            "robot_id": self.robot_id,
            "delivery_status": "en_route",
            "estimated_delivery": datetime.now(timezone.utc).isoformat(),
        }

    def monitor_patient(self, patient_id: str) -> Dict[str, Any]:
        """
        Start continuous monitoring for *patient_id*.

        Returns monitoring session details.
        """
        task = Task(
            description=f"Monitor patient {patient_id}",
            priority=4,
            metadata={"patient_id": patient_id},
        )
        self.assign_task(task)
        self._active_patients[patient_id] = {
            "patient_id": patient_id,
            "monitoring": True,
            "started_at": datetime.now(timezone.utc).isoformat(),
        }

        return {
            "task_id": task.task_id,
            "patient_id": patient_id,
            "robot_id": self.robot_id,
            "monitoring_active": True,
            "started_at": datetime.now(timezone.utc).isoformat(),
        }

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "capabilities": self.CAPABILITIES,
                "active_patients": len(self._active_patients),
                "incidents_logged": len(self._incident_log),
            }
        )
        return base
