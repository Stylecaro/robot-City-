"""
robot_registry.py — Central registry and dispatcher for service robots.

The ServiceRobotRegistry keeps track of all registered robots, provides
lookup by type or status, and dispatches the best available robot for a
given task.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from base_robot import RobotStatus, RobotType, ServiceRobot, Task


class ServiceRobotRegistry:
    """
    A central in-memory registry for all city service robots.

    Usage
    -----
    ::

        registry = ServiceRobotRegistry()
        registry.register_robot(my_robot)
        robot = registry.dispatch_robot(RobotType.MEDICAL, task)
    """

    def __init__(self) -> None:
        self._robots: Dict[str, ServiceRobot] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_robot(self, robot: ServiceRobot) -> None:
        """Add *robot* to the registry, keyed by its robot_id."""
        self._robots[robot.robot_id] = robot

    def deregister_robot(self, robot_id: str) -> bool:
        """
        Remove the robot with *robot_id* from the registry.

        Returns ``True`` if the robot was present and removed,
        ``False`` if it was not found.
        """
        if robot_id in self._robots:
            del self._robots[robot_id]
            return True
        return False

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_robot(self, robot_id: str) -> Optional[ServiceRobot]:
        """Return the robot with *robot_id*, or ``None``."""
        return self._robots.get(robot_id)

    def get_robots_by_type(self, robot_type: RobotType) -> List[ServiceRobot]:
        """Return all robots of the given *robot_type*."""
        return [r for r in self._robots.values() if r.robot_type == robot_type]

    def get_available_robots(
        self, robot_type: Optional[RobotType] = None
    ) -> List[ServiceRobot]:
        """
        Return robots that are IDLE or ACTIVE.

        Parameters
        ----------
        robot_type:
            If provided, filter by this type.
        """
        available_statuses = {RobotStatus.IDLE, RobotStatus.ACTIVE}
        robots = [
            r for r in self._robots.values() if r.status in available_statuses
        ]
        if robot_type is not None:
            robots = [r for r in robots if r.robot_type == robot_type]
        return robots

    def get_all_robots(self) -> List[ServiceRobot]:
        """Return a list of every registered robot."""
        return list(self._robots.values())

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """
        Return aggregate counts broken down by type and status.

        Returns
        -------
        dict
            ``{"total": int, "by_type": {...}, "by_status": {...}}``
        """
        by_type: Dict[str, int] = {t.value: 0 for t in RobotType}
        by_status: Dict[str, int] = {s.value: 0 for s in RobotStatus}

        for robot in self._robots.values():
            by_type[robot.robot_type.value] += 1
            by_status[robot.status.value] += 1

        return {
            "total": len(self._robots),
            "by_type": by_type,
            "by_status": by_status,
        }

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    def dispatch_robot(
        self,
        robot_type: "Union[RobotType, str]",
        task: "Union[Task, str]",
    ) -> "Optional[Dict[str, Any]]":
        """
        Assign *task* to the best available robot of *robot_type*.

        Both *robot_type* and *task* may be passed as strings for
        convenience (e.g. ``dispatch_robot("medical", "emergency")``).

        Selection strategy:

        1. Prefer IDLE robots over ACTIVE ones.
        2. Among equal-status robots, prefer higher battery level.

        Returns a dict ``{"success": True, "robot_id": ..., "robot": ...}``
        or ``{"success": False, "reason": ...}`` when no robot is available.
        """
        # Coerce string → RobotType
        if isinstance(robot_type, str):
            try:
                robot_type = RobotType(robot_type.lower())
            except ValueError:
                return {"success": False, "reason": f"Unknown robot_type '{robot_type}'"}

        # Coerce string → Task
        if isinstance(task, str):
            from base_robot import Task as _Task
            task = _Task(description=task)

        candidates = self.get_available_robots(robot_type)
        if not candidates:
            return {"success": False, "reason": f"No available {robot_type.value} robot"}

        # Sort: IDLE before ACTIVE, then descending battery level.
        def _key(r: ServiceRobot) -> tuple:
            status_priority = 0 if r.status == RobotStatus.IDLE else 1
            return (status_priority, -r.battery_level)

        best = min(candidates, key=_key)
        best.assign_task(task)
        return {"success": True, "robot_id": best.robot_id, "robot": best.to_dict()}
