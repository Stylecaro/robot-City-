"""
Sistema de Robots de Seguridad y Control
Aplicación de reglas, detección de violaciones y respuesta.
Integrado con sistema de prisión para sentencias automáticas.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import uuid

# Importar el sistema de prisión para sentencias automáticas
from prison_system import prison_manager


class RuleSeverity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class EnforcementAction(Enum):
    WARNING = "warning"
    REMOVE = "remove"
    FINE = "fine"
    TEMP_BAN = "temp_ban"
    ESCALATE = "escalate"


@dataclass
class CityRule:
    rule_id: str
    title: str
    description: str
    severity: RuleSeverity
    zone_id: Optional[str] = None


@dataclass
class Violation:
    violation_id: str
    player_id: str
    rule_id: str
    zone_id: Optional[str]
    timestamp: str
    severity: RuleSeverity
    details: str
    resolved: bool = False
    action_taken: Optional[EnforcementAction] = None


@dataclass
class SecurityRobot:
    robot_id: str
    name: str
    zone_id: Optional[str]
    patrol_radius: float
    active: bool = True
    incidents_handled: int = 0
    last_action: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "robot_id": self.robot_id,
            "name": self.name,
            "zone_id": self.zone_id,
            "patrol_radius": self.patrol_radius,
            "active": self.active,
            "incidents_handled": self.incidents_handled,
            "last_action": self.last_action
        }


class SecurityRobotsManager:
    """Gestor de robots de seguridad y reglas"""

    def __init__(self):
        self.rules: Dict[str, CityRule] = {}
        self.robots: Dict[str, SecurityRobot] = {}
        self.violations: List[Violation] = []
        self._seed_default_rules()
        self._seed_default_robots()

    def _seed_default_rules(self) -> None:
        default_rules = [
            ("Acceso no autorizado", "Entrada a edificios restringidos", RuleSeverity.HIGH),
            ("Sabotaje", "Daño a infraestructura crítica", RuleSeverity.CRITICAL),
            ("Interferencia", "Interrumpir operaciones de la ciudad", RuleSeverity.MEDIUM),
            ("Fraude financiero", "Manipulación de mercado", RuleSeverity.HIGH),
            ("Riesgo público", "Amenaza a ciudadanos", RuleSeverity.CRITICAL)
        ]
        for title, desc, severity in default_rules:
            rule_id = str(uuid.uuid4())
            self.rules[rule_id] = CityRule(rule_id, title, desc, severity)

    def _seed_default_robots(self) -> None:
        for idx in range(1, 6):
            robot_id = f"SEC-{idx:03d}"
            self.robots[robot_id] = SecurityRobot(
                robot_id=robot_id,
                name=f"Guardian {idx}",
                zone_id=None,
                patrol_radius=200.0
            )

    def add_rule(self, title: str, description: str, severity: RuleSeverity, zone_id: Optional[str] = None) -> CityRule:
        rule_id = str(uuid.uuid4())
        rule = CityRule(rule_id, title, description, severity, zone_id)
        self.rules[rule_id] = rule
        return rule

    def ensure_rule(self, title: str, description: str, severity: RuleSeverity, zone_id: Optional[str] = None) -> CityRule:
        """Obtiene regla existente por título o la crea"""
        for rule in self.rules.values():
            if rule.title.lower() == title.lower() and rule.zone_id == zone_id:
                return rule
        return self.add_rule(title, description, severity, zone_id)

    def register_robot(self, name: str, zone_id: Optional[str] = None, patrol_radius: float = 200.0) -> SecurityRobot:
        robot_id = str(uuid.uuid4())
        robot = SecurityRobot(robot_id, name, zone_id, patrol_radius)
        self.robots[robot_id] = robot
        return robot

    def assign_robot(self, robot_id: str, zone_id: str) -> bool:
        robot = self.robots.get(robot_id)
        if not robot:
            return False
        robot.zone_id = zone_id
        return True

    def report_violation(self, player_id: str, rule_id: str, zone_id: Optional[str], details: str) -> Violation:
        rule = self.rules.get(rule_id)
        if not rule:
            raise ValueError("Rule not found")

        violation = Violation(
            violation_id=str(uuid.uuid4()),
            player_id=player_id,
            rule_id=rule_id,
            zone_id=zone_id,
            timestamp=datetime.now().isoformat(),
            severity=rule.severity,
            details=details
        )
        self.violations.append(violation)
        return violation

    def report_and_enforce(self, player_id: str, rule_id: str, zone_id: Optional[str], details: str) -> Violation:
        """Registra violación y aplica sanción automática"""
        violation = self.report_violation(player_id, rule_id, zone_id, details)
        return self.enforce_violation(violation.violation_id)

    def enforce_violation(self, violation_id: str) -> Violation:
        violation = next((v for v in self.violations if v.violation_id == violation_id), None)
        if not violation:
            raise ValueError("Violation not found")

        action = self._choose_action(violation.severity)
        violation.action_taken = action
        violation.resolved = True

        # Aplicar sentencia de prisión automática para violaciones graves
        if violation.severity == RuleSeverity.HIGH:
            prison_manager.sentence_player(
                player_id=violation.player_id,
                reason=f"Violación de regla: {self.rules[violation.rule_id].title}",
                duration_minutes=60  # 60 minutos para HIGH
            )
        elif violation.severity == RuleSeverity.CRITICAL:
            prison_manager.sentence_player(
                player_id=violation.player_id,
                reason=f"Violación crítica: {self.rules[violation.rule_id].title}",
                duration_minutes=180  # 180 minutos (3 horas) para CRITICAL
            )

        robot = self._find_available_robot(violation.zone_id)
        if robot:
            robot.incidents_handled += 1
            robot.last_action = f"{action.value} for {violation.player_id}"

        return violation

    def _choose_action(self, severity: RuleSeverity) -> EnforcementAction:
        if severity == RuleSeverity.LOW:
            return EnforcementAction.WARNING
        if severity == RuleSeverity.MEDIUM:
            return EnforcementAction.FINE
        if severity == RuleSeverity.HIGH:
            return EnforcementAction.REMOVE
        return EnforcementAction.ESCALATE

    def _find_available_robot(self, zone_id: Optional[str]) -> Optional[SecurityRobot]:
        for robot in self.robots.values():
            if robot.active and (robot.zone_id == zone_id or robot.zone_id is None):
                return robot
        return None

    def get_zone_security(self, zone_id: str) -> Dict:
        zone_robots = [r.to_dict() for r in self.robots.values() if r.zone_id == zone_id]
        recent = [v for v in self.violations if v.zone_id == zone_id][-10:]
        return {
            "zone_id": zone_id,
            "robots": zone_robots,
            "recent_violations": [self._violation_to_dict(v) for v in recent]
        }

    def get_robots(self) -> List[Dict]:
        return [r.to_dict() for r in self.robots.values()]

    def get_rules(self) -> List[Dict]:
        return [
            {
                "rule_id": r.rule_id,
                "title": r.title,
                "description": r.description,
                "severity": r.severity.name,
                "zone_id": r.zone_id
            }
            for r in self.rules.values()
        ]

    def get_recent_violations(self, limit: int = 20) -> List[Dict]:
        return [self._violation_to_dict(v) for v in self.violations[-limit:]]

    def _violation_to_dict(self, v: Violation) -> Dict:
        return {
            "violation_id": v.violation_id,
            "player_id": v.player_id,
            "rule_id": v.rule_id,
            "zone_id": v.zone_id,
            "timestamp": v.timestamp,
            "severity": v.severity.name,
            "details": v.details,
            "resolved": v.resolved,
            "action_taken": v.action_taken.value if v.action_taken else None
        }


security_robots_manager = SecurityRobotsManager()
