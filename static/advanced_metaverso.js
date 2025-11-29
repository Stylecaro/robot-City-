/**
 * Advanced Metaverso - Interactive Application Engine
 * Sophisticated JavaScript framework for robot city management
 */

class AdvancedMetaversoApp {
    constructor() {
        this.isInitialized = false;
        this.socket = null;
        this.threeScene = null;
        this.charts = {};
        this.notifications = [];
        this.currentView = 'dashboard';
        this.animationFrameId = null;
        this.metricsData = {
            robots: { active: 0, total: 0, trend: 0 },
            manufacturing: { production: 0, efficiency: 0, trend: 0 },
            research: { projects: 0, progress: 0, trend: 0 },
            energy: { consumption: 0, efficiency: 0, trend: 0 },
            network: { connections: 0, bandwidth: 0, trend: 0 },
            security: { alerts: 0, status: 'optimal', trend: 0 }
        };
        
        this.init();
    }

    /**
     * Initialize the application
     */
    async init() {
        try {
            this.showLoadingScreen();
            await this.loadDependencies();
            this.setupEventListeners();
            this.initializeWebSocket();
            this.initializeThreeJS();
            this.initializeCharts();
            this.startDataUpdates();
            this.hideLoadingScreen();
            this.isInitialized = true;
            this.addNotification('Sistema iniciado correctamente', 'success');
        } catch (error) {
            console.error('Error initializing application:', error);
            this.addNotification('Error al inicializar la aplicación', 'error');
        }
    }

    /**
     * Show loading screen with progress
     */
    showLoadingScreen() {
        const loadingScreen = document.querySelector('.loading-screen');
        const progressBar = document.querySelector('.loading-progress-bar');
        const loadingText = document.querySelector('.loading-text');
        
        if (loadingScreen) {
            loadingScreen.classList.remove('hidden');
            
            const steps = [
                'Cargando dependencias...',
                'Inicializando motor 3D...',
                'Conectando con servidor...',
                'Configurando métricas...',
                'Preparando interfaz...'
            ];
            
            let currentStep = 0;
            const stepInterval = setInterval(() => {
                if (currentStep < steps.length) {
                    loadingText.textContent = steps[currentStep];
                    progressBar.style.width = `${(currentStep + 1) * 20}%`;
                    currentStep++;
                } else {
                    clearInterval(stepInterval);
                }
            }, 500);
        }
    }

    /**
     * Hide loading screen
     */
    hideLoadingScreen() {
        setTimeout(() => {
            const loadingScreen = document.querySelector('.loading-screen');
            if (loadingScreen) {
                loadingScreen.classList.add('hidden');
                setTimeout(() => {
                    loadingScreen.style.display = 'none';
                }, 500);
            }
        }, 1000);
    }

