"""
METAVERSO BACKEND API - PROFESSIONAL FLASK APPLICATION
Advanced backend server for Robot City Metaverse with error handling and reliability
"""

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import datetime
import logging
import os
import random
import threading
import time
import traceback
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import sys

# Configure professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('metaverso.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app with error handling
app = Flask(__name__)
app.config['SECRET_KEY'] = 'metaverso_secret_2024_professional'
app.config['DEBUG'] = True
app.config['TESTING'] = False

# Enable CORS with specific configuration
CORS(app, origins=["*"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Initialize SocketIO with error handling
try:
    socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)
    logger.info("✅ SocketIO initialized successfully")
except Exception as e:
    logger.error(f"❌ SocketIO initialization failed: {e}")
    socketio = None

# Global state management
class SystemState:
    def __init__(self):
        self.is_running = False
        self.connected_clients = 0
        self.last_update = datetime.datetime.now()
        self.error_count = 0
        self.system_health = "healthy"
        
    def update_health(self):
        if self.error_count > 10:
            self.system_health = "critical"
        elif self.error_count > 5:
            self.system_health = "warning"
        else:
            self.system_health = "healthy"

system_state = SystemState()

# Professional data models
@dataclass
class RobotStatus:
    id: str
    name: str
    type: str
    status: str
    location: Dict[str, float]
    efficiency: float
    last_update: str
    health: str = "operational"
    tasks_completed: int = 0

@dataclass
class ManufacturingLine:
    id: str
    name: str
    status: str
    production_rate: float
    quality_score: float
    robots_assigned: List[str]
    current_product: str
    uptime: float = 98.5

@dataclass
class ResearchProject:
    id: str
    name: str
    field: str
    progress: float
    researchers: List[str]
    budget: float
    deadline: str
    priority: str = "medium"

@dataclass
class SystemMetrics:
    timestamp: str
    robots_active: int
    robots_total: int
    manufacturing_efficiency: float
    research_progress: float
    energy_consumption: float
    network_status: str
    security_level: str

# Professional error handling
class MetaversoError(Exception):
    """Custom exception for Metaverso application"""
    pass

def handle_error(func):
    """Decorator for professional error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            system_state.error_count += 1
            system_state.update_health()
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({'error': str(e), 'status': 'error'}), 500
    wrapper.__name__ = func.__name__
    return wrapper

# Initialize sample data with professional structure
def initialize_professional_data():
    """Initialize comprehensive sample data"""
    global robots_data, manufacturing_data, research_data
    
    # Professional robot fleet
    robots_data = [
        RobotStatus(
            id="R-001", name="Alpha Constructor", type="Construction", 
            status="active", location={"x": 10, "y": 5, "z": 0}, 
            efficiency=94.5, last_update=datetime.datetime.now().isoformat(),
            health="excellent", tasks_completed=156
        ),
        RobotStatus(
            id="R-002", name="Beta Researcher", type="Research", 
            status="active", location={"x": -5, "y": 8, "z": 2}, 
            efficiency=97.2, last_update=datetime.datetime.now().isoformat(),
            health="good", tasks_completed=89
        ),
        RobotStatus(
            id="R-003", name="Gamma Security", type="Security", 
            status="patrol", location={"x": 0, "y": 0, "z": 5}, 
            efficiency=99.1, last_update=datetime.datetime.now().isoformat(),
            health="excellent", tasks_completed=234
        ),
        RobotStatus(
            id="R-004", name="Delta Maintenance", type="Maintenance", 
            status="repair", location={"x": 7, "y": -3, "z": 1}, 
            efficiency=88.7, last_update=datetime.datetime.now().isoformat(),
            health="fair", tasks_completed=67
        ),
    ]
    
    # Advanced manufacturing lines
    manufacturing_data = [
        ManufacturingLine(
            id="ML-001", name="Robot Assembly Line Alpha", status="active",
            production_rate=12.5, quality_score=96.8, 
            robots_assigned=["R-001", "R-004"], current_product="Constructor Bots",
            uptime=99.2
        ),
        ManufacturingLine(
            id="ML-002", name="Research Equipment Production", status="active",
            production_rate=8.3, quality_score=98.1, 
            robots_assigned=["R-002"], current_product="Lab Equipment",
            uptime=97.8
        ),
    ]
    
    # Comprehensive research projects
    research_data = [
        ResearchProject(
            id="RP-001", name="Advanced AI Neural Networks", field="Artificial Intelligence",
            progress=73.5, researchers=["Dr. Chen", "Dr. Martinez"], 
            budget=2500000, deadline="2025-12-31", priority="high"
        ),
        ResearchProject(
            id="RP-002", name="Quantum Computing Integration", field="Quantum Physics",
            progress=45.2, researchers=["Dr. Thompson", "Dr. Kumar"], 
            budget=3200000, deadline="2026-06-30", priority="critical"
        ),
        ResearchProject(
            id="RP-003", name="Nanotechnology Applications", field="Nanotechnology",
            progress=62.8, researchers=["Dr. Wilson", "Dr. Lee"], 
            budget=1800000, deadline="2025-10-15", priority="medium"
        ),
    ]
    
    logger.info("✅ Professional data initialized successfully")

# Professional route handlers
@app.route('/favicon.ico')
def favicon():
    """Serve favicon with error handling"""
    try:
        return send_from_directory('static', 'favicon.ico')
    except:
        return '', 204

@app.route('/health')
@handle_error
def health_check():
    """Professional health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'system_health': system_state.system_health,
        'connected_clients': system_state.connected_clients,
        'error_count': system_state.error_count,
        'uptime': (datetime.datetime.now() - system_state.last_update).total_seconds()
    })

