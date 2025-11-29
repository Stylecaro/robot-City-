/* ==========================================
   METAVERSO APP - ADVANCED JAVASCRIPT
   ========================================== */

class MetaversoApp {
    constructor() {
        this.isLoading = true;
        this.currentSection = 'dashboard';
        this.chartInstances = {};
        this.activityTimer = null;
        this.notificationPanel = null;
        this.threejsScene = null;
        this.webSocket = null;
        
        // Initialize the application
        this.init();
    }

    async init() {
        try {
            // Show splash screen and load components
            await this.loadApplication();
            
            // Setup event listeners
            this.setupEventListeners();
            
            // Initialize components
            this.initializeCharts();
            this.initializeActivityFeed();
            this.initializeNotifications();
            this.initialize3DViewer();
            this.initializeWebSocket();
            
            // Hide splash screen and show main app
            this.hideSplashScreen();
            
            console.log('✅ Metaverso App initialized successfully');
        } catch (error) {
            console.error('❌ Error initializing Metaverso App:', error);
        }
    }

    async loadApplication() {
        const loadingSteps = [
            { text: 'Inicializando sistemas...', duration: 800 },
            { text: 'Conectando con Unity Hub...', duration: 1000 },
            { text: 'Cargando datos del metaverso...', duration: 700 },
            { text: 'Preparando interfaz 3D...', duration: 900 },
            { text: 'Estableciendo conexiones...', duration: 600 },
            { text: 'Finalizando carga...', duration: 500 }
        ];

        const progressBar = document.getElementById('loading-progress');
        const loadingText = document.getElementById('loading-text');
        
        let totalProgress = 0;
        const stepProgress = 100 / loadingSteps.length;

        for (const step of loadingSteps) {
            loadingText.textContent = step.text;
            totalProgress += stepProgress;
            progressBar.style.width = `${totalProgress}%`;
            
            await this.delay(step.duration);
        }
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    hideSplashScreen() {
        const splashScreen = document.getElementById('splash-screen');
        const mainApp = document.getElementById('main-app');
        
        setTimeout(() => {
            splashScreen.classList.add('hidden');
            mainApp.classList.remove('hidden');
            this.isLoading = false;
        }, 500);
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const section = e.currentTarget.dataset.section;
                this.navigateToSection(section);
            });
        });

        // Header buttons
        document.getElementById('notifications-btn')?.addEventListener('click', () => {
            this.toggleNotificationPanel();
        });

        document.getElementById('settings-btn')?.addEventListener('click', () => {
            this.openSettings();
        });

        document.getElementById('user-btn')?.addEventListener('click', () => {
            this.openUserProfile();
        });

        // Dashboard actions
        document.getElementById('refresh-btn')?.addEventListener('click', () => {
            this.refreshDashboard();
        });

        document.getElementById('export-btn')?.addEventListener('click', () => {
            this.exportData();
        });

        // Unity Hub actions
        document.getElementById('launch-unity')?.addEventListener('click', () => {
            this.launchUnityHub();
        });

        document.getElementById('create-project')?.addEventListener('click', () => {
            this.createUnityProject();
        });

        document.getElementById('import-project')?.addEventListener('click', () => {
            this.importUnityProject();
        });

        // City viewer controls
        document.getElementById('zoom-slider')?.addEventListener('input', (e) => {
            this.updateCityZoom(e.target.value);
        });

        document.getElementById('rotation-slider')?.addEventListener('input', (e) => {
            this.updateCityRotation(e.target.value);
        });

        document.getElementById('reset-view')?.addEventListener('click', () => {
            this.resetCityView();
        });

        document.getElementById('toggle-view')?.addEventListener('click', () => {
            this.toggleCityView();
        });

        // Close notification panel
        document.getElementById('close-notifications')?.addEventListener('click', () => {
            this.closeNotificationPanel();
        });

        // Activity filter
        document.getElementById('activity-filter')?.addEventListener('click', () => {
            this.toggleActivityFilter();
        });
    }

    navigateToSection(sectionName) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionName}"]`)?.classList.add('active');

        // Update content sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(`${sectionName}-section`)?.classList.add('active');

        this.currentSection = sectionName;

        // Section-specific actions
        if (sectionName === 'city-view') {
            this.refreshCityViewer();
        } else if (sectionName === 'dashboard') {
            this.refreshDashboard();
        }
    }

    initializeCharts() {
        // Manufacturing Chart
        this.createSparklineChart('manufacturing-chart', [85, 90, 87, 92, 95, 93, 95]);
        
        // Research Chart
        this.createSparklineChart('research-chart', [80, 82, 85, 84, 87, 86, 87]);
        
        // Security Chart
        this.createSparklineChart('security-chart', [98, 99, 97, 99, 99, 98, 99]);
        
        // AI Chart
        this.createSparklineChart('ai-chart', [78, 82, 85, 88, 90, 91, 92]);
    }

    createSparklineChart(canvasId, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['', '', '', '', '', '', ''],
                datasets: [{
                    data: data,
                    borderColor: '#00d4ff',
                    backgroundColor: 'rgba(0, 212, 255, 0.1)',
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
                scales: {
                    x: { display: false },
                    y: { display: false }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                interaction: { intersect: false }
            }
        });

        this.chartInstances[canvasId] = chart;
    }

    initializeActivityFeed() {
        const activities = [
            {
                icon: 'fas fa-robot',
                iconColor: '#00d4ff',
                title: 'Robot XR-7 completó manufactura de componente',
                time: 'Hace 2 minutos',
                type: 'manufacturing'
            },
            {
                icon: 'fas fa-flask',
                iconColor: '#4ecdc4',
                title: 'Experimento de materiales iniciado',
                time: 'Hace 5 minutos',
                type: 'research'
            },
            {
                icon: 'fas fa-shield-alt',
                iconColor: '#ff4757',
                title: 'Escaneo de seguridad completado',
                time: 'Hace 8 minutos',
                type: 'security'
            },
            {
                icon: 'fas fa-brain',
                iconColor: '#a55eea',
                title: 'IA procesó 1,247 nuevos datos',
                time: 'Hace 12 minutos',
                type: 'ai'
            },
            {
                icon: 'fas fa-cog',
                iconColor: '#ff6b35',
                title: 'Mantenimiento preventivo programado',
                time: 'Hace 15 minutos',
                type: 'system'
            }
        ];

        this.populateActivityFeed(activities);
        this.startActivityUpdates();
    }

    populateActivityFeed(activities) {
        const feedContainer = document.getElementById('activity-feed');
        if (!feedContainer) return;

        feedContainer.innerHTML = activities.map(activity => `
            <div class="activity-item fade-in">
                <div class="activity-icon" style="background: ${activity.iconColor}20; color: ${activity.iconColor};">
                    <i class="${activity.icon}"></i>
                </div>
                <div class="activity-content">
                    <div class="activity-title">${activity.title}</div>
                    <div class="activity-time">${activity.time}</div>
                </div>
            </div>
        `).join('');
    }

    startActivityUpdates() {
        if (this.activityTimer) clearInterval(this.activityTimer);
        
        this.activityTimer = setInterval(() => {
            this.updateSystemStats();
            this.updateMetricValues();
        }, 30000); // Update every 30 seconds
    }

    updateSystemStats() {
        const stats = {
            'active-robots': Math.floor(Math.random() * 20) + 240,
            'research-projects': Math.floor(Math.random() * 5) + 20,
            'production-lines': Math.floor(Math.random() * 3) + 10,
            'running-simulations': Math.floor(Math.random() * 5) + 5,
            'threats-detected': Math.random() > 0.9 ? 1 : 0,
            'energy-efficiency': (Math.random() * 5 + 90).toFixed(1) + '%'
        };

        Object.entries(stats).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
                element.style.animation = 'pulse 0.5s ease-in-out';
                setTimeout(() => {
                    element.style.animation = '';
                }, 500);
            }
        });
    }

    updateMetricValues() {
        const metrics = {
            'manufacturing-value': Math.floor(Math.random() * 10) + 90 + '%',
            'research-value': Math.floor(Math.random() * 10) + 80 + '%',
            'security-value': Math.floor(Math.random() * 3) + 97 + '%',
            'ai-value': Math.floor(Math.random() * 10) + 85 + '%'
        };

        Object.entries(metrics).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }

    initializeNotifications() {
        const notifications = [
            {
                title: 'Sistema actualizado',
                content: 'La versión 2.0 del metaverso ha sido instalada correctamente.',
                time: 'Hace 1 hora',
                type: 'success'
            },
            {
                title: 'Mantenimiento programado',
                content: 'El mantenimiento del servidor está programado para mañana a las 02:00.',
                time: 'Hace 3 horas',
                type: 'warning'
            },
            {
                title: 'Nuevo robot añadido',
                content: 'Robot XR-8 ha sido integrado exitosamente al sistema.',
                time: 'Hace 5 horas',
                type: 'info'
            }
        ];

        this.populateNotifications(notifications);
    }

    populateNotifications(notifications) {
        const notificationList = document.getElementById('notification-list');
        if (!notificationList) return;

        notificationList.innerHTML = notifications.map(notification => `
            <div class="notification-item">
                <div class="notification-header">
                    <div class="notification-title">${notification.title}</div>
                    <div class="notification-time">${notification.time}</div>
                </div>
                <div class="notification-content">${notification.content}</div>
            </div>
        `).join('');
    }

    initialize3DViewer() {
        const container = document.getElementById('city-viewer');
        if (!container || typeof THREE === 'undefined') return;

        try {
            // Scene setup
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0f0f23);

            // Camera
            const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / container.offsetHeight, 0.1, 1000);
            camera.position.set(0, 10, 20);

            // Renderer
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(container.offsetWidth, container.offsetHeight);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            // Lighting
            const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
            scene.add(ambientLight);

            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(10, 10, 5);
            directionalLight.castShadow = true;
            scene.add(directionalLight);

            // Create simple city buildings
            this.createCityBuildings(scene);

            // Animation loop
            const animate = () => {
                requestAnimationFrame(animate);
                scene.rotation.y += 0.001;
                renderer.render(scene, camera);
            };

            animate();
            this.threejsScene = { scene, camera, renderer };

            // Handle window resize
            window.addEventListener('resize', () => {
                if (container.offsetWidth > 0) {
                    camera.aspect = container.offsetWidth / container.offsetHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(container.offsetWidth, container.offsetHeight);
                }
            });

        } catch (error) {
            console.error('Error initializing 3D viewer:', error);
            container.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100%; color: rgba(255,255,255,0.6);">Vista 3D no disponible</div>';
        }
    }

    createCityBuildings(scene) {
        const buildings = [];
        const colors = [0x00d4ff, 0x4ecdc4, 0xff6b35, 0xa55eea, 0xff4757];

        for (let i = 0; i < 20; i++) {
            const height = Math.random() * 5 + 2;
            const geometry = new THREE.BoxGeometry(1, height, 1);
            const material = new THREE.MeshLambertMaterial({ 
                color: colors[Math.floor(Math.random() * colors.length)],
                transparent: true,
                opacity: 0.8
            });
            
            const building = new THREE.Mesh(geometry, material);
            building.position.set(
                (Math.random() - 0.5) * 20,
                height / 2,
                (Math.random() - 0.5) * 20
            );
            building.castShadow = true;
            building.receiveShadow = true;
            
            scene.add(building);
            buildings.push(building);
        }

        // Ground plane
        const groundGeometry = new THREE.PlaneGeometry(50, 50);
        const groundMaterial = new THREE.MeshLambertMaterial({ color: 0x1a1a2e });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        scene.add(ground);
    }

    initializeWebSocket() {
        // Simulated WebSocket connection for real-time data
        console.log('🔗 Simulando conexión WebSocket...');
        
        // In a real implementation, you would connect to your backend
        // this.webSocket = new WebSocket('ws://localhost:8080');
        
        // Simulate real-time updates
        setInterval(() => {
            this.simulateRealtimeData();
        }, 5000);
    }

    simulateRealtimeData() {
        if (this.currentSection === 'dashboard') {
            // Simulate new activity
            const activities = [
                'Robot completó tarea de manufactura',
                'Nuevo experimento iniciado',
                'Análisis de datos completado',
                'Sistema de seguridad actualizado',
                'IA procesó nuevos patrones'
            ];
            
            const randomActivity = activities[Math.floor(Math.random() * activities.length)];
            this.addNewActivity(randomActivity);
        }
    }

    addNewActivity(activityText) {
        const feedContainer = document.getElementById('activity-feed');
        if (!feedContainer) return;

        const newActivity = document.createElement('div');
        newActivity.className = 'activity-item fade-in';
        newActivity.innerHTML = `
            <div class="activity-icon" style="background: #00d4ff20; color: #00d4ff;">
                <i class="fas fa-robot"></i>
            </div>
            <div class="activity-content">
                <div class="activity-title">${activityText}</div>
                <div class="activity-time">Ahora mismo</div>
            </div>
        `;

        feedContainer.insertBefore(newActivity, feedContainer.firstChild);

        // Remove oldest activity if more than 10
        const activities = feedContainer.querySelectorAll('.activity-item');
        if (activities.length > 10) {
            activities[activities.length - 1].remove();
        }
    }

    // Event handler methods
    toggleNotificationPanel() {
        const panel = document.getElementById('notification-panel');
        if (panel) {
            panel.classList.toggle('hidden');
        }
    }

    closeNotificationPanel() {
        const panel = document.getElementById('notification-panel');
        if (panel) {
            panel.classList.add('hidden');
        }
    }

    openSettings() {
        alert('Configuración - Próximamente disponible');
    }

    openUserProfile() {
        alert('Perfil de Usuario - Próximamente disponible');
    }

    refreshDashboard() {
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            const icon = refreshBtn.querySelector('i');
            icon.style.animation = 'spin 1s linear infinite';
            
            setTimeout(() => {
                icon.style.animation = '';
                this.updateSystemStats();
                this.updateMetricValues();
            }, 1000);
        }
    }

    exportData() {
        const data = {
            timestamp: new Date().toISOString(),
            metrics: {
                manufacturing: document.getElementById('manufacturing-value')?.textContent,
                research: document.getElementById('research-value')?.textContent,
                security: document.getElementById('security-value')?.textContent,
                ai: document.getElementById('ai-value')?.textContent
            },
            stats: {
                activeRobots: document.getElementById('active-robots')?.textContent,
                researchProjects: document.getElementById('research-projects')?.textContent,
                productionLines: document.getElementById('production-lines')?.textContent
            }
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `metaverso-data-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    async launchUnityHub() {
        const btn = document.getElementById('launch-unity');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Abriendo...';
            
            try {
                // Simulate Unity Hub launch
                await this.delay(2000);
                
                // Update Unity status
                document.getElementById('unity-status-text').textContent = 'Conectado';
                document.getElementById('unity-connection').textContent = 'Online';
                document.getElementById('unity-connection').className = 'info-value online';
                
                btn.innerHTML = '<i class="fab fa-unity"></i> Unity Hub Activo';
                
                setTimeout(() => {
                    btn.disabled = false;
                    btn.innerHTML = '<i class="fab fa-unity"></i> Abrir Unity Hub';
                }, 3000);
                
            } catch (error) {
                console.error('Error launching Unity Hub:', error);
                btn.disabled = false;
                btn.innerHTML = '<i class="fab fa-unity"></i> Error - Reintentar';
            }
        }
    }

    createUnityProject() {
        alert('Crear Nuevo Proyecto Unity - Próximamente disponible');
    }

    importUnityProject() {
        alert('Importar Proyecto Unity - Próximamente disponible');
    }

    updateCityZoom(value) {
        if (this.threejsScene) {
            const camera = this.threejsScene.camera;
            camera.position.z = 30 - (value * 2);
        }
    }

    updateCityRotation(value) {
        if (this.threejsScene) {
            const scene = this.threejsScene.scene;
            scene.rotation.y = (value * Math.PI) / 180;
        }
    }

    resetCityView() {
        if (this.threejsScene) {
            const camera = this.threejsScene.camera;
            const scene = this.threejsScene.scene;
            
            camera.position.set(0, 10, 20);
            scene.rotation.y = 0;
            
            // Reset sliders
            document.getElementById('zoom-slider').value = 5;
            document.getElementById('rotation-slider').value = 0;
        }
    }

    toggleCityView() {
        const btn = document.getElementById('toggle-view');
        if (btn && this.threejsScene) {
            const camera = this.threejsScene.camera;
            const isAerial = btn.textContent.includes('Aérea');
            
            if (isAerial) {
                // Switch to street view
                camera.position.set(0, 2, 10);
                btn.innerHTML = '<i class="fas fa-eye"></i> Vista Aérea';
            } else {
                // Switch to aerial view
                camera.position.set(0, 20, 20);
                btn.innerHTML = '<i class="fas fa-eye"></i> Vista Calle';
            }
        }
    }

    refreshCityViewer() {
        if (this.threejsScene) {
            // Refresh 3D scene if needed
            console.log('🔄 Refreshing city viewer...');
        }
    }

    toggleActivityFilter() {
        alert('Filtro de Actividades - Próximamente disponible');
    }
}

// CSS Animation for spinning
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.metaversoApp = new MetaversoApp();
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MetaversoApp;
}