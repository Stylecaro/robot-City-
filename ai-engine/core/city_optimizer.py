"""
Optimizador de Ciudad - Sistema de optimización inteligente
Optimiza recursos, tráfico, energía y eficiencia general de la ciudad virtual
"""

import asyncio
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger("city_optimizer")

@dataclass
class CityMetrics:
    """Métricas de la ciudad"""
    energy_efficiency: float
    traffic_flow: float
    resource_utilization: float
    citizen_satisfaction: float
    security_level: float
    environmental_health: float
    economic_performance: float
    infrastructure_health: float

@dataclass
class OptimizationResult:
    """Resultado de optimización"""
    improvement_percentage: float
    affected_systems: List[str]
    estimated_savings: Dict[str, float]
    implementation_time: float
    risk_level: str

class CityOptimizer:
    """Optimizador principal de la ciudad"""
    
    def __init__(self):
        self.current_metrics = CityMetrics(
            energy_efficiency=0.75,
            traffic_flow=0.68,
            resource_utilization=0.72,
            citizen_satisfaction=0.85,
            security_level=0.92,
            environmental_health=0.78,
            economic_performance=0.80,
            infrastructure_health=0.88
        )
        
        self.optimization_history = []
        self.active_optimizations = []
        self.monitoring_active = False
        
        logger.info("City Optimizer inicializado")
    
    async def start_monitoring(self):
        """Iniciar monitoreo continuo"""
        self.monitoring_active = True
        while self.monitoring_active:
            await asyncio.sleep(10)  # Monitorear cada 10 segundos
            await self.monitor_city_systems()
    
    async def monitor_city_systems(self):
        """Monitorear sistemas de la ciudad"""
        try:
            # Simular cambios naturales en las métricas
            await self.update_metrics()
            
            # Verificar si se necesita optimización automática
            if await self.needs_optimization():
                await self.auto_optimize()
                
        except Exception as e:
            logger.error(f"Error en monitoreo de ciudad: {e}")
    
    async def update_metrics(self):
        """Actualizar métricas de la ciudad"""
        # Simular fluctuaciones naturales
        fluctuation = 0.02  # ±2%
        
        self.current_metrics.energy_efficiency += np.random.uniform(-fluctuation, fluctuation)
        self.current_metrics.traffic_flow += np.random.uniform(-fluctuation, fluctuation)
        self.current_metrics.resource_utilization += np.random.uniform(-fluctuation, fluctuation)
        self.current_metrics.citizen_satisfaction += np.random.uniform(-fluctuation/2, fluctuation/2)
        self.current_metrics.security_level += np.random.uniform(-fluctuation/3, fluctuation/3)
        self.current_metrics.environmental_health += np.random.uniform(-fluctuation, fluctuation)
        self.current_metrics.economic_performance += np.random.uniform(-fluctuation, fluctuation)
        self.current_metrics.infrastructure_health += np.random.uniform(-fluctuation/2, fluctuation/2)
        
        # Mantener valores en rango válido
        self._clamp_metrics()
    
    def _clamp_metrics(self):
        """Mantener métricas en rango válido [0.0, 1.0]"""
        self.current_metrics.energy_efficiency = max(0.0, min(1.0, self.current_metrics.energy_efficiency))
        self.current_metrics.traffic_flow = max(0.0, min(1.0, self.current_metrics.traffic_flow))
        self.current_metrics.resource_utilization = max(0.0, min(1.0, self.current_metrics.resource_utilization))
        self.current_metrics.citizen_satisfaction = max(0.0, min(1.0, self.current_metrics.citizen_satisfaction))
        self.current_metrics.security_level = max(0.0, min(1.0, self.current_metrics.security_level))
        self.current_metrics.environmental_health = max(0.0, min(1.0, self.current_metrics.environmental_health))
        self.current_metrics.economic_performance = max(0.0, min(1.0, self.current_metrics.economic_performance))
        self.current_metrics.infrastructure_health = max(0.0, min(1.0, self.current_metrics.infrastructure_health))
    
    async def needs_optimization(self) -> bool:
        """Verificar si la ciudad necesita optimización"""
        thresholds = {
            'energy_efficiency': 0.6,
            'traffic_flow': 0.5,
            'resource_utilization': 0.6,
            'citizen_satisfaction': 0.7,
            'security_level': 0.8,
            'environmental_health': 0.6,
            'economic_performance': 0.6,
            'infrastructure_health': 0.7
        }
        
        metrics_dict = asdict(self.current_metrics)
        
        for metric, value in metrics_dict.items():
            if value < thresholds.get(metric, 0.7):
                logger.info(f"Optimización necesaria: {metric} = {value:.2f}")
                return True
        
        return False
    
    async def auto_optimize(self):
        """Ejecutar optimización automática"""
        logger.info("Iniciando optimización automática de la ciudad")
        
        optimization_plan = await self.generate_optimization_plan()
        result = await self.execute_optimization(optimization_plan)
        
        self.optimization_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "automatic",
            "plan": optimization_plan,
            "result": asdict(result)
        })
    
    async def optimize(self) -> OptimizationResult:
        """Ejecutar optimización manual completa"""
        logger.info("Iniciando optimización manual de la ciudad")
        
        optimization_plan = await self.generate_comprehensive_optimization_plan()
        result = await self.execute_optimization(optimization_plan)
        
        self.optimization_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "manual",
            "plan": optimization_plan,
            "result": asdict(result)
        })
        
        return result
    
    async def generate_optimization_plan(self) -> Dict[str, Any]:
        """Generar plan de optimización básico"""
        metrics_dict = asdict(self.current_metrics)
        
        # Identificar métricas que necesitan mejora
        improvements_needed = []
        for metric, value in metrics_dict.items():
            if value < 0.7:
                improvements_needed.append({
                    "metric": metric,
                    "current_value": value,
                    "target_improvement": min(0.15, 0.9 - value),
                    "priority": self._calculate_priority(metric, value)
                })
        
        # Ordenar por prioridad
        improvements_needed.sort(key=lambda x: x["priority"], reverse=True)
        
        return {
            "improvements": improvements_needed[:3],  # Top 3 prioridades
            "estimated_duration": len(improvements_needed) * 2.0,  # minutos
            "resource_requirements": self._calculate_resource_requirements(improvements_needed)
        }
    
    async def generate_comprehensive_optimization_plan(self) -> Dict[str, Any]:
        """Generar plan de optimización comprensivo"""
        metrics_dict = asdict(self.current_metrics)
        
        # Analizar todas las métricas
        all_improvements = []
        for metric, value in metrics_dict.items():
            potential_improvement = min(0.2, 1.0 - value)
            if potential_improvement > 0.05:  # Solo si hay mejora significativa posible
                all_improvements.append({
                    "metric": metric,
                    "current_value": value,
                    "target_improvement": potential_improvement,
                    "priority": self._calculate_priority(metric, value)
                })
        
        # Estrategias de optimización
        strategies = await self._generate_optimization_strategies(all_improvements)
        
        return {
            "improvements": all_improvements,
            "strategies": strategies,
            "estimated_duration": len(all_improvements) * 1.5,
            "resource_requirements": self._calculate_resource_requirements(all_improvements),
            "expected_roi": self._calculate_expected_roi(all_improvements)
        }
    
    def _calculate_priority(self, metric: str, current_value: float) -> float:
        """Calcular prioridad de optimización para una métrica"""
        # Pesos de importancia por métrica
        importance_weights = {
            'citizen_satisfaction': 1.0,
            'security_level': 0.95,
            'infrastructure_health': 0.9,
            'energy_efficiency': 0.85,
            'environmental_health': 0.8,
            'economic_performance': 0.8,
            'traffic_flow': 0.75,
            'resource_utilization': 0.7
        }
        
        weight = importance_weights.get(metric, 0.5)
        urgency = 1.0 - current_value  # Más urgente si el valor es más bajo
        
        return weight * urgency
    
    def _calculate_resource_requirements(self, improvements: List[Dict]) -> Dict[str, float]:
        """Calcular requerimientos de recursos"""
        total_improvement = sum(imp["target_improvement"] for imp in improvements)
        
        return {
            "cpu_usage": min(0.8, total_improvement * 0.3),
            "memory_usage": min(0.6, total_improvement * 0.2),
            "network_bandwidth": min(0.5, total_improvement * 0.15),
            "energy_cost": total_improvement * 100.0,  # kWh
            "estimated_budget": total_improvement * 10000.0  # Unidades monetarias
        }
    
    def _calculate_expected_roi(self, improvements: List[Dict]) -> Dict[str, float]:
        """Calcular retorno de inversión esperado"""
        total_improvement = sum(imp["target_improvement"] for imp in improvements)
        
        return {
            "efficiency_gain": total_improvement * 0.8,
            "cost_savings": total_improvement * 5000.0,
            "citizen_satisfaction_boost": total_improvement * 0.6,
            "payback_period_days": max(30.0, 90.0 / max(total_improvement, 0.1))
        }
    
    async def _generate_optimization_strategies(self, improvements: List[Dict]) -> List[Dict]:
        """Generar estrategias específicas de optimización"""
        strategies = []
        
        for improvement in improvements:
            metric = improvement["metric"]
            strategy = await self._get_optimization_strategy(metric, improvement)
            strategies.append(strategy)
        
        return strategies
    
    async def _get_optimization_strategy(self, metric: str, improvement: Dict) -> Dict:
        """Obtener estrategia específica para una métrica"""
        strategies_map = {
            'energy_efficiency': {
                "name": "Optimización Energética",
                "actions": [
                    "Implementar algoritmos de gestión inteligente de energía",
                    "Optimizar rutas de robots para reducir consumo",
                    "Activar modo de ahorro energético en sistemas no críticos"
                ],
                "expected_time": 3.0,
                "complexity": "medium"
            },
            'traffic_flow': {
                "name": "Optimización de Tráfico",
                "actions": [
                    "Reconfigurar rutas de transporte",
                    "Implementar semáforos inteligentes",
                    "Coordinar movimiento de robots de transporte"
                ],
                "expected_time": 4.0,
                "complexity": "high"
            },
            'resource_utilization': {
                "name": "Optimización de Recursos",
                "actions": [
                    "Balancear carga de trabajo entre robots",
                    "Optimizar asignación de tareas",
                    "Implementar compartición de recursos"
                ],
                "expected_time": 2.5,
                "complexity": "medium"
            },
            'citizen_satisfaction': {
                "name": "Mejora de Servicios Ciudadanos",
                "actions": [
                    "Mejorar tiempos de respuesta de servicios",
                    "Optimizar interfaces de usuario",
                    "Implementar servicios personalizados"
                ],
                "expected_time": 5.0,
                "complexity": "high"
            },
            'security_level': {
                "name": "Fortalecimiento de Seguridad",
                "actions": [
                    "Actualizar protocolos de seguridad",
                    "Mejorar monitoreo de amenazas",
                    "Implementar respuesta automática a incidentes"
                ],
                "expected_time": 3.5,
                "complexity": "high"
            }
        }
        
        default_strategy = {
            "name": f"Optimización de {metric.replace('_', ' ').title()}",
            "actions": ["Aplicar algoritmos de optimización generales"],
            "expected_time": 2.0,
            "complexity": "low"
        }
        
        return strategies_map.get(metric, default_strategy)
    
    async def execute_optimization(self, plan: Dict[str, Any]) -> OptimizationResult:
        """Ejecutar plan de optimización"""
        improvements = plan.get("improvements", [])
        
        total_improvement = 0.0
        affected_systems = []
        
        for improvement in improvements:
            metric = improvement["metric"]
            target_improvement = improvement["target_improvement"]
            
            # Aplicar mejora a la métrica
            current_value = getattr(self.current_metrics, metric)
            new_value = min(1.0, current_value + target_improvement * 0.8)  # 80% de eficiencia
            setattr(self.current_metrics, metric, new_value)
            
            total_improvement += target_improvement
            affected_systems.append(metric)
        
        # Calcular ahorros estimados
        estimated_savings = {
            "energy": total_improvement * 1000.0,  # kWh
            "time": total_improvement * 50.0,  # horas
            "cost": total_improvement * 2500.0  # unidades monetarias
        }
        
        # Determinar nivel de riesgo
        risk_level = "low"
        if total_improvement > 0.3:
            risk_level = "high"
        elif total_improvement > 0.15:
            risk_level = "medium"
        
        result = OptimizationResult(
            improvement_percentage=total_improvement * 100,
            affected_systems=affected_systems,
            estimated_savings=estimated_savings,
            implementation_time=plan.get("estimated_duration", 5.0),
            risk_level=risk_level
        )
        
        logger.info(f"Optimización completada: {result.improvement_percentage:.1f}% de mejora")
        
        return result
    
    async def get_optimization_data(self) -> Dict[str, Any]:
        """Obtener datos de optimización actuales"""
        return {
            "current_metrics": asdict(self.current_metrics),
            "optimization_history": self.optimization_history[-10:],  # Últimas 10
            "active_optimizations": self.active_optimizations,
            "system_health": await self._calculate_overall_health(),
            "optimization_opportunities": await self._identify_opportunities(),
            "performance_trends": await self._analyze_trends()
        }
    
    async def _calculate_overall_health(self) -> float:
        """Calcular salud general del sistema"""
        metrics_dict = asdict(self.current_metrics)
        weights = {
            'citizen_satisfaction': 0.2,
            'security_level': 0.15,
            'infrastructure_health': 0.15,
            'energy_efficiency': 0.15,
            'environmental_health': 0.1,
            'economic_performance': 0.1,
            'traffic_flow': 0.08,
            'resource_utilization': 0.07
        }
        
        weighted_sum = sum(
            metrics_dict[metric] * weight 
            for metric, weight in weights.items()
        )
        
        return weighted_sum
    
    async def _identify_opportunities(self) -> List[Dict]:
        """Identificar oportunidades de optimización"""
        metrics_dict = asdict(self.current_metrics)
        opportunities = []
        
        for metric, value in metrics_dict.items():
            if value < 0.8:  # Hay margen de mejora
                potential = 0.95 - value  # Objetivo de 95%
                opportunities.append({
                    "metric": metric,
                    "current": value,
                    "potential_improvement": potential,
                    "impact": self._calculate_impact(metric, potential),
                    "difficulty": self._calculate_difficulty(metric)
                })
        
        # Ordenar por impacto vs dificultad
        opportunities.sort(key=lambda x: x["impact"] / x["difficulty"], reverse=True)
        
        return opportunities[:5]  # Top 5 oportunidades
    
    def _calculate_impact(self, metric: str, improvement: float) -> float:
        """Calcular impacto de mejorar una métrica"""
        impact_multipliers = {
            'citizen_satisfaction': 3.0,
            'security_level': 2.5,
            'infrastructure_health': 2.0,
            'energy_efficiency': 2.0,
            'environmental_health': 1.8,
            'economic_performance': 1.8,
            'traffic_flow': 1.5,
            'resource_utilization': 1.3
        }
        
        multiplier = impact_multipliers.get(metric, 1.0)
        return improvement * multiplier
    
    def _calculate_difficulty(self, metric: str) -> float:
        """Calcular dificultad de mejorar una métrica"""
        difficulty_scores = {
            'energy_efficiency': 2.0,
            'resource_utilization': 2.0,
            'traffic_flow': 3.0,
            'citizen_satisfaction': 4.0,
            'environmental_health': 2.5,
            'economic_performance': 3.5,
            'security_level': 4.0,
            'infrastructure_health': 3.0
        }
        
        return difficulty_scores.get(metric, 2.5)
    
    async def _analyze_trends(self) -> Dict[str, Any]:
        """Analizar tendencias de rendimiento"""
        # Simular datos de tendencias basados en historial
        if len(self.optimization_history) < 2:
            return {"status": "insufficient_data"}
        
        recent_optimizations = self.optimization_history[-5:]
        
        # Calcular tendencia de mejora
        improvements = [opt["result"]["improvement_percentage"] for opt in recent_optimizations]
        avg_improvement = sum(improvements) / len(improvements)
        
        # Analizar frecuencia de optimizaciones
        timestamps = [datetime.fromisoformat(opt["timestamp"]) for opt in recent_optimizations]
        if len(timestamps) > 1:
            intervals = [(timestamps[i] - timestamps[i-1]).total_seconds() / 3600 
                        for i in range(1, len(timestamps))]  # en horas
            avg_interval = sum(intervals) / len(intervals)
        else:
            avg_interval = 24.0  # default
        
        return {
            "average_improvement": avg_improvement,
            "optimization_frequency_hours": avg_interval,
            "trend": "improving" if avg_improvement > 5.0 else "stable",
            "efficiency_trend": "up" if avg_improvement > 0 else "down",
            "last_optimization": recent_optimizations[-1]["timestamp"] if recent_optimizations else None
        }