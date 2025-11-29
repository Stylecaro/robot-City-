import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

// Ocultar pantalla de carga después de que React se monte
setTimeout(() => {
  if (window.hideLoadingScreen) {
    window.hideLoadingScreen();
  }
}, 1000);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)