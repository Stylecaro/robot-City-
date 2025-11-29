// Dashboard de Seguridad 3D - Componente React
// Visualización avanzada del sistema de humanoides de seguridad

import React, { useState, useEffect, useRef, useMemo } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { 
  OrbitControls, 
  Text, 
  Html, 
  useGLTF, 
  Environment,
  PerspectiveCamera,
  Grid,
  Stats
} from '@react-three/drei';
import * as THREE from 'three';
import { useSpring, animated } from '@react-spring/three';
import { io } from 'socket.io-client';

// Hooks personalizados
import { useWebSocket } from '../hooks/useWebSocket';
import { useSecurityAPI } from '../hooks/useSecurityAPI';

// Componentes
import SecurityHUD from './SecurityHUD';
import ThreatIndicator from './ThreatIndicator';
import SecurityZone from './SecurityZone';
import AlertOverlay from './AlertOverlay';

// Constantes
const HUMANOID_TYPES = {
  guardian: { color: '#00ff00', scale: 1.0, model: 'guardian.glb' },
  sentinel: { color: '#0080ff', scale: 1.2, model: 'sentinel.glb' },
  interceptor: { color: '#ff8000', scale: 0.9, model: 'interceptor.glb' },
  scout: { color: '#ffff00', scale: 0.7, model: 'scout.glb' },
  commander: { color: '#ff0080', scale: 1.3, model: 'commander.glb' },
  medic: { color: '#80ff80', scale: 1.0, model: 'medic.glb' },
  cyber_defender: { color: '#8080ff', scale: 1.1, model: 'cyber_defender.glb' },
  heavy_guardian: { color: '#ff4040', scale: 1.5, model: 'heavy_guardian.glb' }
};

const ALERT_COLORS = {
  GREEN: '#00ff00',
  YELLOW: '#ffff00',
  ORANGE: '#ff8000',
  RED: '#ff0000',
  BLACK: '#800080'
};

