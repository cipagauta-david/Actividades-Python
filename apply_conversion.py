#!/usr/bin/env python3
"""
Script para aplicar la conversión HTML a Markdown directamente al archivo original
Crea un backup automáticamente antes de modificar el archivo
"""

import re
import sys
import os
from datetime import datetime

def convert_html_to_markdown(content):
    """
    Convierte listas HTML a Markdown de forma simple y directa
    """
    lines = content.split('\n')
    result_lines = []
    in_ol = False
    in_ul = False
    ol_level = 0
    ol_counter = [1]  # Stack de contadores
    ol_type = ['1']   # Stack de tipos de lista
    
    for line in lines:
        stripped = line.strip()
        leading_tabs = len(line) - len(line.lstrip('\t'))
        
        # Detectar apertura de lista ordenada
        ol_match = re.match(r'<ol(?:\s+type="([^"]*)")?>', stripped, re.IGNORECASE)
        if ol_match:
            list_type = ol_match.group(1) if ol_match.group(1) else '1'
            ol_level += 1
            ol_counter.append(1)
            ol_type.append(list_type)
            in_ol = True
            continue
            
        # Detectar apertura de lista desordenada
        if re.match(r'<ul>', stripped, re.IGNORECASE):
            in_ul = True
            continue
            
        # Detectar cierre de lista ordenada
        if re.match(r'</ol>', stripped, re.IGNORECASE):
            if ol_level > 0:
                ol_level -= 1
                ol_counter.pop()
                ol_type.pop()
            if ol_level == 0:
                in_ol = False
            continue
            
        # Detectar cierre de lista desordenada  
        if re.match(r'</ul>', stripped, re.IGNORECASE):
            in_ul = False
            continue
            
        # Convertir elementos de lista
        if stripped.startswith('- '):
            content_text = stripped[2:]  # Remover "- "
            
            if in_ol and ol_level > 0:
                # Lista ordenada
                indent = '\t' * leading_tabs
                list_type = ol_type[-1]
                counter = ol_counter[-1]
                
                if list_type == 'a':
                    marker = chr(ord('a') + counter - 1) + '.'
                elif list_type == 'A':
                    marker = chr(ord('A') + counter - 1) + '.'
                elif list_type == 'i':
                    marker = int_to_roman_lower(counter) + '.'
                elif list_type == 'I':
                    marker = int_to_roman_upper(counter) + '.'
                else:
                    marker = str(counter) + '.'
                
                result_lines.append(f"{indent}{marker} {content_text}")
                ol_counter[-1] += 1
                
            elif in_ul:
                # Lista desordenada
                indent = '\t' * leading_tabs
                result_lines.append(f"{indent}- {content_text}")
            else:
                # No está en una lista, mantener como está
                result_lines.append(line)
        else:
            # Línea que no es elemento de lista
            if stripped:  # Solo añadir líneas no vacías
                result_lines.append(line)
            elif not result_lines or result_lines[-1].strip():  # Evitar líneas vacías duplicadas
                result_lines.append('')
    
    return '\n'.join(result_lines)

def int_to_roman_lower(num):
    """Convierte número a romano minúsculas"""
    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ['m', 'cm', 'd', 'cd', 'c', 'xc', 'l', 'xl', 'x', 'ix', 'v', 'iv', 'i']
    result = ''
    for value, numeral in zip(values, numerals):
        count = num // value
        result += numeral * count
        num -= value * count
    return result

def int_to_roman_upper(num):
    """Convierte número a romano mayúsculas"""
    return int_to_roman_lower(num).upper()

def create_backup(filename):
    """Crea un backup del archivo original"""
    if not os.path.exists(filename):
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{filename}.backup_{timestamp}"
    
    try:
        with open(filename, 'r', encoding='utf-8') as source:
            content = source.read()
        with open(backup_name, 'w', encoding='utf-8') as backup:
            backup.write(content)
        return backup_name
    except Exception as e:
        print(f"Error creando backup: {e}")
        return None

def apply_conversion(filename, create_backup_flag=True):
    """Aplica la conversión al archivo original"""
    if not os.path.exists(filename):
        print(f"Error: El archivo {filename} no existe")
        return False
    
    # Crear backup
    backup_name = None
    if create_backup_flag:
        backup_name = create_backup(filename)
        if backup_name:
            print(f"Backup creado: {backup_name}")
        else:
            print("Advertencia: No se pudo crear el backup")
    
    # Leer archivo original
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(filename, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"Error leyendo el archivo: {e}")
            return False
    
    # Convertir contenido
    converted = convert_html_to_markdown(content)
    
    # Escribir archivo convertido
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(converted)
        print(f"Conversión aplicada exitosamente a: {filename}")
        return True
    except Exception as e:
        print(f"Error escribiendo el archivo convertido: {e}")
        # Si hay backup, intentar restaurar
        if backup_name and os.path.exists(backup_name):
            try:
                with open(backup_name, 'r', encoding='utf-8') as backup:
                    original_content = backup.read()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                print(f"Archivo restaurado desde backup: {backup_name}")
            except:
                print("No se pudo restaurar el archivo desde el backup")
        return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python apply_conversion.py <archivo.md> [--no-backup]")
        print()
        print("Opciones:")
        print("  --no-backup    No crear backup del archivo original")
        print()
        print("Este script modifica el archivo original aplicando la conversión HTML a Markdown.")
        print("Por defecto crea un backup con timestamp antes de modificar el archivo.")
        return
    
    filename = sys.argv[1]
    create_backup_flag = '--no-backup' not in sys.argv
    
    print(f"Aplicando conversión a: {filename}")
    if create_backup_flag:
        print("Se creará un backup del archivo original")
    else:
        print("NO se creará backup del archivo original")
    
    # Confirmación
    if create_backup_flag:
        proceed = input("¿Continuar? (y/N): ").lower().strip()
    else:
        proceed = input("¿Continuar SIN BACKUP? (y/N): ").lower().strip()
    
    if proceed not in ['y', 'yes', 'sí', 'si']:
        print("Operación cancelada")
        return
    
    success = apply_conversion(filename, create_backup_flag)
    if success:
        print("¡Conversión completada exitosamente!")
    else:
        print("La conversión falló")

if __name__ == "__main__":
    main()