# Service Robots

City service robot module for **Robot City**.  
Each robot type is a specialised subclass of `ServiceRobot`.

---

## Available Robot Types

| Class | `RobotType` | Capabilities |
|---|---|---|
| `MedicalRobot` | `MEDICAL` | first_aid, diagnostics, medication_delivery, patient_monitoring, emergency_response |
| `SecurityRobotService` | `SECURITY` | patrol, surveillance, threat_detection, access_control, incident_response |
| `TransportRobot` | `TRANSPORT` | passenger_transport, cargo_delivery, route_optimization, traffic_management |
| `CommerceRobot` | `COMMERCE` | inventory_management, customer_service, payment_processing, product_recommendation |
| `ConstructionRobot` | `CONSTRUCTION` | building, demolition, maintenance, inspection, material_transport |
| `EducationRobot` | `EDUCATION` | tutoring, curriculum_delivery, student_assessment, resource_management, interactive_learning |

---

## Quick Start

```python
from service_robots import (
    MedicalRobot,
    SecurityRobotService,
    ServiceRobotRegistry,
    RobotType,
    Task,
)
from service_robots.base_robot import Location

# Create robots
medic = MedicalRobot("MediBot-1")
guard = SecurityRobotService("GuardBot-1")

# Register in the city registry
registry = ServiceRobotRegistry()
registry.register_robot(medic)
registry.register_robot(guard)

# Dispatch a robot for a task
task = Task(description="Emergency response required", priority=1)
robot = registry.dispatch_robot(RobotType.MEDICAL, task)
print(robot.to_dict())

# Direct API usage
emergency = medic.respond_emergency(Location(10.0, 20.0, "City Square"), severity=2)
print(emergency)

# Print registry statistics
print(registry.get_stats())
```

---

## Robot Lifecycle

```
IDLE ──assign_task──► ACTIVE ──complete_task──► IDLE
                               │
                    battery<10%▼
                            CHARGING
```

- **IDLE** – robot is waiting for tasks  
- **ACTIVE** – executing a task  
- **CHARGING** – battery below 10 %, recharging  
- **MAINTENANCE** – undergoing maintenance (set manually)  
- **OFFLINE** – powered off  

---

## Adding a New Robot Type

1. Add a member to `RobotType` in `base_robot.py`.
2. Create `my_robot.py` extending `ServiceRobot`:

```python
from .base_robot import RobotType, ServiceRobot

class MyRobot(ServiceRobot):
    CAPABILITIES = ["capability_a", "capability_b"]

    def __init__(self, name, **kwargs):
        super().__init__(name, RobotType.MY_TYPE, **kwargs)

    def my_action(self, param: str) -> dict:
        ...

    def to_dict(self) -> dict:
        base = super().to_dict()
        base["capabilities"] = self.CAPABILITIES
        return base
```

3. Import and export from `__init__.py`.
4. Register in `ServiceRobotRegistry`.

---

## Module Structure

```
service-robots/
├── __init__.py            # Public API
├── base_robot.py          # ServiceRobot, RobotStatus, RobotType, Task, Location
├── medical_robot.py       # MedicalRobot
├── security_robot.py      # SecurityRobotService
├── transport_robot.py     # TransportRobot
├── commerce_robot.py      # CommerceRobot
├── construction_robot.py  # ConstructionRobot
├── education_robot.py     # EducationRobot
└── robot_registry.py      # ServiceRobotRegistry
```

All implementations rely solely on the Python standard library.
