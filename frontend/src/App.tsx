import React, { useEffect, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { Suspense } from 'react';
import CityScene from './components/3D/CityScene';
import UIOverlay from './components/UI/UIOverlay';
import SystemMonitor from './components/UI/SystemMonitor';
import ControlPanel from './components/UI/ControlPanel';
import LoadingScreen from './components/UI/LoadingScreen';
import { SocketProvider } from './hooks/useSocket';
import { AppStateProvider } from './store/AppStore';

declare global {
  interface Window {
    hideLoadingScreen?: () => void;
  }
}

const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [loadingProgress, setLoadingProgress] = useState(0);

  useEffect(() => {
    // Simular carga de recursos
    const loadResources = async () => {
      const steps = [
        'Conectando con IA...',
        'Cargando robots...',
        'Inicializando ciudad...',
        'Configurando avatares...',
        'Estableciendo conexión...',
        'Sistema listo!'
      ];

      for (let i = 0; i < steps.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 500));
        setLoadingProgress((i + 1) / steps.length * 100);
      }

      setIsLoading(false);
    };

    loadResources();
  }, []);

  if (isLoading) {
    return <LoadingScreen progress={loadingProgress} />;
  }

  return (
    <AppStateProvider>
      <SocketProvider>
        <div className="w-full h-full relative">
          {/* Escena 3D principal */}
          <div className="canvas-container">
            <Canvas
              camera={{ 
                position: [10, 15, 10], 
                fov: 60,
                near: 0.1,
                far: 1000
              }}
              shadows
              gl={{ antialias: true, alpha: false }}
              onCreated={({ gl }) => {
                gl.setClearColor('#87CEEB'); // Color de cielo
                gl.shadowMap.enabled = true;
                gl.shadowMap.type = 2; // PCFSoftShadowMap
              }}
            >
              <Suspense fallback={<LoadingScreen progress={90} />}>
                <CityScene />
              </Suspense>
            </Canvas>
          </div>

          {/* UI Overlay */}
          <UIOverlay>
            <SystemMonitor />
            <ControlPanel />
          </UIOverlay>
        </div>
      </SocketProvider>
    </AppStateProvider>
  );
};

export default App;