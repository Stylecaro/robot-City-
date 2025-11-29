"""
Motor de Decisiones - Sistema de toma de decisiones inteligentes
Procesa información compleja y toma decisiones estratégicas para la ciudad
"""

import asyncio
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import json

logger = logging.getLogger("decision_engine")

class DecisionType(Enum):
    """Tipos de decisiones"""
    RESOURCE_ALLOCATION = "resource_allocation"
    EMERGENCY_RESPONSE = "emergency_response"
    OPTIMIZATION = "optimization"
    SECURITY = "security"
    MAINTENANCE = "maintenance"
    PLANNING = "planning"
    COMMUNICATION = "communication"
    ADAPTIVE = "adaptive"

class Priority(Enum):
    """Niveles de prioridad"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class DecisionContext:
    """Contexto para toma de decisiones"""
    situation_type: str
    urgency_level: float  # 0.0 - 1.0
    available_resources: Dict[str, float]
    constraints: List[str]
    objectives: List[str]
    stakeholders: List[str]
    time_limit: Optional[float]  # seconds

@dataclass
class DecisionOption:
    """Opción de decisión"""
    id: str
    name: str
    description: str
    expected_outcome: Dict[str, float]
    resource_cost: Dict[str, float]
    risk_level: float
    confidence: float
    implementation_time: float

@dataclass
class DecisionResult:
    """Resultado de una decisión"""
    selected_option: DecisionOption
    reasoning: str
    confidence_score: float
    alternative_options: List[DecisionOption]
    implementation_plan: List[Dict[str, Any]]
    monitoring_metrics: List[str]

class DecisionEngine:
    """Motor principal de decisiones"""
    
    def __init__(self):
        self.decision_history = []
        self.active_decisions = {}
        self.decision_rules = self._initialize_decision_rules()
        self.learning_weights = self._initialize_learning_weights()
        
        # Contexto del sistema
        self.system_context = {
            "current_load": 0.5,
            "available_resources": {
                "cpu": 0.7,
                "memory": 0.6,
                "bandwidth": 0.8,
                "robots": 0.9,
                "energy": 0.85
            },
            "security_status": "normal",
            "emergency_level": 0.0,
            "optimization_mode": "balanced"
        }
        
        logger.info("Decision Engine inicializado")
    
    def _initialize_decision_rules(self) -> Dict[str, Dict]:
        """Inicializar reglas de decisión"""
        return {
            "emergency_response": {
                "max_response_time": 30.0,  # seconds
                "resource_priority": ["robots", "communication", "energy"],
                "escalation_threshold": 0.7,
                "fallback_strategy": "manual_intervention"
            },
            "resource_allocation": {
                "efficiency_weight": 0.4,
                "fairness_weight": 0.3,
                "urgency_weight": 0.3,
                "min_reserve_percentage": 0.2
            },
            "optimization": {
                "improvement_threshold": 0.05,
                "risk_tolerance": 0.3,
                "rollback_enabled": True,
                "test_duration": 300.0  # seconds
            },
            "security": {
                "threat_escalation": [0.3, 0.6, 0.8],
                "response_protocols": ["monitor", "alert", "lockdown"],
                "false_positive_tolerance": 0.1
            }
        }
    
    def _initialize_learning_weights(self) -> Dict[str, float]:
        """Inicializar pesos de aprendizaje"""
        return {
            "historical_success": 0.3,
            "context_similarity": 0.25,
            "resource_efficiency": 0.2,
            "outcome_quality": 0.15,
            "stakeholder_satisfaction": 0.1
        }
    
    async def make_decision(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Hacer una decisión basada en la solicitud"""
        try:
            # Parsear contexto de la decisión
            context = self._parse_decision_context(request)
            
            # Generar opciones de decisión
            options = await self._generate_decision_options(context)
            
            # Evaluar opciones
            evaluated_options = await self._evaluate_options(options, context)
            
            # Seleccionar mejor opción
            best_option = await self._select_best_option(evaluated_options, context)
            
            # Crear plan de implementación
            implementation_plan = await self._create_implementation_plan(best_option, context)
            
            # Crear resultado de decisión
            result = DecisionResult(
                selected_option=best_option,
                reasoning=await self._generate_reasoning(best_option, evaluated_options, context),
                confidence_score=best_option.confidence,
                alternative_options=evaluated_options[:3],  # Top 3 alternativas
                implementation_plan=implementation_plan,
                monitoring_metrics=self._get_monitoring_metrics(best_option, context)
            )
            
            # Guardar decisión en historial
            self._save_decision(context, result)
            
            logger.info(f"Decisión tomada: {best_option.name} (confianza: {best_option.confidence:.2f})")
            
            return {
                "decision": asdict(result),
                "status": "success",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error en toma de decisión: {e}")
            return {
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.now().isoformat()
            }
    
    def _parse_decision_context(self, request: Dict[str, Any]) -> DecisionContext:
        """Parsear contexto de decisión desde la solicitud"""
        return DecisionContext(
            situation_type=request.get("situation_type", "general"),
            urgency_level=request.get("urgency_level", 0.5),
            available_resources=request.get("available_resources", self.system_context["available_resources"]),
            constraints=request.get("constraints", []),
            objectives=request.get("objectives", ["optimize_efficiency"]),
            stakeholders=request.get("stakeholders", ["system"]),
            time_limit=request.get("time_limit")
        )
    
    async def _generate_decision_options(self, context: DecisionContext) -> List[DecisionOption]:
        """Generar opciones de decisión basadas en el contexto"""
        situation_type = context.situation_type
        
        if situation_type == "robot_deployment":
            return await self._generate_robot_deployment_options(context)
        elif situation_type == "resource_optimization":
            return await self._generate_resource_optimization_options(context)
        elif situation_type == "emergency_response":
            return await self._generate_emergency_response_options(context)
        elif situation_type == "system_maintenance":
            return await self._generate_maintenance_options(context)
        elif situation_type == "traffic_management":
            return await self._generate_traffic_management_options(context)
        else:
            return await self._generate_general_options(context)
    
    async def _generate_robot_deployment_options(self, context: DecisionContext) -> List[DecisionOption]:
        """Generar opciones para despliegue de robots"""
        options = []
        
        # Opción 1: Despliegue conservador
        options.append(DecisionOption(
            id="conservative_deployment",
            name="Despliegue Conservador",
            description="Desplegar robots gradualmente con monitoreo intensivo",
            expected_outcome={
                "efficiency": 0.7,
                "reliability": 0.9,
                "cost": 0.6
            },
            resource_cost={
                "robots": 0.3,
                "energy": 0.4,
                "monitoring": 0.8
            },
            risk_level=0.2,
            confidence=0.85,
            implementation_time=300.0
        ))
        
        # Opción 2: Despliegue agresivo
        options.append(DecisionOption(
            id="aggressive_deployment",
            name="Despliegue Agresivo",
            description="Desplegar robots rápidamente para máxima eficiencia",
            expected_outcome={
                "efficiency": 0.95,
                "reliability": 0.7,
                "cost": 0.8
            },
            resource_cost={
                "robots": 0.8,
                "energy": 0.7,
                "monitoring": 0.5
            },
            risk_level=0.6,
            confidence=0.7,
            implementation_time=120.0
        ))
        
        # Opción 3: Despliegue balanceado
        options.append(DecisionOption(
            id="balanced_deployment",
            name="Despliegue Balanceado",
            description="Balance entre eficiencia y seguridad",
            expected_outcome={
                "efficiency": 0.8,
                "reliability": 0.8,
                "cost": 0.7
            },
            resource_cost={
                "robots": 0.5,
                "energy": 0.5,
                "monitoring": 0.6
            },
            risk_level=0.4,
            confidence=0.8,
            implementation_time=180.0
        ))
        
        return options
    
    async def _generate_resource_optimization_options(self, context: DecisionContext) -> List[DecisionOption]:
        """Generar opciones para optimización de recursos"""
        options = []
        
        options.append(DecisionOption(
            id="cpu_optimization",
            name="Optimización de CPU",
            description="Optimizar uso de procesamiento",
            expected_outcome={
                "cpu_efficiency": 0.85,
                "response_time": 0.9,
                "throughput": 0.8
            },
            resource_cost={
                "cpu": 0.1,
                "memory": 0.05
            },
            risk_level=0.2,
            confidence=0.9,
            implementation_time=60.0
        ))
        
        options.append(DecisionOption(
            id="memory_optimization",
            name="Optimización de Memoria",
            description="Optimizar uso de memoria del sistema",
            expected_outcome={
                "memory_efficiency": 0.9,
                "stability": 0.85,
                "performance": 0.8
            },
            resource_cost={
                "memory": 0.1,
                "cpu": 0.05
            },
            risk_level=0.3,
            confidence=0.85,
            implementation_time=90.0
        ))
        
        return options
    
    async def _generate_emergency_response_options(self, context: DecisionContext) -> List[DecisionOption]:
        """Generar opciones para respuesta de emergencia"""
        options = []
        
        options.append(DecisionOption(
            id="immediate_isolation",
            name="Aislamiento Inmediato",
            description="Aislar área afectada inmediatamente",
            expected_outcome={
                "containment": 0.95,
                "service_continuity": 0.3,
                "recovery_time": 0.6
            },
            resource_cost={
                "robots": 0.8,
                "communication": 0.9
            },
            risk_level=0.4,
            confidence=0.9,
            implementation_time=30.0
        ))
        
        options.append(DecisionOption(
            id="gradual_response",
            name="Respuesta Gradual",
            description="Respuesta escalada manteniendo servicios",
            expected_outcome={
                "containment": 0.7,
                "service_continuity": 0.8,
                "recovery_time": 0.8
            },
            resource_cost={
                "robots": 0.5,
                "communication": 0.6
            },
            risk_level=0.6,
            confidence=0.75,
            implementation_time=120.0
        ))
        
        return options
    
    async def _generate_maintenance_options(self, context: DecisionContext) -> List[DecisionOption]:
        """Generar opciones para mantenimiento del sistema"""
        return [
            DecisionOption(
                id="preventive_maintenance",
                name="Mantenimiento Preventivo",
                description="Mantenimiento programado regular",
                expected_outcome={"reliability": 0.9, "downtime": 0.1, "cost": 0.6},
                resource_cost={"robots": 0.3, "time": 0.2},
                risk_level=0.1,
                confidence=0.95,
                implementation_time=1800.0
            ),
            DecisionOption(
                id="reactive_maintenance",
                name="Mantenimiento Reactivo",
                description="Mantenimiento solo cuando sea necesario",
                expected_outcome={"reliability": 0.6, "downtime": 0.4, "cost": 0.3},
                resource_cost={"robots": 0.1, "time": 0.1},
                risk_level=0.7,
                confidence=0.6,
                implementation_time=600.0
            )
        ]
    
    async def _generate_traffic_management_options(self, context: DecisionContext) -> List[DecisionOption]:
        """Generar opciones para gestión de tráfico"""
        return [
            DecisionOption(
                id="dynamic_routing",
                name="Enrutamiento Dinámico",
                description="Ajustar rutas en tiempo real",
                expected_outcome={"flow_efficiency": 0.9, "delay_reduction": 0.8},
                resource_cost={"cpu": 0.4, "communication": 0.6},
                risk_level=0.3,
                confidence=0.8,
                implementation_time=90.0
            ),
            DecisionOption(
                id="load_balancing",
                name="Balanceo de Carga",
                description="Distribuir tráfico uniformemente",
                expected_outcome={"flow_efficiency": 0.75, "delay_reduction": 0.6},
                resource_cost={"cpu": 0.2, "communication": 0.3},
                risk_level=0.2,
                confidence=0.85,
                implementation_time=60.0
            )
        ]
    
    async def _generate_general_options(self, context: DecisionContext) -> List[DecisionOption]:
        """Generar opciones generales"""
        return [
            DecisionOption(
                id="default_action",
                name="Acción por Defecto",
                description="Mantener estado actual del sistema",
                expected_outcome={"stability": 0.8, "efficiency": 0.6},
                resource_cost={"energy": 0.1},
                risk_level=0.1,
                confidence=0.7,
                implementation_time=0.0
            ),
            DecisionOption(
                id="optimization_action",
                name="Optimización General",
                description="Aplicar optimizaciones básicas",
                expected_outcome={"stability": 0.7, "efficiency": 0.8},
                resource_cost={"cpu": 0.2, "energy": 0.15},
                risk_level=0.3,
                confidence=0.75,
                implementation_time=120.0
            )
        ]
    
    async def _evaluate_options(self, options: List[DecisionOption], context: DecisionContext) -> List[DecisionOption]:
        """Evaluar y puntuar opciones de decisión"""
        evaluated_options = []
        
        for option in options:
            score = await self._calculate_option_score(option, context)
            
            # Actualizar confianza basada en el puntaje
            option.confidence = min(1.0, option.confidence * (score / 100.0))
            
            evaluated_options.append(option)
        
        # Ordenar por puntaje (confianza ajustada)
        evaluated_options.sort(key=lambda x: x.confidence, reverse=True)
        
        return evaluated_options
    
    async def _calculate_option_score(self, option: DecisionOption, context: DecisionContext) -> float:
        """Calcular puntaje para una opción"""
        score = 0.0
        
        # Factor de eficiencia esperada
        outcome_avg = sum(option.expected_outcome.values()) / len(option.expected_outcome)
        score += outcome_avg * 40.0
        
        # Factor de costo de recursos
        resource_cost_avg = sum(option.resource_cost.values()) / len(option.resource_cost)
        score += (1.0 - resource_cost_avg) * 30.0  # Menor costo = mayor puntaje
        
        # Factor de riesgo
        score += (1.0 - option.risk_level) * 20.0
        
        # Factor de tiempo de implementación vs urgencia
        if context.time_limit:
            time_factor = min(1.0, context.time_limit / option.implementation_time)
            score += time_factor * 10.0
        else:
            score += 10.0  # Sin límite de tiempo
        
        return min(100.0, score)
    
    async def _select_best_option(self, options: List[DecisionOption], context: DecisionContext) -> DecisionOption:
        """Seleccionar la mejor opción"""
        if not options:
            raise ValueError("No hay opciones disponibles para la decisión")
        
        # Aplicar filtros adicionales basados en contexto
        filtered_options = []
        
        for option in options:
            # Verificar restricciones de recursos
            if self._check_resource_constraints(option, context):
                # Verificar restricciones de tiempo
                if self._check_time_constraints(option, context):
                    filtered_options.append(option)
        
        if not filtered_options:
            # Si no hay opciones que cumplan las restricciones, usar la menos restrictiva
            logger.warning("Ninguna opción cumple todas las restricciones, seleccionando la mejor disponible")
            return options[0]
        
        return filtered_options[0]  # Ya están ordenadas por puntaje
    
    def _check_resource_constraints(self, option: DecisionOption, context: DecisionContext) -> bool:
        """Verificar si la opción cumple las restricciones de recursos"""
        available = context.available_resources
        required = option.resource_cost
        
        for resource, cost in required.items():
            if resource in available and available[resource] < cost:
                return False
        
        return True
    
    def _check_time_constraints(self, option: DecisionOption, context: DecisionContext) -> bool:
        """Verificar si la opción cumple las restricciones de tiempo"""
        if context.time_limit is None:
            return True
        
        return option.implementation_time <= context.time_limit
    
    async def _create_implementation_plan(self, option: DecisionOption, context: DecisionContext) -> List[Dict[str, Any]]:
        """Crear plan de implementación para la opción seleccionada"""
        plan = []
        
        # Paso 1: Preparación
        plan.append({
            "step": 1,
            "name": "Preparación",
            "description": f"Preparar recursos para {option.name}",
            "duration": option.implementation_time * 0.2,
            "resources_needed": {k: v * 0.3 for k, v in option.resource_cost.items()},
            "checkpoints": ["Verificar recursos", "Validar prerrequisitos"]
        })
        
        # Paso 2: Implementación
        plan.append({
            "step": 2,
            "name": "Implementación",
            "description": f"Ejecutar {option.name}",
            "duration": option.implementation_time * 0.6,
            "resources_needed": option.resource_cost,
            "checkpoints": ["Monitorear progreso", "Verificar métricas"]
        })
        
        # Paso 3: Verificación
        plan.append({
            "step": 3,
            "name": "Verificación",
            "description": "Verificar resultados y estabilizar",
            "duration": option.implementation_time * 0.2,
            "resources_needed": {k: v * 0.1 for k, v in option.resource_cost.items()},
            "checkpoints": ["Verificar objetivos", "Documentar resultados"]
        })
        
        return plan
    
    async def _generate_reasoning(self, selected_option: DecisionOption, all_options: List[DecisionOption], context: DecisionContext) -> str:
        """Generar explicación del razonamiento de la decisión"""
        reasoning = f"Seleccionada opción '{selected_option.name}' basado en los siguientes factores:\n"
        
        reasoning += f"- Confianza: {selected_option.confidence:.2f} (más alta entre las opciones)\n"
        reasoning += f"- Nivel de riesgo: {selected_option.risk_level:.2f} (aceptable para el contexto)\n"
        reasoning += f"- Tiempo de implementación: {selected_option.implementation_time:.0f}s"
        
        if context.time_limit:
            reasoning += f" (dentro del límite de {context.time_limit:.0f}s)\n"
        else:
            reasoning += "\n"
        
        # Mencionar por qué se descartaron otras opciones
        if len(all_options) > 1:
            reasoning += "\nOpciones alternativas consideradas:\n"
            for i, option in enumerate(all_options[1:3], 1):  # Top 2 alternativas
                reasoning += f"{i}. {option.name} - Confianza: {option.confidence:.2f}, Riesgo: {option.risk_level:.2f}\n"
        
        return reasoning
    
    def _get_monitoring_metrics(self, option: DecisionOption, context: DecisionContext) -> List[str]:
        """Obtener métricas de monitoreo para la decisión"""
        base_metrics = ["execution_time", "resource_usage", "success_rate"]
        
        # Añadir métricas específicas basadas en los resultados esperados
        for outcome_key in option.expected_outcome.keys():
            base_metrics.append(f"{outcome_key}_achievement")
        
        # Añadir métricas específicas del contexto
        if context.situation_type == "emergency_response":
            base_metrics.extend(["response_time", "containment_effectiveness"])
        elif context.situation_type == "resource_optimization":
            base_metrics.extend(["efficiency_improvement", "cost_savings"])
        
        return base_metrics
    
    def _save_decision(self, context: DecisionContext, result: DecisionResult):
        """Guardar decisión en el historial"""
        decision_record = {
            "timestamp": datetime.now().isoformat(),
            "context": asdict(context),
            "result": asdict(result),
            "system_state": self.system_context.copy()
        }
        
        self.decision_history.append(decision_record)
        
        # Mantener solo las últimas 1000 decisiones
        if len(self.decision_history) > 1000:
            self.decision_history = self.decision_history[-1000:]
    
    async def get_decision_analytics(self) -> Dict[str, Any]:
        """Obtener analíticas de decisiones"""
        if not self.decision_history:
            return {"status": "no_data"}
        
        recent_decisions = self.decision_history[-50:]  # Últimas 50 decisiones
        
        # Calcular métricas
        avg_confidence = sum(d["result"]["confidence_score"] for d in recent_decisions) / len(recent_decisions)
        
        decision_types = {}
        for decision in recent_decisions:
            situation_type = decision["context"]["situation_type"]
            decision_types[situation_type] = decision_types.get(situation_type, 0) + 1
        
        # Análisis de éxito (simulado)
        success_rate = 0.85  # Valor simulado
        
        return {
            "total_decisions": len(self.decision_history),
            "recent_decisions": len(recent_decisions),
            "average_confidence": avg_confidence,
            "success_rate": success_rate,
            "decision_types": decision_types,
            "most_common_situation": max(decision_types.items(), key=lambda x: x[1])[0] if decision_types else None,
            "performance_trend": "improving" if avg_confidence > 0.7 else "stable"
        }