@app.route('/')
@handle_error
def index():
    """Serve the main application with fallback"""
    try:
        return render_template('metaverso_app.html')
    except Exception as e:
        logger.warning(f"Main template failed, serving fallback: {e}")
        return render_template('test_simple.html')

@app.route('/advanced')
@handle_error
def advanced_app():
    """Serve the advanced metaverso application"""
    return render_template('advanced_metaverso.html')

@app.route('/ciudad3d')
@handle_error
def ciudad_3d():
    """Serve the 3D city viewer"""
    return render_template('ciudad_robot_3d.html')

@app.route('/test')
@handle_error
def test_simple():
    """Serve simple test page"""
    return render_template('test_simple.html')

@app.route('/professional')
@handle_error
def professional_dashboard():
    """Serve the professional dashboard"""
    return render_template('professional_dashboard.html')

@app.route('/dashboard')
@handle_error
def dashboard():
    """Professional dashboard with comprehensive metrics"""
    try:
        return render_template('metaverso_dashboard.html')
    except:
        return render_template('test_simple.html')

# Professional API endpoints
@app.route('/api/robots')
@handle_error
def get_robots():
    """Get all robots with professional data structure"""
    return jsonify([asdict(robot) for robot in robots_data])

@app.route('/api/robots/<robot_id>')
@handle_error
def get_robot(robot_id):
    """Get specific robot details"""
    robot = next((r for r in robots_data if r.id == robot_id), None)
    if robot:
        return jsonify(asdict(robot))
    return jsonify({'error': 'Robot not found'}), 404

@app.route('/api/manufacturing')
@handle_error
def get_manufacturing():
    """Get manufacturing data"""
    return jsonify([asdict(line) for line in manufacturing_data])

@app.route('/api/research')
@handle_error
def get_research():
    """Get research projects"""
    return jsonify([asdict(project) for project in research_data])

@app.route('/api/metrics')
@handle_error
def get_metrics():
    """Get real-time system metrics"""
    metrics = SystemMetrics(
        timestamp=datetime.datetime.now().isoformat(),
        robots_active=len([r for r in robots_data if r.status == "active"]),
        robots_total=len(robots_data),
        manufacturing_efficiency=sum(line.production_rate for line in manufacturing_data) / len(manufacturing_data) if manufacturing_data else 0,
        research_progress=sum(project.progress for project in research_data) / len(research_data) if research_data else 0,
        energy_consumption=random.uniform(1200, 1800),
        network_status="optimal",
        security_level="high"
    )
    return jsonify(asdict(metrics))

@app.route('/api/system/restart', methods=['POST'])
@handle_error
def restart_system():
    """Professional system restart endpoint"""
    logger.info("🔄 System restart requested")
    system_state.error_count = 0
    system_state.update_health()
    initialize_professional_data()
    return jsonify({'status': 'restarted', 'timestamp': datetime.datetime.now().isoformat()})

