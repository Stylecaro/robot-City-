"""
Predictive Analytics Engine - Motor de Análisis Predictivo con ML
Predice tráfico, recursos, mantenimiento y optimiza operaciones
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging

try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("scikit-learn no disponible - predicciones limitadas")


@dataclass
class Prediction:
    """Predicción con intervalo de confianza"""
    timestamp: str
    value: float
    confidence: float
    lower_bound: float
    upper_bound: float
    feature_importance: Dict[str, float]


@dataclass
class Alert:
    """Alerta predictiva"""
    alert_id: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    category: str  # 'traffic', 'energy', 'maintenance', 'security'
    message: str
    predicted_time: str
    recommended_action: str
    confidence: float


class TrafficPredictor:
    """Predictor de congestión de tráfico"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, max_depth=10) if SKLEARN_AVAILABLE else None
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        self.is_trained = False
        self.feature_names = [
            'hour', 'day_of_week', 'active_robots', 'total_robots',
            'manufacturing_efficiency', 'avg_speed', 'battery_avg'
        ]
    
    def train(self, historical_data: pd.DataFrame):
        """Entrena el modelo con datos históricos"""
        if not SKLEARN_AVAILABLE or historical_data.empty:
            return
        
        try:
            # Preparar features
            X = historical_data[self.feature_names].values
            y = historical_data['traffic_density'].values
            
            # Normalizar
            X_scaled = self.scaler.fit_transform(X)
            
            # Entrenar
            self.model.fit(X_scaled, y)
            self.is_trained = True
            
            logging.info(f"✅ TrafficPredictor entrenado con {len(historical_data)} registros")
        except Exception as e:
            logging.error(f"Error entrenando TrafficPredictor: {e}")
    
    def predict(self, features: Dict[str, float]) -> Prediction:
        """Predice densidad de tráfico"""
        if not self.is_trained or not SKLEARN_AVAILABLE:
            # Predicción simple basada en reglas
            return self._rule_based_prediction(features)
        
        try:
            # Preparar features
            X = np.array([[
                features.get('hour', datetime.now().hour),
                features.get('day_of_week', datetime.now().weekday()),
                features.get('active_robots', 0),
                features.get('total_robots', 1),
                features.get('manufacturing_efficiency', 0.5),
                features.get('avg_speed', 5.0),
                features.get('battery_avg', 0.8)
            ]])
            
            X_scaled = self.scaler.transform(X)
            
            # Predicción
            prediction = self.model.predict(X_scaled)[0]
            
            # Calcular confianza (basado en varianza de árboles)
            tree_predictions = [tree.predict(X_scaled)[0] for tree in self.model.estimators_]
            std = np.std(tree_predictions)
            confidence = 1.0 / (1.0 + std)
            
            # Feature importance
            importance = dict(zip(self.feature_names, self.model.feature_importances_))
            
            return Prediction(
                timestamp=datetime.now().isoformat(),
                value=float(prediction),
                confidence=float(confidence),
                lower_bound=float(prediction - 2 * std),
                upper_bound=float(prediction + 2 * std),
                feature_importance=importance
            )
        except Exception as e:
            logging.error(f"Error en predicción: {e}")
            return self._rule_based_prediction(features)
    
    def _rule_based_prediction(self, features: Dict[str, float]) -> Prediction:
        """Predicción basada en reglas cuando no hay ML"""
        active = features.get('active_robots', 0)
        total = features.get('total_robots', 1)
        hour = features.get('hour', datetime.now().hour)
        
        # Calcular densidad base
        base_density = active / max(total, 1)
        
        # Ajustar por hora (pico en horas laborales)
        if 8 <= hour <= 17:
            base_density *= 1.3
        
        # Añadir ruido
        prediction = max(0, min(1, base_density + np.random.normal(0, 0.05)))
        
        return Prediction(
            timestamp=datetime.now().isoformat(),
            value=prediction,
            confidence=0.6,
            lower_bound=max(0, prediction - 0.1),
            upper_bound=min(1, prediction + 0.1),
            feature_importance={'active_robots': 0.5, 'hour': 0.3, 'total_robots': 0.2}
        )


