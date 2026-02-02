"""
Endpoints de Seguridad - Robots y Reglas
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from security_system.security_robots import (
    security_robots_manager,
    RuleSeverity
)

router = APIRouter(prefix="/api/security", tags=["security"])


class CreateRuleRequest(BaseModel):
    title: str
    description: str
    severity: str
    zone_id: Optional[str] = None


class RegisterRobotRequest(BaseModel):
    name: str
    zone_id: Optional[str] = None
    patrol_radius: float = 200.0


class AssignRobotRequest(BaseModel):
    robot_id: str
    zone_id: str


class ReportViolationRequest(BaseModel):
    player_id: str
    rule_id: str
    zone_id: Optional[str] = None
    details: str


class EnforceViolationRequest(BaseModel):
    violation_id: str


@router.get("/rules")
async def get_rules():
    return {"rules": security_robots_manager.get_rules()}


@router.post("/rules")
async def create_rule(request: CreateRuleRequest):
    try:
        severity = RuleSeverity[request.severity.upper()]
        rule = security_robots_manager.add_rule(
            request.title,
            request.description,
            severity,
            request.zone_id
        )
        return {"rule": {
            "rule_id": rule.rule_id,
            "title": rule.title,
            "description": rule.description,
            "severity": rule.severity.name,
            "zone_id": rule.zone_id
        }}
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid severity")


@router.get("/robots")
async def get_robots():
    return {"robots": security_robots_manager.get_robots()}


@router.post("/robots")
async def register_robot(request: RegisterRobotRequest):
    robot = security_robots_manager.register_robot(
        request.name,
        request.zone_id,
        request.patrol_radius
    )
    return {"robot": robot.to_dict()}


@router.post("/robots/assign")
async def assign_robot(request: AssignRobotRequest):
    if not security_robots_manager.assign_robot(request.robot_id, request.zone_id):
        raise HTTPException(status_code=404, detail="Robot not found")
    return {"status": "assigned", "robot_id": request.robot_id, "zone_id": request.zone_id}


@router.post("/violations")
async def report_violation(request: ReportViolationRequest):
    try:
        violation = security_robots_manager.report_violation(
            request.player_id,
            request.rule_id,
            request.zone_id,
            request.details
        )
        return {"violation": security_robots_manager._violation_to_dict(violation)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/violations/enforce")
async def enforce_violation(request: EnforceViolationRequest):
    try:
        violation = security_robots_manager.enforce_violation(request.violation_id)
        return {"violation": security_robots_manager._violation_to_dict(violation)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/violations/recent")
async def get_recent_violations(limit: int = 20):
    return {"violations": security_robots_manager.get_recent_violations(limit)}


@router.get("/zones/{zone_id}")
async def get_zone_security(zone_id: str):
    return security_robots_manager.get_zone_security(zone_id)
