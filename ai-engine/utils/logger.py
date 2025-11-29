"""
Configuración de logging para el sistema de IA
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configurar logger para un módulo específico"""
    
    # Crear directorio de logs si no existe
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo
    today = datetime.now().strftime("%Y%m%d")
    file_handler = logging.FileHandler(log_dir / f"ai_engine_{today}.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger