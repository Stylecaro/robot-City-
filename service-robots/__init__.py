"""
service-robots — City Service Robot APIs
Provides service robot classes for: medical, security, transport,
commerce, construction, and education city services.
"""
from .base_robot import ServiceRobot, RobotStatus, RobotType
from .medical_robot import MedicalRobot
from .security_robot import SecurityRobotService
from .transport_robot import TransportRobot
from .commerce_robot import CommerceRobot
from .construction_robot import ConstructionRobot
from .education_robot import EducationRobot
from .robot_registry import ServiceRobotRegistry

__all__ = [
    "ServiceRobot",
    "RobotStatus",
    "RobotType",
    "MedicalRobot",
    "SecurityRobotService",
    "TransportRobot",
    "CommerceRobot",
    "ConstructionRobot",
    "EducationRobot",
    "ServiceRobotRegistry",
]