class ResourcePredictor:
    """Predictor de consumo de recursos"""
    
    def __init__(self):
        self.energy_model = GradientBoostingRegressor(n_estimators=100) if SKLEARN_AVAILABLE else None
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        self.is_trained = False
    
    def predict_energy(self, features: Dict[str, float]) -> Prediction:
        """Predice consumo energético futuro"""
        active = features.get('active_robots', 0)
        total = features.get('total_robots', 1)
        current_consumption = features.get('current_consumption', 0.5)
        
        # Proyección simple
        if total > 0:
            predicted_consumption = (active / total) * 0.8 + current_consumption * 0.2
        else:
            predicted_consumption = current_consumption
        
        return Prediction(
            timestamp=(datetime.now() + timedelta(hours=1)).isoformat(),
            value=predicted_consumption,
            confidence=0.75,
            lower_bound=predicted_consumption * 0.9,
            upper_bound=predicted_consumption * 1.1,
            feature_importance={'active_robots': 0.6, 'current_consumption': 0.4}
        )
    
    def predict_battery_depletion(self, robot_data: Dict[str, Any]) -> Tuple[float, str]:
        """Predice cuándo se agotará la batería de un robot"""
        battery = robot_data.get('battery_level', 1.0)
        state = robot_data.get('state', 'idle')
        
        # Tasa de consumo por estado
        consumption_rates = {
            'idle': 0.001,
            'patrol': 0.005,
            'working': 0.01,
            'charging': -0.05,
            'emergency': 0.02
        }
        
        rate = consumption_rates.get(state, 0.005)
        
        if rate <= 0:
            return float('inf'), "Cargando"
        
        # Calcular tiempo hasta agotamiento (en minutos)
        time_remaining = (battery / rate) / 60.0
        
        # Formatear mensaje
        if time_remaining < 5:
            message = f"⚠️ CRÍTICO: {time_remaining:.1f} minutos restantes"
        elif time_remaining < 15:
            message = f"⚡ BAJO: {time_remaining:.1f} minutos restantes"
        else:
            message = f"✅ OK: {time_remaining:.0f} minutos restantes"
        
        return time_remaining, message


class MaintenancePredictor:
    """Predictor de necesidades de mantenimiento"""
    
    def __init__(self):
        self.failure_threshold = 0.3
        self.warning_threshold = 0.5
    
    def predict_maintenance_needed(self, robot_data: Dict[str, Any]) -> Optional[Alert]:
        """Predice si un robot necesitará mantenimiento pronto"""
        health = robot_data.get('health', 1.0)
        battery = robot_data.get('battery_level', 1.0)
        tasks_completed = robot_data.get('tasks_completed', 0)
        robot_id = robot_data.get('robot_id', 'unknown')
        
        # Calcular score de riesgo
        risk_score = 0.0
        
        if health < self.failure_threshold:
            risk_score += 0.5
        elif health < self.warning_threshold:
            risk_score += 0.3
        
        if battery < 0.2:
            risk_score += 0.3
        
        # Desgaste por uso
        wear_factor = min(tasks_completed / 1000.0, 0.2)
        risk_score += wear_factor
        
        risk_score = min(risk_score, 1.0)
        
        # Generar alerta si es necesario
        if risk_score > 0.6:
            severity = 'critical' if risk_score > 0.8 else 'high'
            
            # Predicción de tiempo hasta fallo
            time_to_failure = (health / 0.001) / 60.0  # minutos
            
            return Alert(
                alert_id=f"maint_{robot_id}_{int(datetime.now().timestamp())}",
                severity=severity,
                category='maintenance',
                message=f"Robot {robot_id} requiere mantenimiento (salud: {health:.1%})",
                predicted_time=(datetime.now() + timedelta(minutes=time_to_failure)).isoformat(),
                recommended_action=f"Programar mantenimiento preventivo en {time_to_failure:.0f} minutos",
                confidence=0.8
            )
        
        return None