# Professional WebSocket handlers
if socketio:
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection with logging"""
        system_state.connected_clients += 1
        logger.info(f"✅ Client connected. Total clients: {system_state.connected_clients}")
        emit('system_status', {
            'status': 'connected',
            'system_health': system_state.system_health,
            'timestamp': datetime.datetime.now().isoformat()
        })

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        system_state.connected_clients = max(0, system_state.connected_clients - 1)
        logger.info(f"❌ Client disconnected. Total clients: {system_state.connected_clients}")

    @socketio.on('robot_command')
    def handle_robot_command(data):
        """Handle robot commands with validation"""
        try:
            robot_id = data.get('robot_id')
            command = data.get('command')
            
            if not robot_id or not command:
                emit('error', {'message': 'Invalid command data'})
                return
                
            robot = next((r for r in robots_data if r.id == robot_id), None)
            if robot:
                robot.last_update = datetime.datetime.now().isoformat()
                logger.info(f"🤖 Command '{command}' sent to robot {robot_id}")
                emit('command_response', {
                    'status': 'success', 
                    'robot_id': robot_id, 
                    'command': command,
                    'timestamp': robot.last_update
                })
            else:
                emit('error', {'message': f'Robot {robot_id} not found'})
                
        except Exception as e:
            logger.error(f"Error handling robot command: {e}")
            emit('error', {'message': 'Command processing failed'})

# Professional data update system
def update_system_data():
    """Professional real-time data updates"""
    while system_state.is_running:
        try:
            # Update robot positions and efficiency
            for robot in robots_data:
                robot.efficiency = max(70, min(100, robot.efficiency + random.uniform(-2, 3)))
                robot.location['x'] += random.uniform(-0.5, 0.5)
                robot.location['y'] += random.uniform(-0.5, 0.5)
                robot.last_update = datetime.datetime.now().isoformat()
                
                # Simulate task completion
                if random.random() < 0.1:  # 10% chance
                    robot.tasks_completed += 1
            
            # Update manufacturing efficiency
            for line in manufacturing_data:
                line.production_rate = max(5, min(20, line.production_rate + random.uniform(-1, 2)))
                line.quality_score = max(85, min(100, line.quality_score + random.uniform(-1, 1)))
                line.uptime = max(90, min(100, line.uptime + random.uniform(-0.1, 0.2)))
            
            # Update research progress
            for project in research_data:
                project.progress = min(100, project.progress + random.uniform(0, 0.5))
            
            # Emit updates via WebSocket
            if socketio and system_state.connected_clients > 0:
                socketio.emit('metrics_update', {
                    'robots': [asdict(robot) for robot in robots_data],
                    'manufacturing': [asdict(line) for line in manufacturing_data],
                    'research': [asdict(project) for project in research_data],
                    'timestamp': datetime.datetime.now().isoformat()
                })
            
            system_state.last_update = datetime.datetime.now()
            
        except Exception as e:
            logger.error(f"Error updating system data: {e}")
            system_state.error_count += 1
            system_state.update_health()
        
        time.sleep(2)  # Update every 2 seconds

# Professional error handlers
@app.errorhandler(404)
def not_found(error):
    """Professional 404 handler"""
    logger.warning(f"404 error: {request.url}")
    return jsonify({
        'error': 'Endpoint not found',
        'status': 404,
        'timestamp': datetime.datetime.now().isoformat(),
        'requested_url': request.url
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Professional 500 handler"""
    logger.error(f"Internal server error: {error}")
    system_state.error_count += 1
    system_state.update_health()
    return jsonify({
        'error': 'Internal server error',
        'status': 500,
        'timestamp': datetime.datetime.now().isoformat(),
        'system_health': system_state.system_health
    }), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all other exceptions"""
    logger.error(f"Unhandled exception: {e}")
    logger.error(traceback.format_exc())
    system_state.error_count += 1
    system_state.update_health()
    return jsonify({
        'error': 'Unexpected error occurred',
        'status': 500,
        'timestamp': datetime.datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    try:
        logger.info('🚀 Starting Professional Metaverso Backend Server...')
        logger.info('📡 WebSocket support enabled')
        logger.info('🔄 Real-time updates active')
        logger.info('🛡️ Professional error handling enabled')
        logger.info('📊 Health monitoring active')
        
        # Initialize data
        initialize_professional_data()
        
        # Start background data updates
        system_state.is_running = True
        update_thread = threading.Thread(target=update_system_data, daemon=True)
        update_thread.start()
        logger.info('📈 Background data updates started')
        
        # Run the professional application
        if socketio:
            socketio.run(
                app,
                host='127.0.0.1',
                port=5000,
                debug=True,
                allow_unsafe_werkzeug=True,
                use_reloader=False  # Prevent issues with threading
            )
        else:
            app.run(
                host='127.0.0.1',
                port=5000,
                debug=True
            )
            
    except KeyboardInterrupt:
        logger.info('🛑 Server shutdown requested')
        system_state.is_running = False
    except Exception as e:
        logger.error(f'❌ Critical error starting server: {e}')
        logger.error(traceback.format_exc())
        sys.exit(1)
    finally:
        system_state.is_running = False
        logger.info('🏁 Server shutdown complete')