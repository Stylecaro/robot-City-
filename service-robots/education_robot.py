"""
education_robot.py — Education Service Robot

Provides tutoring, curriculum delivery, student assessment,
learning resource management, and interactive learning sessions.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from base_robot import Location, RobotType, ServiceRobot, Task


class EducationRobot(ServiceRobot):
    """
    A service robot specialised in city education services.

    Capabilities
    ------------
    tutoring, curriculum_delivery, student_assessment,
    resource_management, interactive_learning
    """

    CAPABILITIES: List[str] = [
        "tutoring",
        "curriculum_delivery",
        "student_assessment",
        "resource_management",
        "interactive_learning",
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
            RobotType.EDUCATION,
            robot_id=robot_id,
            initial_location=initial_location,
            battery_level=battery_level,
        )
        self._lesson_log: List[Dict[str, Any]] = []
        self._assessment_log: List[Dict[str, Any]] = []
        self._resource_log: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Education operations
    # ------------------------------------------------------------------

    def start_lesson(
        self, student_id: str, subject: str, level: str
    ) -> Dict[str, Any]:
        """
        Begin a lesson session for *student_id*.

        Parameters
        ----------
        student_id:
            Unique student identifier.
        subject:
            E.g. ``"mathematics"``, ``"robotics"``, ``"history"``.
        level:
            Difficulty / grade level, e.g. ``"beginner"``, ``"grade_5"``.

        Returns
        -------
        dict
            Lesson session details with task_id.
        """
        task = Task(
            description=f"Lesson: {subject} ({level}) for student {student_id}",
            priority=5,
            metadata={
                "student_id": student_id,
                "subject": subject,
                "level": level,
            },
        )
        self.assign_task(task)

        record: Dict[str, Any] = {
            "task_id": task.task_id,
            "student_id": student_id,
            "subject": subject,
            "level": level,
            "robot_id": self.robot_id,
            "status": "in_session",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "notes": "Placeholder — integrate with city curriculum database.",
        }
        self._lesson_log.append(record)
        return record

    def assess_student(self, student_id: str, subject: str) -> Dict[str, Any]:
        """
        Run an assessment for *student_id* in *subject*.

        Returns a placeholder assessment report; real integration would
        query the city's learning management system (LMS).
        """
        task = Task(
            description=f"Assess student {student_id} in {subject}",
            priority=4,
            metadata={"student_id": student_id, "subject": subject},
        )
        self.assign_task(task)

        report: Dict[str, Any] = {
            "task_id": task.task_id,
            "student_id": student_id,
            "subject": subject,
            "robot_id": self.robot_id,
            "score": None,  # TODO: derive from LMS data
            "level_achieved": None,
            "recommendations": [],
            "assessed_at": datetime.now(timezone.utc).isoformat(),
            "notes": "Placeholder assessment — integrate with city LMS.",
        }
        self._assessment_log.append(report)
        return report

    def provide_resource(
        self, student_id: str, resource_type: str
    ) -> Dict[str, Any]:
        """
        Deliver a learning resource to *student_id*.

        Parameters
        ----------
        resource_type:
            E.g. ``"video"``, ``"worksheet"``, ``"interactive_sim"``.
        """
        task = Task(
            description=f"Provide {resource_type} resource to student {student_id}",
            priority=6,
            metadata={"student_id": student_id, "resource_type": resource_type},
        )
        self.assign_task(task)

        record: Dict[str, Any] = {
            "task_id": task.task_id,
            "student_id": student_id,
            "resource_type": resource_type,
            "robot_id": self.robot_id,
            "resource_url": None,  # TODO: resolve from content library
            "delivered_at": datetime.now(timezone.utc).isoformat(),
            "notes": "Placeholder — integrate with city content library.",
        }
        self._resource_log.append(record)
        return record

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update(
            {
                "capabilities": self.CAPABILITIES,
                "lessons_logged": len(self._lesson_log),
                "assessments_logged": len(self._assessment_log),
                "resources_logged": len(self._resource_log),
            }
        )
        return base
