#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de validación y corrección de errores del proyecto
Versión simplificada sin dependencias externas
"""

import os
import json
import re
from pathlib import Path

def validate_project():
    """Valida el proyecto y muestra estado de errores"""
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║               🔍 VALIDACIÓN DEL PROYECTO 📊                 ║") 
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    project_root = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Contadores
    files_checked = 0
    errors_found = 0
    warnings = 0
    fixes_applied = 0
    
    # Validar archivos JSX/JS
    print("📁 VALIDANDO ARCHIVOS FRONTEND (JSX/JS):")
    for jsx_file in project_root.rglob("*.jsx"):
        if jsx_file.exists():
            files_checked += 1
            result = validate_jsx_file(jsx_file)
            if result['errors']:
                errors_found += result['errors']
                print(f"   ❌ {jsx_file.name}: {result['errors']} errores")
            else:
                print(f"   ✅ {jsx_file.name}: Sin errores")
            
            if result['warnings']:
                warnings += result['warnings']
                print(f"      ⚠️  {result['warnings']} advertencias")
    
    # Validar archivos HTML
    print("\n📄 VALIDANDO ARCHIVOS HTML:")
    for html_file in project_root.rglob("*.html"):
        if html_file.exists():
            files_checked += 1
            result = validate_html_file(html_file)
            if result['errors']:
                errors_found += result['errors']
                print(f"   ❌ {html_file.name}: {result['errors']} errores")
            else:
                print(f"   ✅ {html_file.name}: Sin errores críticos")
                
            if result['warnings']:
                warnings += result['warnings']
                print(f"      ⚠️  {result['warnings']} advertencias")
    
    # Validar archivos Python
    print("\n🐍 VALIDANDO ARCHIVOS PYTHON:")
    for py_file in project_root.rglob("*.py"):
        if py_file.exists() and py_file.name != __file__.split('/')[-1]:
            files_checked += 1
            result = validate_python_file(py_file)
            if result['errors']:
                errors_found += result['errors']
                print(f"   ❌ {py_file.name}: {result['errors']} errores")
            else:
                print(f"   ✅ {py_file.name}: Sin errores de sintaxis")
    
    # Validar archivos CSS
    print("\n🎨 VALIDANDO ARCHIVOS CSS:")
    for css_file in project_root.rglob("*.css"):
        if css_file.exists():
            files_checked += 1
            result = validate_css_file(css_file)
            if result['errors']:
                errors_found += result['errors']
                print(f"   ❌ {css_file.name}: {result['errors']} errores")
            else:
                print(f"   ✅ {css_file.name}: Formato válido")
                
            if result['warnings']:
                warnings += result['warnings']
                print(f"      ⚠️  {result['warnings']} advertencias de compatibilidad")
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE VALIDACIÓN:")
    print(f"   📁 Archivos verificados: {files_checked}")
    print(f"   ❌ Errores encontrados: {errors_found}")
    print(f"   ⚠️  Advertencias: {warnings}")
    
    if errors_found == 0:
        print("\n🎉 ¡EXCELENTE! No se encontraron errores críticos")
        print("✨ El proyecto está en buen estado")
    else:
        print(f"\n⚠️  Se encontraron {errors_found} errores que necesitan atención")
        print("🔧 Revisa los archivos marcados con ❌")
    
    if warnings > 0:
        print(f"💡 {warnings} advertencias menores detectadas")
        print("📝 Considera revisar las sugerencias marcadas con ⚠️")
    
    print("\n🚀 Estado general del proyecto: ", end="")
    if errors_found == 0 and warnings < 5:
        print("🟢 EXCELENTE")
    elif errors_found == 0:
        print("🟡 BUENO")
    elif errors_found < 5:
        print("🟠 NECESITA MEJORAS")
    else:
        print("🔴 REQUIERE ATENCIÓN")

def validate_jsx_file(file_path):
    """Valida archivo JSX/JS"""
    result = {'errors': 0, 'warnings': 0}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que no empiece con comentarios Python
        if content.strip().startswith('"""'):
            result['errors'] += 1
        
        # Verificar imports básicos
        if 'useState' in content and 'import React' not in content:
            result['warnings'] += 1
        
        # Verificar componentes
        if file_path.suffix == '.jsx':
            # Buscar componentes que no empiecen con mayúscula
            components = re.findall(r'const\s+([a-z][a-zA-Z0-9_]*)\s*=\s*\(', content)
            if components:
                result['warnings'] += len(components)
        
    except Exception:
        result['errors'] += 1
    
    return result

def validate_html_file(file_path):
    """Valida archivo HTML"""
    result = {'errors': 0, 'warnings': 0}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar elementos básicos
        if '<html>' in content and 'lang=' not in content:
            result['warnings'] += 1
        
        if 'charset' not in content:
            result['warnings'] += 1
            
        if 'viewport' not in content:
            result['warnings'] += 1
        
        # Verificar estilos inline
        inline_styles = len(re.findall(r'style="[^"]*"', content))
        if inline_styles > 2:
            result['warnings'] += 1
            
    except Exception:
        result['errors'] += 1
    
    return result

def validate_python_file(file_path):
    """Valida archivo Python"""
    result = {'errors': 0, 'warnings': 0}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compilar para verificar sintaxis
        compile(content, str(file_path), 'exec')
        
        # Verificar imports duplicados
        import_lines = [line for line in content.split('\n') if line.strip().startswith(('import ', 'from '))]
        unique_imports = set(import_lines)
        if len(import_lines) != len(unique_imports):
            result['warnings'] += 1
            
    except SyntaxError:
        result['errors'] += 1
    except Exception:
        result['warnings'] += 1
    
    return result

def validate_css_file(file_path):
    """Valida archivo CSS"""
    result = {'errors': 0, 'warnings': 0}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar llaves balanceadas
        open_braces = content.count('{')
        close_braces = content.count('}')
        
        if open_braces != close_braces:
            result['errors'] += 1
        
        # Verificar propiedades con prefijos webkit sin estándar
        webkit_props = re.findall(r'-webkit-([a-z-]+):', content)
        for prop in webkit_props:
            standard_prop = prop.replace('-webkit-', '')
            if f'{standard_prop}:' not in content:
                result['warnings'] += 1
                
    except Exception:
        result['errors'] += 1
    
    return result

if __name__ == "__main__":
    validate_project()