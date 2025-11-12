#!/usr/bin/env python3
"""
Script para convertir listas HTML a Markdown
Convierte <ol>, <ul> y listas anidadas a formato Markdown apropiado
"""

import re
import sys
from typing import List, Tuple

class HTMLToMarkdownConverter:
    def __init__(self):
        # Patrones para diferentes tipos de listas
        self.ol_pattern = re.compile(r'<ol(?:\s+type="([^"]*)")?>', re.IGNORECASE)
        self.ul_pattern = re.compile(r'<ul>', re.IGNORECASE)
        self.ol_close_pattern = re.compile(r'</ol>', re.IGNORECASE)
        self.ul_close_pattern = re.compile(r'</ul>', re.IGNORECASE)
        
        # Stack para manejar listas anidadas
        self.list_stack = []
        
        # Contadores para diferentes tipos de numeración
        self.counters = {}

    def get_list_marker(self, list_type: str, list_subtype: str, level: int, index: int) -> str:
        """
        Genera el marcador apropiado para el elemento de lista
        
        Args:
            list_type: 'ol' o 'ul'
            list_subtype: tipo de lista ordenada ('a', 'i', etc.)
            level: nivel de anidamiento
            index: índice del elemento en la lista
        """
        indent = "\t" * level
        
        if list_type == 'ul':
            return f"{indent}-"
        else:  # ol
            if list_subtype == 'a':
                # Lista alfabética minúscula
                letter = chr(ord('a') + index)
                return f"{indent}{letter}."
            elif list_subtype == 'A':
                # Lista alfabética mayúscula
                letter = chr(ord('A') + index)
                return f"{indent}{letter}."
            elif list_subtype == 'i':
                # Números romanos minúsculas
                roman = self.int_to_roman(index + 1).lower()
                return f"{indent}{roman}."
            elif list_subtype == 'I':
                # Números romanos mayúsculas
                roman = self.int_to_roman(index + 1)
                return f"{indent}{roman}."
            else:
                # Lista numérica normal
                return f"{indent}{index + 1}."

    def int_to_roman(self, num: int) -> str:
        """Convierte un número a romano"""
        values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        numerals = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
        result = ''
        for value, numeral in zip(values, numerals):
            count = num // value
            result += numeral * count
            num -= value * count
        return result

    def extract_list_content(self, content: str, start_pos: int) -> Tuple[str, int]:
        """
        Extrae el contenido de una lista desde la posición inicial
        hasta encontrar su tag de cierre correspondiente
        """
        tag_stack = 0
        pos = start_pos
        
        # Encontrar el tipo de lista
        if content[start_pos:start_pos+3].lower() == '<ol':
            list_tag = 'ol'
            close_tag = '</ol>'
        else:
            list_tag = 'ul'
            close_tag = '</ul>'
        
        # Buscar el final de la lista considerando anidamiento
        while pos < len(content):
            if content[pos:pos+len(f'<{list_tag}')].lower() == f'<{list_tag}':
                tag_stack += 1
            elif content[pos:pos+len(close_tag)].lower() == close_tag.lower():
                tag_stack -= 1
                if tag_stack == 0:
                    return content[start_pos:pos + len(close_tag)], pos + len(close_tag)
            pos += 1
        
        return content[start_pos:], len(content)

    def convert_list_items(self, content: str) -> str:
        """Convierte elementos de lista HTML a Markdown"""
        lines = content.split('\n')
        converted_lines = []
        current_list_level = 0
        item_counters = [0]  # Stack de contadores para cada nivel
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Detectar apertura de lista
            ol_match = self.ol_pattern.match(line)
            ul_match = self.ul_pattern.match(line)
            
            if ol_match or ul_match:
                list_type = 'ol' if ol_match else 'ul'
                list_subtype = ol_match.group(1) if ol_match else None
                
                self.list_stack.append({
                    'type': list_type,
                    'subtype': list_subtype,
                    'level': current_list_level
                })
                
                current_list_level += 1
                item_counters.append(0)
                i += 1
                continue
                
            # Detectar cierre de lista
            elif self.ol_close_pattern.match(line) or self.ul_close_pattern.match(line):
                if self.list_stack:
                    self.list_stack.pop()
                    current_list_level -= 1
                    if item_counters:
                        item_counters.pop()
                i += 1
                continue
                
            # Detectar elementos de lista (líneas que empiezan con -)
            elif line.startswith('-') and self.list_stack:
                current_list = self.list_stack[-1]
                
                # Obtener el contenido del elemento
                content_text = line[1:].strip()
                
                # Generar el marcador apropiado
                marker = self.get_list_marker(
                    current_list['type'],
                    current_list['subtype'],
                    current_list['level'],
                    item_counters[-1]
                )
                
                converted_lines.append(f"{marker} {content_text}")
                item_counters[-1] += 1
                
            else:
                # Línea normal, mantener como está
                if line:
                    converted_lines.append(line)
                
            i += 1
        
        return '\n'.join(converted_lines)

    def convert_html_lists(self, content: str) -> str:
        """
        Convierte todas las listas HTML en el contenido a Markdown
        """
        result = content
        
        # Buscar y convertir cada lista
        pos = 0
        while pos < len(result):
            # Buscar el siguiente <ol> o <ul>
            ol_match = re.search(r'<ol(?:\s+[^>]*)?>', result[pos:], re.IGNORECASE)
            ul_match = re.search(r'<ul>', result[pos:], re.IGNORECASE)
            
            next_match = None
            if ol_match and ul_match:
                next_match = ol_match if ol_match.start() < ul_match.start() else ul_match
            elif ol_match:
                next_match = ol_match
            elif ul_match:
                next_match = ul_match
            
            if not next_match:
                break
                
            # Extraer el contenido de la lista
            start_pos = pos + next_match.start()
            list_content, end_pos = self.extract_list_content(result, start_pos)
            
            # Convertir la lista
            converted_content = self.convert_list_items(list_content)
            
            # Reemplazar en el resultado
            result = result[:start_pos] + converted_content + result[end_pos:]
            
            # Actualizar posición
            pos = start_pos + len(converted_content)
        
        return result

    def clean_empty_lines(self, content: str) -> str:
        """Limpia líneas vacías excesivas"""
        lines = content.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            if line.strip() == '':
                if not prev_empty:
                    cleaned_lines.append('')
                prev_empty = True
            else:
                cleaned_lines.append(line)
                prev_empty = False
        
        return '\n'.join(cleaned_lines)

def main():
    if len(sys.argv) != 2:
        print("Uso: python html_to_markdown_converter.py <archivo>")
        print("o")
        print("Uso: python html_to_markdown_converter.py -")
        print("(para leer desde stdin)")
        sys.exit(1)
    
    converter = HTMLToMarkdownConverter()
    
    if sys.argv[1] == '-':
        # Leer desde stdin
        content = sys.stdin.read()
    else:
        # Leer desde archivo
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo {sys.argv[1]}")
            sys.exit(1)
        except UnicodeDecodeError:
            try:
                with open(sys.argv[1], 'r', encoding='latin-1') as f:
                    content = f.read()
            except UnicodeDecodeError:
                print(f"Error: No se pudo leer el archivo {sys.argv[1]} con codificación UTF-8 o Latin-1")
                sys.exit(1)
    
    # Convertir listas HTML a Markdown
    converted = converter.convert_html_lists(content)
    converted = converter.clean_empty_lines(converted)
    
    # Imprimir resultado
    print(converted)

if __name__ == "__main__":
    main()