import React from 'react';

interface LoadingScreenProps {
  progress: number;
}

const LoadingScreen: React.FC<LoadingScreenProps> = ({ progress }) => {
  return (
    <div className="loading-screen">
      <div className="loading-spinner"></div>
      <div className="loading-text">Cargando Ciudad Robot...</div>
      <div className="loading-progress">
        <div className="loading-bar" style={{ width: `${progress}%` }}></div>
      </div>
      <div style={{ marginTop: '10px', fontSize: '0.9rem', opacity: 0.8 }}>
        {progress.toFixed(0)}%
      </div>
    </div>
  );
};

export default LoadingScreen;