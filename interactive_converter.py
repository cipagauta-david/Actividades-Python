#!/usr/bin/env python3
"""
Script interactivo para convertir fragmentos de texto HTML a Markdown
Útil para conversiones rápidas de partes específicas del documento
"""

import re

def convert_fragment(text):
    """Convierte un fragmento de texto HTML a Markdown"""
    lines = text.strip().split('\n')
    result_lines = []
    in_ol = False
    in_ul = False
    ol_level = 0
    ol_counter = [1]
    ol_type = ['1']
    
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
            if stripped or (result_lines and not result_lines[-1].strip()):
                result_lines.append(line)
    
    return '\n'.join(result_lines)

def main():
    print("=== Convertidor HTML a Markdown (modo interactivo) ===")
    print("Pega tu texto HTML y presiona Enter dos veces para convertir.")
    print("Escribe 'quit' o 'exit' para salir.\n")
    
    while True:
        print("Texto HTML a convertir:")
        lines = []
        
        try:
            while True:
                line = input()
                if line.strip().lower() in ['quit', 'exit']:
                    print("¡Hasta luego!")
                    return
                if line == '' and lines and lines[-1] == '':
                    break  # Dos líneas vacías = fin de entrada
                lines.append(line)
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            return
        except EOFError:
            print("\n¡Hasta luego!")
            return
        
        if not lines or all(line.strip() == '' for line in lines):
            continue
            
        # Remover la última línea vacía si existe
        if lines and lines[-1] == '':
            lines = lines[:-1]
            
        text = '\n'.join(lines)
        converted = convert_fragment(text)
        
        print("\n--- Resultado convertido ---")
        print(converted)
        print("--- Fin del resultado ---\n")

if __name__ == "__main__":
    main()