// Componente principal del dashboard
const SecurityDashboard3D = () => {
  // Estados principales
  const [securityData, setSecurityData] = useState({
    humanoids: {},
    zones: {},
    incidents: [],
    alert_level: 'GREEN',
    metrics: {}
  });
  
  const [selectedHumanoid, setSelectedHumanoid] = useState(null);
  const [viewMode, setViewMode] = useState('overview'); // overview, tactical, zones
  const [showMetrics, setShowMetrics] = useState(true);
  const [cameraPosition, setCameraPosition] = useState([50, 50, 50]);
  
  // Referencias
  const canvasRef = useRef();
  const socketRef = useRef();
  
  // Hooks personalizados
  const { securityState, sendCommand, error } = useSecurityAPI();
  const { connected, lastMessage } = useWebSocket('ws://localhost:8000');

  // Efectos
  useEffect(() => {
    // Inicializar conexión WebSocket para eventos en tiempo real
    socketRef.current = io('http://localhost:8000');
    
    socketRef.current.on('security_update', (data) => {
      setSecurityData(prev => ({ ...prev, ...data }));
    });
    
    socketRef.current.on('humanoid_deployed', (data) => {
      setSecurityData(prev => ({
        ...prev,
        humanoids: {
          ...prev.humanoids,
          [data.humanoid.id]: data.humanoid
        }
      }));
    });
    
    socketRef.current.on('threat_detected', (data) => {
      setSecurityData(prev => ({
        ...prev,
        incidents: [data.threat, ...prev.incidents.slice(0, 49)]
      }));
    });
    
    socketRef.current.on('alert_level_changed', (data) => {
      setSecurityData(prev => ({
        ...prev,
        alert_level: data.level
      }));
    });
    
    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);

  useEffect(() => {
    // Cargar datos iniciales de seguridad
    if (securityState) {
      setSecurityData(securityState);
    }
  }, [securityState]);

  // Memoizar datos procesados
  const processedData = useMemo(() => {
    const humanoidsList = Object.values(securityData.humanoids || {});
    const zonesList = Object.values(securityData.zones || {});
    const activeIncidents = securityData.incidents?.filter(i => i.status === 'active') || [];
    
    return {
      humanoids: humanoidsList,
      zones: zonesList,
      activeIncidents,
      totalHumanoids: humanoidsList.length,
      activeHumanoids: humanoidsList.filter(h => h.status === 'active').length,
      threatsDetected: activeIncidents.length
    };
  }, [securityData]);

  // Manejadores de eventos
  const handleHumanoidClick = (humanoid) => {
    setSelectedHumanoid(humanoid);
  };

  const handleDeployHumanoid = async (type, position) => {
    try {
      await sendCommand('deploy', {
        type,
        position,
        priority: 'normal'
      });
    } catch (error) {
      console.error('Error desplegando humanoide:', error);
    }
  };

  const handleChangeAlertLevel = async (level, reason) => {
    try {
      await sendCommand('alert_level', { level, reason });
    } catch (error) {
      console.error('Error cambiando nivel de alerta:', error);
    }
  };

  return (
    <div className="security-dashboard-container">
      {/* HUD superior */}
      <SecurityHUD 
        data={processedData}
        alertLevel={securityData.alert_level}
        onViewModeChange={setViewMode}
        onToggleMetrics={() => setShowMetrics(!showMetrics)}
        onChangeAlertLevel={handleChangeAlertLevel}
      />
      
      {/* Canvas 3D principal */}
      <div className="canvas-container">
        <Canvas
          ref={canvasRef}
          camera={{ position: cameraPosition, fov: 60 }}
          onCreated={({ gl }) => {
            gl.setClearColor('#001122');
            gl.shadowMap.enabled = true;
            gl.shadowMap.type = THREE.PCFSoftShadowMap;
          }}
        >
          {/* Configuración de cámara y controles */}
          <PerspectiveCamera makeDefault position={cameraPosition} />
          <OrbitControls
            enablePan={true}
            enableZoom={true}
            enableRotate={true}
            maxDistance={200}
            minDistance={10}
          />
          
          {/* Iluminación */}
          <ambientLight intensity={0.3} />
          <directionalLight
            position={[100, 100, 50]}
            intensity={1}
            castShadow
            shadow-mapSize-width={2048}
            shadow-mapSize-height={2048}
          />
          <pointLight position={[0, 50, 0]} intensity={0.5} color="#4080ff" />
          
          {/* Entorno */}
          <Environment preset="night" />
          <Grid
            args={[200, 200]}
            cellSize={5}
            cellThickness={0.5}
            cellColor="#003366"
            sectionSize={25}
            sectionThickness={1}
            sectionColor="#0066cc"
            fadeDistance={150}
            fadeStrength={1}
          />
          
          {/* Zonas de seguridad */}
          {processedData.zones.map(zone => (
            <SecurityZone
              key={zone.zone_id}
              zone={zone}
              alertLevel={securityData.alert_level}
              viewMode={viewMode}
            />
          ))}
          
          {/* Humanoides de seguridad */}
          {processedData.humanoids.map(humanoid => (
            <SecurityHumanoid3D
              key={humanoid.id}
              humanoid={humanoid}
              isSelected={selectedHumanoid?.id === humanoid.id}
              onClick={() => handleHumanoidClick(humanoid)}
              alertLevel={securityData.alert_level}
            />
          ))}
          
          {/* Indicadores de amenazas */}
          {processedData.activeIncidents.map(incident => (
            <ThreatIndicator
              key={incident.id}
              incident={incident}
              alertLevel={securityData.alert_level}
            />
          ))}
          
          {/* Estadísticas de rendimiento */}
          {process.env.NODE_ENV === 'development' && <Stats />}
        </Canvas>
      </div>
      
      {/* Overlays y paneles */}
      {selectedHumanoid && (
        <HumanoidDetailPanel
          humanoid={selectedHumanoid}
          onClose={() => setSelectedHumanoid(null)}
          onSendCommand={sendCommand}
        />
      )}
      
      {securityData.alert_level !== 'GREEN' && (
        <AlertOverlay
          alertLevel={securityData.alert_level}
          incidents={processedData.activeIncidents}
        />
      )}
      
      {showMetrics && (
        <MetricsPanel
          metrics={securityData.metrics}
          realTimeData={processedData}
        />
      )}
      
      {/* Panel de control de despliegue */}
      <DeploymentPanel
        onDeploy={handleDeployHumanoid}
        availableTypes={Object.keys(HUMANOID_TYPES)}
      />
    </div>
  );
};

// Componente para humanoide 3D individual
const SecurityHumanoid3D = ({ humanoid, isSelected, onClick, alertLevel }) => {
  const meshRef = useRef();
  const { scene } = useGLTF(`/models/${HUMANOID_TYPES[humanoid.type]?.model || 'default.glb'}`);
  
  // Animación de selección
  const { scale, emissive } = useSpring({
    scale: isSelected ? 1.2 : 1.0,
    emissive: isSelected ? 0.3 : 0.0,
    config: { mass: 1, tension: 300, friction: 30 }
  });
  
  // Animación de estado
  const statusColor = useMemo(() => {
    switch (humanoid.status) {
      case 'active': return '#00ff00';
      case 'patrol': return '#ffff00';
      case 'responding': return '#ff8000';
      case 'maintenance': return '#808080';
      default: return '#ffffff';
    }
  }, [humanoid.status]);
  
  // Animación de movimiento
  useFrame((state, delta) => {
    if (meshRef.current && humanoid.status === 'patrol') {
      meshRef.current.rotation.y += delta * 0.5;
    }
  });
  
  return (
    <group
      ref={meshRef}
      position={[humanoid.position.x, humanoid.position.y, humanoid.position.z]}
      onClick={onClick}
    >
      {/* Modelo 3D del humanoide */}
      <animated.primitive
        object={scene.clone()}
        scale={scale}
      />
      
      {/* Indicador de estado */}
      <mesh position={[0, 3, 0]}>
        <sphereGeometry args={[0.2, 8, 8]} />
        <animated.meshBasicMaterial
          color={statusColor}
          emissive={statusColor}
          emissiveIntensity={emissive}
        />
      </mesh>
      
      {/* Etiqueta de información */}
      <Html
        position={[0, 4, 0]}
        center
        distanceFactor={15}
        occlude={false}
      >
        <div className="humanoid-label">
          <div className="humanoid-id">{humanoid.id}</div>
          <div className="humanoid-type">{humanoid.type}</div>
          <div className="humanoid-status">{humanoid.status}</div>
          {humanoid.energy < 20 && (
            <div className="low-energy">⚡ {humanoid.energy}%</div>
          )}
        </div>
      </Html>
      
      {/* Área de detección/patrullaje */}
      {humanoid.status === 'patrol' && (
        <mesh>
          <ringGeometry args={[8, 10, 32]} />
          <meshBasicMaterial
            color={HUMANOID_TYPES[humanoid.type]?.color || '#ffffff'}
            transparent
            opacity={0.1}
            side={THREE.DoubleSide}
          />
        </mesh>
      )}
    </group>
  );
};

// Panel de detalles del humanoide
const HumanoidDetailPanel = ({ humanoid, onClose, onSendCommand }) => {
  const [selectedCommand, setSelectedCommand] = useState('');
  
  const commands = [
    { id: 'patrol', label: 'Patrullar', icon: '🚶' },
    { id: 'investigate', label: 'Investigar', icon: '🔍' },
    { id: 'respond', label: 'Responder', icon: '🚨' },
    { id: 'return_base', label: 'Volver a Base', icon: '🏠' },
    { id: 'emergency_stop', label: 'Parada de Emergencia', icon: '⛔' },
    { id: 'recharge', label: 'Recargar', icon: '🔋' }
  ];
  
  const handleSendCommand = async () => {
    if (selectedCommand) {
      try {
        await onSendCommand('humanoid_command', {
          humanoid_id: humanoid.id,
          command: selectedCommand
        });
        setSelectedCommand('');
      } catch (error) {
        console.error('Error enviando comando:', error);
      }
    }
  };
  
  return (
    <div className="humanoid-detail-panel">
      <div className="panel-header">
        <h3>Humanoide {humanoid.id}</h3>
        <button onClick={onClose} className="close-button">×</button>
      </div>
      
      <div className="panel-content">
        <div className="basic-info">
          <div className="info-row">
            <span>Tipo:</span>
            <span className="info-value">{humanoid.type}</span>
          </div>
          <div className="info-row">
            <span>Estado:</span>
            <span className={`status ${humanoid.status}`}>{humanoid.status}</span>
          </div>
          <div className="info-row">
            <span>Energía:</span>
            <div className="energy-bar">
              <div 
                className="energy-fill"
                style={{ width: `${humanoid.energy}%` }}
              />
              <span className="energy-text">{humanoid.energy}%</span>
            </div>
          </div>
          <div className="info-row">
            <span>Armadura:</span>
            <span className="info-value">{humanoid.armor}%</span>
          </div>
          <div className="info-row">
            <span>Escudos:</span>
            <span className="info-value">{humanoid.shields}%</span>
          </div>
        </div>
        
        <div className="position-info">
          <h4>Posición</h4>
          <div className="coordinates">
            X: {humanoid.position.x.toFixed(1)}<br/>
            Y: {humanoid.position.y.toFixed(1)}<br/>
            Z: {humanoid.position.z.toFixed(1)}
          </div>
        </div>
        
        <div className="performance-metrics">
          <h4>Métricas de Rendimiento</h4>
          <div className="metrics-grid">
            <div className="metric">
              <span>Amenazas Neutralizadas</span>
              <span>{humanoid.performance_metrics?.threats_neutralized || 0}</span>
            </div>
            <div className="metric">
              <span>Tiempo Resp. Promedio</span>
              <span>{humanoid.performance_metrics?.response_time_avg || 0}s</span>
            </div>
            <div className="metric">
              <span>Tasa de Éxito</span>
              <span>{((humanoid.performance_metrics?.success_rate || 0) * 100).toFixed(1)}%</span>
            </div>
            <div className="metric">
              <span>Tiempo Operativo</span>
              <span>{humanoid.performance_metrics?.uptime_percentage || 0}%</span>
            </div>
          </div>
        </div>
        
        <div className="command-section">
          <h4>Comandos</h4>
          <div className="command-buttons">
            {commands.map(cmd => (
              <button
                key={cmd.id}
                className={`command-btn ${selectedCommand === cmd.id ? 'selected' : ''}`}
                onClick={() => setSelectedCommand(cmd.id)}
              >
                <span className="command-icon">{cmd.icon}</span>
                {cmd.label}
              </button>
            ))}
          </div>
          <button
            className="send-command-btn"
            onClick={handleSendCommand}
            disabled={!selectedCommand}
          >
            Enviar Comando
          </button>
        </div>
      </div>
    </div>
  );
};

// Panel de métricas en tiempo real
const MetricsPanel = ({ metrics, realTimeData }) => {
  return (
    <div className="metrics-panel">
      <h3>Métricas de Seguridad</h3>
      
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-title">Humanoides Activos</div>
          <div className="metric-value">{realTimeData.activeHumanoids}/{realTimeData.totalHumanoids}</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-title">Amenazas Detectadas</div>
          <div className="metric-value">{metrics.total_threats_detected || 0}</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-title">Tiempo Resp. Promedio</div>
          <div className="metric-value">{(metrics.average_response_time || 0).toFixed(1)}s</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-title">Cobertura</div>
          <div className="metric-value">{(metrics.coverage_percentage || 0).toFixed(1)}%</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-title">Falsos Positivos</div>
          <div className="metric-value">{((metrics.false_positive_rate || 0) * 100).toFixed(2)}%</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-title">Amenazas Neutralizadas</div>
          <div className="metric-value">{metrics.total_threats_neutralized || 0}</div>
        </div>
      </div>
    </div>
  );
};

// Panel de despliegue de humanoides
const DeploymentPanel = ({ onDeploy, availableTypes }) => {
  const [selectedType, setSelectedType] = useState('guardian');
  const [deployPosition, setDeployPosition] = useState({ x: 0, y: 0, z: 0 });
  const [isOpen, setIsOpen] = useState(false);
  
  const handleDeploy = () => {
    onDeploy(selectedType, deployPosition);
    setIsOpen(false);
  };
  
  return (
    <div className={`deployment-panel ${isOpen ? 'open' : ''}`}>
      <button
        className="deployment-toggle"
        onClick={() => setIsOpen(!isOpen)}
      >
        🚀 Desplegar
      </button>
      
      {isOpen && (
        <div className="deployment-content">
          <h4>Desplegar Humanoide</h4>
          
          <div className="type-selection">
            <label>Tipo:</label>
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
            >
              {availableTypes.map(type => (
                <option key={type} value={type}>
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </option>
              ))}
            </select>
          </div>
          
          <div className="position-inputs">
            <label>Posición:</label>
            <div className="coordinate-inputs">
              <input
                type="number"
                placeholder="X"
                value={deployPosition.x}
                onChange={(e) => setDeployPosition(prev => ({
                  ...prev,
                  x: parseFloat(e.target.value) || 0
                }))}
              />
              <input
                type="number"
                placeholder="Y"
                value={deployPosition.y}
                onChange={(e) => setDeployPosition(prev => ({
                  ...prev,
                  y: parseFloat(e.target.value) || 0
                }))}
              />
              <input
                type="number"
                placeholder="Z"
                value={deployPosition.z}
                onChange={(e) => setDeployPosition(prev => ({
                  ...prev,
                  z: parseFloat(e.target.value) || 0
                }))}
              />
            </div>
          </div>
          
          <button
            className="deploy-button"
            onClick={handleDeploy}
          >
            Confirmar Despliegue
          </button>
        </div>
      )}
    </div>
  );
};

export default SecurityDashboard3D;