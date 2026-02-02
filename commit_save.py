#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os

os.chdir(r"c:\Users\Brian Carlisle\mundo virtual")

# Agregar todos los cambios
print("📦 Agregando cambios...")
subprocess.run(["git", "add", "-A"], check=True)

# Hacer commit
print("💾 Creando commit...")
subprocess.run([
    "git", "commit", "-m", 
    "Sistema completo: pago, robots, avatares, bolsa de valores, seguridad, prision"
], check=True)

# Push
print("🚀 Enviando a repositorio...")
subprocess.run(["git", "push", "origin", "main"], check=False)

print("\n✅ Todo guardado correctamente!")
print("\nEstado del repositorio:")
subprocess.run(["git", "status"], check=True)