class PredictiveAnalytics:
    """Motor central de análisis predictivo"""
    
    def __init__(self):
        self.traffic_predictor = TrafficPredictor()
        self.resource_predictor = ResourcePredictor()
        self.maintenance_predictor = MaintenancePredictor()
        
        self.alerts: List[Alert] = []
        self.predictions_history: List[Dict] = []
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def analyze_city(self, city_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis completo de la ciudad"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'traffic_prediction': None,
            'energy_prediction': None,
            'maintenance_alerts': [],
            'recommendations': []
        }
        
        try:
            # Predicción de tráfico
            traffic_features = {
                'hour': datetime.now().hour,
                'day_of_week': datetime.now().weekday(),
                'active_robots': city_data.get('active_robots', 0),
                'total_robots': city_data.get('total_robots', 0),
                'manufacturing_efficiency': city_data.get('manufacturing_efficiency', 0.5),
                'avg_speed': 5.0,
                'battery_avg': 0.8
            }
            
            traffic_pred = self.traffic_predictor.predict(traffic_features)
            results['traffic_prediction'] = asdict(traffic_pred)
            
            # Predicción de energía
            energy_features = {
                'active_robots': city_data.get('active_robots', 0),
                'total_robots': city_data.get('total_robots', 1),
                'current_consumption': city_data.get('energy_consumption', 0.5)
            }
            
            energy_pred = self.resource_predictor.predict_energy(energy_features)
            results['energy_prediction'] = asdict(energy_pred)
            
            # Análisis de mantenimiento por robot
            robots = city_data.get('robots', [])
            for robot_data in robots:
                alert = self.maintenance_predictor.predict_maintenance_needed(robot_data)
                if alert:
                    results['maintenance_alerts'].append(asdict(alert))
                    self.alerts.append(alert)
            
            # Generar recomendaciones
            results['recommendations'] = self._generate_recommendations(results)
            
            # Guardar en historial
            self.predictions_history.append(results)
            if len(self.predictions_history) > 1000:
                self.predictions_history = self.predictions_history[-1000:]
            
            self.logger.info(f"📊 Análisis completado - {len(results['maintenance_alerts'])} alertas")
            
        except Exception as e:
            self.logger.error(f"Error en análisis: {e}")
        
        return results
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Genera recomendaciones basadas en predicciones"""
        recommendations = []
        
        # Tráfico
        if analysis.get('traffic_prediction'):
            traffic_value = analysis['traffic_prediction']['value']
            if traffic_value > 0.8:
                recommendations.append(
                    "🚦 Tráfico alto previsto - Considere redistribuir robots o crear rutas alternativas"
                )
            elif traffic_value > 0.6:
                recommendations.append(
                    "⚠️ Tráfico moderado - Monitoree congestión en zonas clave"
                )
        
        # Energía
        if analysis.get('energy_prediction'):
            energy_value = analysis['energy_prediction']['value']
            if energy_value > 0.8:
                recommendations.append(
                    "⚡ Consumo energético alto - Active modo ahorro de energía y envíe robots a carga"
                )
            elif energy_value > 0.6:
                recommendations.append(
                    "🔋 Consumo elevado - Optimice distribución de tareas para reducir consumo"
                )
        
        # Mantenimiento
        critical_alerts = len([a for a in analysis.get('maintenance_alerts', []) 
                              if a['severity'] == 'critical'])
        if critical_alerts > 0:
            recommendations.append(
                f"🔧 {critical_alerts} robots requieren mantenimiento URGENTE - Programe inmediatamente"
            )
        
        high_alerts = len([a for a in analysis.get('maintenance_alerts', []) 
                          if a['severity'] == 'high'])
        if high_alerts > 0:
            recommendations.append(
                f"⚠️ {high_alerts} robots necesitan mantenimiento preventivo en 24h"
            )
        
        if not recommendations:
            recommendations.append("✅ Todos los sistemas operando dentro de parámetros normales")
        
        return recommendations
    
    def train_models(self, historical_data: pd.DataFrame):
        """Entrena todos los modelos con datos históricos"""
        if not SKLEARN_AVAILABLE:
            self.logger.warning("scikit-learn no disponible - entrenamiento omitido")
            return
        
        try:
            self.traffic_predictor.train(historical_data)
            self.logger.info("✅ Modelos entrenados exitosamente")
        except Exception as e:
            self.logger.error(f"Error entrenando modelos: {e}")
    
    def get_active_alerts(self, severity: Optional[str] = None) -> List[Alert]:
        """Obtiene alertas activas"""
        if severity:
            return [a for a in self.alerts if a.severity == severity]
        return self.alerts.copy()
    
    def clear_old_alerts(self, hours: int = 24):
        """Limpia alertas antiguas"""
        cutoff = datetime.now() - timedelta(hours=hours)
        self.alerts = [
            a for a in self.alerts 
            if datetime.fromisoformat(a.predicted_time) > cutoff
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del motor"""
        return {
            'models_trained': self.traffic_predictor.is_trained,
            'total_predictions': len(self.predictions_history),
            'active_alerts': len(self.alerts),
            'alerts_by_severity': {
                'critical': len([a for a in self.alerts if a.severity == 'critical']),
                'high': len([a for a in self.alerts if a.severity == 'high']),
                'medium': len([a for a in self.alerts if a.severity == 'medium']),
                'low': len([a for a in self.alerts if a.severity == 'low'])
            }
        }


# Instancia global
analytics_engine = PredictiveAnalytics()


async def main():
    """Función de prueba"""
    import asyncio
    
    print("📊 Iniciando Predictive Analytics Engine...")
    
    # Datos de prueba
    city_data = {
        'total_robots': 50,
        'active_robots': 35,
        'manufacturing_efficiency': 0.85,
        'energy_consumption': 0.65,
        'robots': [
            {
                'robot_id': 'robot_001',
                'health': 0.4,
                'battery_level': 0.3,
                'tasks_completed': 150,
                'state': 'working'
            },
            {
                'robot_id': 'robot_002',
                'health': 0.9,
                'battery_level': 0.8,
                'tasks_completed': 50,
                'state': 'idle'
            }
        ]
    }
    
    # Analizar
    results = analytics_engine.analyze_city(city_data)
    
    print("\n📊 RESULTADOS DEL ANÁLISIS:")
    print(f"\nPredicción de Tráfico:")
    if results['traffic_prediction']:
        print(f"  Valor: {results['traffic_prediction']['value']:.2%}")
        print(f"  Confianza: {results['traffic_prediction']['confidence']:.2%}")
    
    print(f"\nPredicción de Energía:")
    if results['energy_prediction']:
        print(f"  Consumo previsto: {results['energy_prediction']['value']:.2%}")
    
    print(f"\nAlertas de Mantenimiento: {len(results['maintenance_alerts'])}")
    for alert in results['maintenance_alerts']:
        print(f"  🚨 {alert['severity'].upper()}: {alert['message']}")
    
    print(f"\nRecomendaciones:")
    for rec in results['recommendations']:
        print(f"  {rec}")
    
    print(f"\n✅ Análisis completado")
    print(f"Estadísticas: {analytics_engine.get_stats()}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
