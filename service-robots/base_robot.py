"""
base_robot.py — Base classes for all City Service Robots.

Defines the shared RobotStatus/RobotType enumerations and the
abstract ServiceRobot base class that every specialised robot extends.
"""

from __future__ import annotations

import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Deque, Dict, List, Optional


class RobotStatus(Enum):
    """Operational states a service robot can be in."""

    IDLE = "idle"
    ACTIVE = "active"
    CHARGING = "charging"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class RobotType(Enum):
    """Service categories for city robots."""

    MEDICAL = "medical"
    SECURITY = "security"
    TRANSPORT = "transport"
    COMMERCE = "commerce"
    CONSTRUCTION = "construction"
    EDUCATION = "education"


@dataclass
class Location:
    """Simple 2-D city coordinate with an optional label."""

    x: float
    y: float
    label: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"x": self.x, "y": self.y, "label": self.label}


@dataclass
class Task:
    """A unit of work that can be assigned to a robot."""

    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    priority: int = 5  # 1 (highest) … 10 (lowest)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "description": self.description,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }


class ServiceRobot:
    """
    Abstract base class for every city service robot.

    Subclasses must implement the ``execute_task`` method and should
    call ``super().__init__()`` with all required arguments.
    """

    def __init__(
        self,
        name: str,
        robot_type: RobotType,
        *,
        robot_id: Optional[str] = None,
        initial_location: Optional[Location] = None,
        battery_level: float = 100.0,
    ) -> None:
        self.robot_id: str = robot_id or str(uuid.uuid4())
        self.name: str = name
        self.robot_type: RobotType = robot_type
        self.status: RobotStatus = RobotStatus.IDLE
        self.location: Location = initial_location or Location(0.0, 0.0)
        self.battery_level: float = max(0.0, min(100.0, battery_level))
        self._tasks: Deque[Task] = deque()
        self._current_task: Optional[Task] = None
        self._completed_tasks: List[Task] = []
        self._created_at: datetime = datetime.now(timezone.utc)

    # ------------------------------------------------------------------
    # Task management
    # ------------------------------------------------------------------

    def assign_task(self, task: Task) -> None:
        """Add *task* to the robot's pending queue."""
        self._tasks.append(task)
        if self.status == RobotStatus.IDLE:
            self._start_next_task()

    def complete_task(self) -> Optional[Task]:
        """
        Mark the current task as completed.

        Returns the completed task, or ``None`` if no task was active.
        """
        if self._current_task is None:
            return None
        completed = self._current_task
        self._completed_tasks.append(completed)
        self._current_task = None
        self._start_next_task()
        return completed

    def _start_next_task(self) -> None:
        """Dequeue the next pending task and set the robot to ACTIVE."""
        if self._tasks:
            self._current_task = self._tasks.popleft()
            self.status = RobotStatus.ACTIVE
        else:
            self.status = RobotStatus.IDLE

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------

    def update_status(self, status: RobotStatus) -> None:
        """Manually override the robot's operational status."""
        self.status = status

    def update_location(self, location: Location) -> None:
        """Move the robot to a new city coordinate."""
        self.location = location

    def update_battery(self, level: float) -> None:
        """Set the battery level (0–100 %)."""
        self.battery_level = max(0.0, min(100.0, level))
        if self.battery_level < 10.0 and self.status not in (
            RobotStatus.CHARGING,
            RobotStatus.OFFLINE,
        ):
            self.status = RobotStatus.CHARGING

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serialisable representation of the robot."""
        return {
            "robot_id": self.robot_id,
            "name": self.name,
            "robot_type": self.robot_type.value,
            "status": self.status.value,
            "location": self.location.to_dict(),
            "battery_level": self.battery_level,
            "current_task": self._current_task.to_dict() if self._current_task else None,
            "pending_tasks": len(self._tasks),
            "completed_tasks": len(self._completed_tasks),
            "created_at": self._created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} id={self.robot_id!r} "
            f"name={self.name!r} status={self.status.value}>"
        )