    /**
     * Load external dependencies
     */
    async loadDependencies() {
        // Check if required libraries are loaded
        return new Promise((resolve) => {
            const checkLibraries = () => {
                if (typeof THREE !== 'undefined' && 
                    typeof Chart !== 'undefined' && 
                    typeof io !== 'undefined') {
                    resolve();
                } else {
                    setTimeout(checkLibraries, 100);
                }
            };
            checkLibraries();
        });
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchView(link.dataset.view);
                this.updateActiveNavigation(link);
            });
        });

        // Notification button
        const notificationBtn = document.querySelector('.notification-button');
        if (notificationBtn) {
            notificationBtn.addEventListener('click', () => {
                this.toggleNotificationPanel();
            });
        }

        // Close notification panel
        const closePanel = document.querySelector('.close-panel');
        if (closePanel) {
            closePanel.addEventListener('click', () => {
                this.closeNotificationPanel();
            });
        }

        // Control inputs
        document.querySelectorAll('.control-input, .control-range').forEach(input => {
            input.addEventListener('change', (e) => {
                this.handleControlChange(e.target);
            });
        });

        // Viewer controls
        document.querySelectorAll('.viewer-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.handleViewerControl(e.target);
            });
        });

        // Window resize
        window.addEventListener('resize', () => {
            this.handleResize();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });
    }

    /**
     * Initialize WebSocket connection
     */
    initializeWebSocket() {
        try {
            this.socket = io('http://localhost:5000');
            
            this.socket.on('connect', () => {
                console.log('Connected to server');
                this.addNotification('Conectado al servidor', 'success');
                this.updateConnectionStatus(true);
            });

            this.socket.on('disconnect', () => {
                console.log('Disconnected from server');
                this.addNotification('Desconectado del servidor', 'warning');
                this.updateConnectionStatus(false);
            });

            this.socket.on('metrics_update', (data) => {
                this.updateMetrics(data);
            });

            this.socket.on('robot_status', (data) => {
                this.updateRobotStatus(data);
            });

            this.socket.on('system_alert', (data) => {
                this.addNotification(data.message, data.type || 'info');
            });

        } catch (error) {
            console.error('WebSocket initialization failed:', error);
            this.addNotification('Error de conexión WebSocket', 'error');
        }
    }

    /**
     * Initialize Three.js 3D scene
     */
    initializeThreeJS() {
        const container = document.getElementById('threejs-container');
        if (!container) return;

        try {
            // Scene setup
            this.threeScene = {
                scene: new THREE.Scene(),
                camera: new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000),
                renderer: new THREE.WebGLRenderer({ antialias: true, alpha: true }),
                controls: null,
                objects: []
            };

            // Renderer configuration
            this.threeScene.renderer.setSize(container.clientWidth, container.clientHeight);
            this.threeScene.renderer.setClearColor(0x0f172a, 0.8);
            this.threeScene.renderer.shadowMap.enabled = true;
            this.threeScene.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(this.threeScene.renderer.domElement);

            // Camera position
            this.threeScene.camera.position.set(10, 10, 10);
            this.threeScene.camera.lookAt(0, 0, 0);

            // Lighting
            const ambientLight = new THREE.AmbientLight(0x667eea, 0.6);
            this.threeScene.scene.add(ambientLight);

            const directionalLight = new THREE.DirectionalLight(0xf093fb, 0.8);
            directionalLight.position.set(10, 10, 5);
            directionalLight.castShadow = true;
            directionalLight.shadow.mapSize.width = 2048;
            directionalLight.shadow.mapSize.height = 2048;
            this.threeScene.scene.add(directionalLight);

            // Create city environment
            this.createCityEnvironment();

            // Start animation loop
            this.animate();

            this.addNotification('Visualización 3D iniciada', 'success');

        } catch (error) {
            console.error('Three.js initialization failed:', error);
            this.addNotification('Error al inicializar visualización 3D', 'error');
        }
    }

    /**
     * Create 3D city environment
     */
    createCityEnvironment() {
        if (!this.threeScene) return;

        // Ground plane
        const groundGeometry = new THREE.PlaneGeometry(50, 50);
        const groundMaterial = new THREE.MeshLambertMaterial({ 
            color: 0x1e293b,
            transparent: true,
            opacity: 0.8
        });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        this.threeScene.scene.add(ground);

        // Buildings
        this.createBuildings();

        // Robots
        this.createRobots();

        // Particles
        this.createParticleSystem();
    }

    /**
     * Create city buildings
     */
    createBuildings() {
        const buildingConfigs = [
            { x: -10, z: -10, height: 8, color: 0x667eea },
            { x: 10, z: -10, height: 12, color: 0xf093fb },
            { x: -10, z: 10, height: 6, color: 0x4ade80 },
            { x: 10, z: 10, height: 10, color: 0xfbbf24 },
            { x: 0, z: 0, height: 15, color: 0xf6d365 }
        ];

        buildingConfigs.forEach(config => {
            const geometry = new THREE.BoxGeometry(4, config.height, 4);
            const material = new THREE.MeshPhongMaterial({ 
                color: config.color,
                transparent: true,
                opacity: 0.8
            });
            const building = new THREE.Mesh(geometry, material);
            building.position.set(config.x, config.height / 2, config.z);
            building.castShadow = true;
            building.receiveShadow = true;
            this.threeScene.scene.add(building);
            this.threeScene.objects.push(building);
        });
    }

    /**
     * Create robot entities
     */
    createRobots() {
        const robotCount = 8;
        for (let i = 0; i < robotCount; i++) {
            const geometry = new THREE.SphereGeometry(0.5, 16, 16);
            const material = new THREE.MeshPhongMaterial({ 
                color: 0x3b82f6,
                emissive: 0x1e40af,
                emissiveIntensity: 0.2
            });
            const robot = new THREE.Mesh(geometry, material);
            
            const angle = (i / robotCount) * Math.PI * 2;
            const radius = 15;
            robot.position.set(
                Math.cos(angle) * radius,
                1,
                Math.sin(angle) * radius
            );
            
            robot.castShadow = true;
            robot.userData = { isRobot: true, id: i, angle: angle };
            this.threeScene.scene.add(robot);
            this.threeScene.objects.push(robot);
        }
    }

    /**
     * Create particle system
     */
    createParticleSystem() {
        const particleCount = 100;
        const particles = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        
        for (let i = 0; i < particleCount * 3; i += 3) {
            positions[i] = (Math.random() - 0.5) * 100;     // x
            positions[i + 1] = Math.random() * 20;          // y
            positions[i + 2] = (Math.random() - 0.5) * 100; // z
        }
        
        particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        const particleMaterial = new THREE.PointsMaterial({
            color: 0x667eea,
            size: 0.1,
            transparent: true,
            opacity: 0.6
        });
        
        const particleSystem = new THREE.Points(particles, particleMaterial);
        this.threeScene.scene.add(particleSystem);
        this.threeScene.objects.push(particleSystem);
    }

    /**
     * Animation loop
     */
    animate() {
        this.animationFrameId = requestAnimationFrame(() => this.animate());
        
        if (this.threeScene && this.threeScene.scene) {
            // Animate robots
            this.threeScene.objects.forEach(obj => {
                if (obj.userData && obj.userData.isRobot) {
                    obj.userData.angle += 0.01;
                    const radius = 15;
                    obj.position.x = Math.cos(obj.userData.angle) * radius;
                    obj.position.z = Math.sin(obj.userData.angle) * radius;
                    obj.rotation.y += 0.02;
                }
            });

            // Animate buildings (subtle breathing effect)
            this.threeScene.objects.forEach((obj, index) => {
                if (!obj.userData || !obj.userData.isRobot) {
                    const scale = 1 + Math.sin(Date.now() * 0.001 + index) * 0.02;
                    obj.scale.y = scale;
                }
            });

            this.threeScene.renderer.render(this.threeScene.scene, this.threeScene.camera);
        }
    }

    /**
     * Initialize charts
     */
    initializeCharts() {
        try {
            this.initializeSparklineCharts();
            this.addNotification('Gráficos inicializados', 'success');
        } catch (error) {
            console.error('Chart initialization failed:', error);
            this.addNotification('Error al inicializar gráficos', 'error');
        }
    }

    /**
     * Initialize sparkline charts for metrics
     */
    initializeSparklineCharts() {
        const chartElements = document.querySelectorAll('.metric-chart canvas');
        
        chartElements.forEach((canvas, index) => {
            const ctx = canvas.getContext('2d');
            const chartId = `sparkline-${index}`;
            
            this.charts[chartId] = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Array.from({length: 20}, (_, i) => i),
                    datasets: [{
                        data: Array.from({length: 20}, () => Math.random() * 100),
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0,
                        pointHoverRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: { enabled: false }
                    },
                    scales: {
                        x: { display: false },
                        y: { display: false }
                    },
                    animation: { duration: 0 }
                }
            });
        });
    }

    /**
     * Start automatic data updates
     */
    startDataUpdates() {
        setInterval(() => {
            this.updateMetricsDisplay();
            this.updateCharts();
        }, 2000);

        setInterval(() => {
            this.generateRandomNotification();
        }, 15000);
    }

    /**
     * Update metrics display
     */
    updateMetricsDisplay() {
        // Simulate real-time data
        this.metricsData.robots.active = Math.floor(Math.random() * 50) + 30;
        this.metricsData.robots.total = 80;
        this.metricsData.robots.trend = (Math.random() - 0.5) * 10;

        this.metricsData.manufacturing.production = Math.floor(Math.random() * 100) + 50;
        this.metricsData.manufacturing.efficiency = Math.floor(Math.random() * 30) + 70;
        this.metricsData.manufacturing.trend = (Math.random() - 0.5) * 15;

        this.metricsData.research.projects = Math.floor(Math.random() * 10) + 5;
        this.metricsData.research.progress = Math.floor(Math.random() * 40) + 60;
        this.metricsData.research.trend = (Math.random() - 0.5) * 8;

        this.metricsData.energy.consumption = Math.floor(Math.random() * 500) + 1000;
        this.metricsData.energy.efficiency = Math.floor(Math.random() * 20) + 80;
        this.metricsData.energy.trend = (Math.random() - 0.5) * 12;

        this.metricsData.network.connections = Math.floor(Math.random() * 100) + 200;
        this.metricsData.network.bandwidth = Math.floor(Math.random() * 50) + 75;
        this.metricsData.network.trend = (Math.random() - 0.5) * 20;

        this.metricsData.security.alerts = Math.floor(Math.random() * 5);
        this.metricsData.security.status = this.metricsData.security.alerts > 2 ? 'warning' : 'optimal';
        this.metricsData.security.trend = (Math.random() - 0.5) * 5;

        // Update DOM elements
        this.updateMetricCard('robots', `${this.metricsData.robots.active}/${this.metricsData.robots.total}`, this.metricsData.robots.trend);
        this.updateMetricCard('manufacturing', `${this.metricsData.manufacturing.efficiency}%`, this.metricsData.manufacturing.trend);
        this.updateMetricCard('research', `${this.metricsData.research.projects} Proyectos`, this.metricsData.research.trend);
        this.updateMetricCard('energy', `${this.metricsData.energy.consumption}kW`, this.metricsData.energy.trend);
        this.updateMetricCard('network', `${this.metricsData.network.bandwidth}%`, this.metricsData.network.trend);
        this.updateMetricCard('security', this.metricsData.security.status, this.metricsData.security.trend);
    }

    /**
     * Update specific metric card
     */
    updateMetricCard(type, value, trend) {
        const card = document.querySelector(`[data-metric="${type}"]`);
        if (!card) return;

        const valueElement = card.querySelector('.metric-value');
        const changeElement = card.querySelector('.metric-change');

        if (valueElement) {
            valueElement.textContent = value;
        }

        if (changeElement) {
            const trendValue = Math.abs(trend).toFixed(1);
            const trendIcon = trend > 0 ? '↗' : trend < 0 ? '↘' : '→';
            const trendClass = trend > 0 ? 'positive' : trend < 0 ? 'negative' : 'neutral';
            
            changeElement.textContent = `${trendIcon} ${trendValue}%`;
            changeElement.className = `metric-change ${trendClass}`;
        }
    }

    /**
     * Update charts with new data
     */
    updateCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart && chart.data && chart.data.datasets[0]) {
                // Shift data and add new point
                chart.data.datasets[0].data.shift();
                chart.data.datasets[0].data.push(Math.random() * 100);
                chart.update('none');
            }
        });
    }

    /**
     * Handle view switching
     */
    switchView(viewName) {
        this.currentView = viewName;
        
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.style.display = 'none';
        });

        // Show selected section
        const targetSection = document.querySelector(`[data-section="${viewName}"]`);
        if (targetSection) {
            targetSection.style.display = 'block';
            targetSection.classList.add('animate-fade-in-up');
        }

        this.addNotification(`Vista cambiada a ${viewName}`, 'info');
    }

    /**
     * Update active navigation
     */
    updateActiveNavigation(activeLink) {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        activeLink.classList.add('active');
    }

    /**
     * Handle control changes
     */
    handleControlChange(input) {
        const value = input.value;
        const name = input.name || input.id;
        
        console.log(`Control changed: ${name} = ${value}`);
        
        if (this.socket) {
            this.socket.emit('control_change', { name, value });
        }

        this.addNotification(`Control actualizado: ${name}`, 'info');
    }

    /**
     * Handle viewer controls
     */
    handleViewerControl(button) {
        const action = button.dataset.action;
        
        // Update active state
        button.parentElement.querySelectorAll('.viewer-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        button.classList.add('active');

        // Handle different actions
        switch (action) {
            case 'reset':
                this.resetCameraView();
                break;
            case 'wireframe':
                this.toggleWireframe();
                break;
            case 'lighting':
                this.toggleLighting();
                break;
            case 'fullscreen':
                this.toggleFullscreen();
                break;
        }

        this.addNotification(`Acción del visor: ${action}`, 'info');
    }

    /**
     * Reset camera view
     */
    resetCameraView() {
        if (this.threeScene && this.threeScene.camera) {
            this.threeScene.camera.position.set(10, 10, 10);
            this.threeScene.camera.lookAt(0, 0, 0);
        }
    }

    /**
     * Toggle wireframe mode
     */
    toggleWireframe() {
        if (this.threeScene) {
            this.threeScene.objects.forEach(obj => {
                if (obj.material) {
                    obj.material.wireframe = !obj.material.wireframe;
                }
            });
        }
    }

    /**
     * Toggle lighting
     */
    toggleLighting() {
        if (this.threeScene) {
            this.threeScene.scene.children.forEach(child => {
                if (child instanceof THREE.Light && !(child instanceof THREE.AmbientLight)) {
                    child.visible = !child.visible;
                }
            });
        }
    }

    /**
     * Toggle fullscreen
     */
    toggleFullscreen() {
        const container = document.getElementById('threejs-container');
        if (container) {
            if (document.fullscreenElement) {
                document.exitFullscreen();
            } else {
                container.requestFullscreen();
            }
        }
    }

    /**
     * Handle window resize
     */
    handleResize() {
        if (this.threeScene && this.threeScene.camera && this.threeScene.renderer) {
            const container = document.getElementById('threejs-container');
            if (container) {
                const width = container.clientWidth;
                const height = container.clientHeight;
                
                this.threeScene.camera.aspect = width / height;
                this.threeScene.camera.updateProjectionMatrix();
                this.threeScene.renderer.setSize(width, height);
            }
        }

        // Resize charts
        Object.values(this.charts).forEach(chart => {
            if (chart && chart.resize) {
                chart.resize();
            }
        });
    }

    /**
     * Handle keyboard shortcuts
     */
    handleKeyboardShortcuts(event) {
        if (event.ctrlKey || event.metaKey) {
            switch (event.key) {
                case '1':
                    event.preventDefault();
                    this.switchView('dashboard');
                    break;
                case '2':
                    event.preventDefault();
                    this.switchView('robots');
                    break;
                case '3':
                    event.preventDefault();
                    this.switchView('city');
                    break;
                case 'n':
                    event.preventDefault();
                    this.toggleNotificationPanel();
                    break;
                case 'r':
                    event.preventDefault();
                    this.resetCameraView();
                    break;
            }
        }

        if (event.key === 'Escape') {
            this.closeNotificationPanel();
        }
    }

    /**
     * Notification management
     */
    addNotification(message, type = 'info') {
        const notification = {
            id: Date.now(),
            message,
            type,
            timestamp: new Date().toLocaleTimeString()
        };

        this.notifications.unshift(notification);
        
        // Limit to 50 notifications
        if (this.notifications.length > 50) {
            this.notifications = this.notifications.slice(0, 50);
        }

        this.updateNotificationDisplay();
        this.updateNotificationBadge();
    }

    /**
     * Update notification display
     */
    updateNotificationDisplay() {
        const container = document.querySelector('.notification-list');
        if (!container) return;

        container.innerHTML = this.notifications.map(notification => `
            <div class="notification-item animate-fade-in-up">
                <div class="notification-meta">
                    <span class="notification-type ${notification.type}">${notification.type}</span>
                    <span class="notification-time">${notification.timestamp}</span>
                </div>
                <div class="notification-message">${notification.message}</div>
            </div>
        `).join('');
    }

    /**
     * Update notification badge
     */
    updateNotificationBadge() {
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            const unreadCount = this.notifications.length;
            badge.textContent = unreadCount > 99 ? '99+' : unreadCount;
            badge.style.display = unreadCount > 0 ? 'flex' : 'none';
        }
    }

    /**
     * Toggle notification panel
     */
    toggleNotificationPanel() {
        const panel = document.querySelector('.notification-panel');
        if (panel) {
            panel.classList.toggle('open');
        }
    }

    /**
     * Close notification panel
     */
    closeNotificationPanel() {
        const panel = document.querySelector('.notification-panel');
        if (panel) {
            panel.classList.remove('open');
        }
    }

    /**
     * Generate random notifications for demo
     */
    generateRandomNotification() {
        const messages = [
            { text: 'Robot R-001 completó su tarea de mantenimiento', type: 'success' },
            { text: 'Nuevo proyecto de investigación iniciado', type: 'info' },
            { text: 'Nivel de energía por debajo del 20%', type: 'warning' },
            { text: 'Conexión de red restaurada', type: 'success' },
            { text: 'Análisis de rendimiento completado', type: 'info' },
            { text: 'Sistema de seguridad actualizado', type: 'success' }
        ];

        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        this.addNotification(randomMessage.text, randomMessage.type);
    }

    /**
     * Update connection status
     */
    updateConnectionStatus(connected) {
        const statusIndicator = document.querySelector('.status-indicator');
        const statusDot = document.querySelector('.status-dot');
        const statusText = statusIndicator?.querySelector('span:last-child');

        if (statusIndicator && statusDot && statusText) {
            if (connected) {
                statusIndicator.style.background = 'rgba(74, 222, 128, 0.1)';
                statusIndicator.style.borderColor = 'rgba(74, 222, 128, 0.3)';
                statusDot.style.background = '#4ade80';
                statusText.textContent = 'Conectado';
            } else {
                statusIndicator.style.background = 'rgba(239, 68, 68, 0.1)';
                statusIndicator.style.borderColor = 'rgba(239, 68, 68, 0.3)';
                statusDot.style.background = '#ef4444';
                statusText.textContent = 'Desconectado';
            }
        }
    }

    /**
     * Update metrics from server
     */
    updateMetrics(data) {
        if (data) {
            this.metricsData = { ...this.metricsData, ...data };
            this.updateMetricsDisplay();
        }
    }

    /**
     * Update robot status
     */
    updateRobotStatus(data) {
        console.log('Robot status update:', data);
        // Handle robot-specific updates
    }

    /**
     * Cleanup on page unload
     */
    destroy() {
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }

        if (this.socket) {
            this.socket.disconnect();
        }

        Object.values(this.charts).forEach(chart => {
            if (chart && chart.destroy) {
                chart.destroy();
            }
        });

        if (this.threeScene && this.threeScene.renderer) {
            this.threeScene.renderer.dispose();
        }
    }
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.advancedMetaversoApp = new AdvancedMetaversoApp();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.advancedMetaversoApp) {
        window.advancedMetaversoApp.destroy();
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvancedMetaversoApp;
}