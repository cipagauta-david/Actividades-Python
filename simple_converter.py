#!/usr/bin/env python3
"""
Script simple para convertir listas HTML específicas a Markdown
Enfocado en los patrones encontrados en README.md
"""

import re
import sys

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
                indent = '\t' * (leading_tabs)
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

def process_file(filename):
    """Procesa un archivo y convierte las listas HTML a Markdown"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin-1') as f:
            content = f.read()
    
    converted = convert_html_to_markdown(content)
    
    # Guardar el archivo convertido
    output_filename = filename.replace('.md', '_converted.md')
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(converted)
    
    print(f"Archivo convertido guardado como: {output_filename}")
    
    return converted

def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python simple_converter.py <archivo.md>")
        print("  python simple_converter.py - (para leer desde stdin)")
        return
    
    if sys.argv[1] == '-':
        # Leer desde stdin
        content = sys.stdin.read()
        converted = convert_html_to_markdown(content)
        print(converted)
    else:
        # Procesar archivo
        process_file(sys.argv[1])

if __name__ == "__main__":
    main()