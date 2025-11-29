"""
METAVERSO BACKEND API - PYTHON FLASK APPLICATION
Advanced backend server for Robot City Metaverse
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import datetime
import logging
import os
import random
import threading
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'metaverso_secret_2024'
CORS(app, origins=["*"])
socketio = SocketIO(app, cors_allowed_origins="*")

# Data models
@dataclass
class RobotStatus:
    id: str
    name: str
    type: str
    status: str
    location: Dict[str, float]
    efficiency: float
    last_update: str

@dataclass
class ManufacturingLine:
    id: str
    name: str
    status: str
    production_rate: float
    quality_score: float
    robots_assigned: List[str]
    current_product: str

@dataclass
class ResearchProject:
    id: str
    title: str
    status: str
    progress: float
    researchers: List[str]
    budget: float
    deadline: str

@dataclass
class SecurityAlert:
    id: str
    level: str
    message: str
    timestamp: str
    resolved: bool

@dataclass
class SystemMetrics:
    manufacturing_efficiency: float
    research_progress: float
    security_level: float
    ai_performance: float
    active_robots: int
    energy_consumption: float
    timestamp: str

# Global data storage
class MetaversoData:
    def __init__(self):
        self.robots: List[RobotStatus] = []
        self.manufacturing_lines: List[ManufacturingLine] = []
        self.research_projects: List[ResearchProject] = []
        self.security_alerts: List[SecurityAlert] = []
        self.system_metrics: SystemMetrics = None
        self.activity_log: List[Dict] = []
        
        # Initialize with sample data
        self.initialize_sample_data()
    
    def initialize_sample_data(self):
        """Initialize the system with sample data"""
        # Sample robots
        robot_types = ['Manufacturing', 'Research', 'Security', 'Maintenance']
        for i in range(20):
            robot = RobotStatus(
                id=f"ROBOT-{i+1:03d}",
                name=f"Robot XR-{i+1}",
                type=random.choice(robot_types),
                status=random.choice(['Active', 'Idle', 'Maintenance']),
                location={
                    'x': random.uniform(-50, 50),
                    'y': random.uniform(0, 10),
                    'z': random.uniform(-50, 50)
                },
                efficiency=random.uniform(0.8, 1.0),
                last_update=datetime.datetime.now().isoformat()
            )
            self.robots.append(robot)
        
        # Sample manufacturing lines
        for i in range(5):
            line = ManufacturingLine(
                id=f"LINE-{i+1:02d}",
                name=f"Línea de Producción {i+1}",
                status=random.choice(['Running', 'Idle', 'Maintenance']),
                production_rate=random.uniform(80, 100),
                quality_score=random.uniform(90, 100),
                robots_assigned=[f"ROBOT-{j:03d}" for j in range(i*4+1, (i+1)*4+1)],
                current_product=f"Componente-{chr(65+i)}"
            )
            self.manufacturing_lines.append(line)
        
        # Sample research projects
        research_topics = [
            "Inteligencia Artificial Avanzada",
            "Materiales Cuánticos",
            "Robótica Biomimética",
            "Energía de Fusión",
            "Nanotecnología Médica"
        ]
        for i, topic in enumerate(research_topics):
            project = ResearchProject(
                id=f"RESEARCH-{i+1:03d}",
                title=topic,
                status=random.choice(['Active', 'Planning', 'Review']),
                progress=random.uniform(0.2, 0.9),
                researchers=[f"Dr. Investigador {j}" for j in range(1, 4)],
                budget=random.uniform(100000, 1000000),
                deadline=(datetime.datetime.now() + datetime.timedelta(days=random.randint(30, 365))).isoformat()
            )
            self.research_projects.append(project)
        
        # Initialize system metrics
        self.update_system_metrics()
    
    def update_system_metrics(self):
        """Update system metrics based on current data"""
        active_robots = len([r for r in self.robots if r.status == 'Active'])
        avg_efficiency = sum(r.efficiency for r in self.robots) / len(self.robots) if self.robots else 0
        
        manufacturing_eff = sum(l.production_rate for l in self.manufacturing_lines) / len(self.manufacturing_lines) if self.manufacturing_lines else 0
        research_prog = sum(p.progress for p in self.research_projects) / len(self.research_projects) if self.research_projects else 0
        
        unresolved_alerts = len([a for a in self.security_alerts if not a.resolved])
        security_level = max(0, 100 - (unresolved_alerts * 10))
        
        self.system_metrics = SystemMetrics(
            manufacturing_efficiency=manufacturing_eff,
            research_progress=research_prog * 100,
            security_level=security_level,
            ai_performance=avg_efficiency * 100,
            active_robots=active_robots,
            energy_consumption=random.uniform(500, 800),
            timestamp=datetime.datetime.now().isoformat()
        )
    
    def add_activity(self, activity_type: str, message: str, severity: str = 'info'):
        """Add activity to the log"""
        activity = {
            'id': len(self.activity_log) + 1,
            'type': activity_type,
            'message': message,
            'severity': severity,
            'timestamp': datetime.datetime.now().isoformat()
        }
        self.activity_log.insert(0, activity)  # Add to beginning
        
        # Keep only last 100 activities
        if len(self.activity_log) > 100:
            self.activity_log = self.activity_log[:100]

# Global data instance
metaverso_data = MetaversoData()

# Background task for real-time updates
def background_updates():
    """Background thread for real-time data updates"""
    while True:
        try:
            # Update robot statuses
            for robot in metaverso_data.robots:
                if random.random() < 0.1:  # 10% chance to update
                    robot.efficiency = max(0.7, min(1.0, robot.efficiency + random.uniform(-0.05, 0.05)))
                    robot.last_update = datetime.datetime.now().isoformat()
            
            # Update manufacturing lines
            for line in metaverso_data.manufacturing_lines:
                if random.random() < 0.15:  # 15% chance to update
                    line.production_rate = max(60, min(100, line.production_rate + random.uniform(-5, 5)))
                    line.quality_score = max(80, min(100, line.quality_score + random.uniform(-2, 2)))
            
            # Update research projects
            for project in metaverso_data.research_projects:
                if random.random() < 0.05:  # 5% chance to update
                    project.progress = min(1.0, project.progress + random.uniform(0, 0.01))
            
            # Generate random activities
            if random.random() < 0.3:  # 30% chance per update cycle
                activities = [
                    ('manufacturing', 'Robot completó manufactura de componente'),
                    ('research', 'Experimento de materiales iniciado'),
                    ('security', 'Escaneo de seguridad completado'),
                    ('ai', 'IA procesó nuevos patrones de datos'),
                    ('system', 'Mantenimiento preventivo ejecutado')
                ]
                activity_type, message = random.choice(activities)
                metaverso_data.add_activity(activity_type, message)
            
            # Update system metrics
            metaverso_data.update_system_metrics()
            
            # Emit real-time updates via WebSocket
            socketio.emit('system_update', {
                'metrics': asdict(metaverso_data.system_metrics),
                'latest_activity': metaverso_data.activity_log[0] if metaverso_data.activity_log else None
            })
            
            time.sleep(5)  # Update every 5 seconds
            
        except Exception as e:
            logger.error(f"Error in background updates: {e}")
            time.sleep(10)

# Start background thread
update_thread = threading.Thread(target=background_updates, daemon=True)
update_thread.start()

# API Routes

@app.route('/test')
def test_simple():
    """Serve simple test page"""
    return render_template('test_simple.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return app.send_static_file('favicon.ico')

@app.route('/')
def index():
    """Serve the main application"""
    return render_template('metaverso_app.html')

@app.route('/ciudad3d')
def ciudad_3d():
    """Serve the 3D city viewer"""
    return render_template('ciudad_robot_3d.html')

@app.route('/advanced')
def advanced_app():
    """Serve the advanced metaverso application"""
    return render_template('advanced_metaverso.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '2.0.0'
    })

@app.route('/api/dashboard')
def get_dashboard_data():
    """Get dashboard overview data"""
    return jsonify({
        'metrics': asdict(metaverso_data.system_metrics),
        'summary': {
            'total_robots': len(metaverso_data.robots),
            'active_robots': len([r for r in metaverso_data.robots if r.status == 'Active']),
            'manufacturing_lines': len(metaverso_data.manufacturing_lines),
            'active_lines': len([l for l in metaverso_data.manufacturing_lines if l.status == 'Running']),
            'research_projects': len(metaverso_data.research_projects),
            'active_projects': len([p for p in metaverso_data.research_projects if p.status == 'Active']),
            'security_alerts': len([a for a in metaverso_data.security_alerts if not a.resolved])
        },
        'recent_activities': metaverso_data.activity_log[:10]
    })

@app.route('/api/robots')
def get_robots():
    """Get all robots data"""
    robots_data = [asdict(robot) for robot in metaverso_data.robots]
    return jsonify({
        'robots': robots_data,
        'total': len(robots_data),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/robots/<robot_id>')
def get_robot(robot_id):
    """Get specific robot data"""
    robot = next((r for r in metaverso_data.robots if r.id == robot_id), None)
    if robot:
        return jsonify(asdict(robot))
    return jsonify({'error': 'Robot not found'}), 404

@app.route('/api/robots/<robot_id>', methods=['PUT'])
def update_robot(robot_id):
    """Update robot data"""
    robot = next((r for r in metaverso_data.robots if r.id == robot_id), None)
    if not robot:
        return jsonify({'error': 'Robot not found'}), 404
    
    data = request.json
    if 'status' in data:
        robot.status = data['status']
    if 'efficiency' in data:
        robot.efficiency = float(data['efficiency'])
    
    robot.last_update = datetime.datetime.now().isoformat()
    
    metaverso_data.add_activity('system', f'Robot {robot_id} actualizado: {data}')
    
    return jsonify(asdict(robot))

@app.route('/api/manufacturing')
def get_manufacturing():
    """Get manufacturing data"""
    lines_data = [asdict(line) for line in metaverso_data.manufacturing_lines]
    return jsonify({
        'manufacturing_lines': lines_data,
        'total': len(lines_data),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/manufacturing/<line_id>', methods=['PUT'])
def update_manufacturing_line(line_id):
    """Update manufacturing line"""
    line = next((l for l in metaverso_data.manufacturing_lines if l.id == line_id), None)
    if not line:
        return jsonify({'error': 'Manufacturing line not found'}), 404
    
    data = request.json
    if 'status' in data:
        line.status = data['status']
    if 'production_rate' in data:
        line.production_rate = float(data['production_rate'])
    
    metaverso_data.add_activity('manufacturing', f'Línea {line_id} actualizada')
    
    return jsonify(asdict(line))

@app.route('/api/research')
def get_research():
    """Get research projects data"""
    projects_data = [asdict(project) for project in metaverso_data.research_projects]
    return jsonify({
        'research_projects': projects_data,
        'total': len(projects_data),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/research/<project_id>', methods=['PUT'])
def update_research_project(project_id):
    """Update research project"""
    project = next((p for p in metaverso_data.research_projects if p.id == project_id), None)
    if not project:
        return jsonify({'error': 'Research project not found'}), 404
    
    data = request.json
    if 'status' in data:
        project.status = data['status']
    if 'progress' in data:
        project.progress = float(data['progress'])
    
    metaverso_data.add_activity('research', f'Proyecto {project_id} actualizado')
    
    return jsonify(asdict(project))

@app.route('/api/security')
def get_security():
    """Get security data"""
    alerts_data = [asdict(alert) for alert in metaverso_data.security_alerts]
    return jsonify({
        'security_alerts': alerts_data,
        'total': len(alerts_data),
        'unresolved': len([a for a in metaverso_data.security_alerts if not a.resolved]),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/security/alerts', methods=['POST'])
def create_security_alert():
    """Create new security alert"""
    data = request.json
    alert = SecurityAlert(
        id=f"ALERT-{len(metaverso_data.security_alerts) + 1:03d}",
        level=data.get('level', 'low'),
        message=data.get('message', ''),
        timestamp=datetime.datetime.now().isoformat(),
        resolved=False
    )
    metaverso_data.security_alerts.append(alert)
    metaverso_data.add_activity('security', f'Nueva alerta: {alert.message}', 'warning')
    
    return jsonify(asdict(alert)), 201

@app.route('/api/activities')
def get_activities():
    """Get activity log"""
    limit = request.args.get('limit', 50, type=int)
    activity_type = request.args.get('type', None)
    
    activities = metaverso_data.activity_log
    if activity_type:
        activities = [a for a in activities if a['type'] == activity_type]
    
    return jsonify({
        'activities': activities[:limit],
        'total': len(activities),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/metrics/export')
def export_metrics():
    """Export system metrics"""
    export_data = {
        'export_timestamp': datetime.datetime.now().isoformat(),
        'system_metrics': asdict(metaverso_data.system_metrics),
        'robots': [asdict(robot) for robot in metaverso_data.robots],
        'manufacturing_lines': [asdict(line) for line in metaverso_data.manufacturing_lines],
        'research_projects': [asdict(project) for project in metaverso_data.research_projects],
        'security_alerts': [asdict(alert) for alert in metaverso_data.security_alerts],
        'recent_activities': metaverso_data.activity_log[:100]
    }
    
    return jsonify(export_data)

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected')
    emit('connected', {'status': 'Connected to Metaverso Backend'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')

@socketio.on('request_update')
def handle_update_request():
    """Handle real-time update request"""
    emit('system_update', {
        'metrics': asdict(metaverso_data.system_metrics),
        'latest_activity': metaverso_data.activity_log[0] if metaverso_data.activity_log else None
    })

@socketio.on('robot_command')
def handle_robot_command(data):
    """Handle robot command"""
    robot_id = data.get('robot_id')
    command = data.get('command')
    
    robot = next((r for r in metaverso_data.robots if r.id == robot_id), None)
    if robot:
        metaverso_data.add_activity('system', f'Comando enviado a {robot_id}: {command}')
        emit('command_response', {'status': 'success', 'robot_id': robot_id, 'command': command})
    else:
        emit('command_response', {'status': 'error', 'message': 'Robot not found'})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info('🚀 Starting Metaverso Backend Server...')
    logger.info('📡 WebSocket support enabled')
    logger.info('🔄 Real-time updates active')
    
    # Run the application
    socketio.run(
        app,
        host='127.0.0.1',
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )