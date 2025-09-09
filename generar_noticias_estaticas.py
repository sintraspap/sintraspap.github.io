#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generador de páginas estáticas para noticias de SINTRASPAP
Para mejorar el compartido en redes sociales
"""

import json
import os
import re
from datetime import datetime

# Configuración
SITE_URL = "https://sintraspap.github.io"
NOTICIAS_JSON = "data/noticias.json"
OUTPUT_DIR = "."  # Esto pondrá los archivos en la raíz

def slugify(text):
    """Convierte texto a formato slug para URLs compatible con GitHub Pages"""
    if not text:
        return "noticia"
    
    # Diccionario completo de reemplazos
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ñ': 'n', 'ü': 'u', 
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
        'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
        'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o', 
        'ç': 'c',
        '¿': '', '?': '', '¡': '', '!': '',
        '´': '', '`': '', "'": '', '"': '', 
        '(': '', ')': '', '[': '', ']': '', '{': '', '}': '',
        '*': '', '+': '-', '=': '-', '$': '', '%': '', 
        '&': 'y', '@': '', '#': '', ';': '', ':': '', 
        ',': '', '.': '', '<': '', '>': '', '/': '-', '\\': '-',
        'º': '', 'ª': '', '·': '-'
    }
    
    text = text.lower().strip()
    
    # Aplicar reemplazos
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Eliminar otros caracteres especiales y normalizar
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    text = text.strip('-')
    
    # Si después de todo el procesamiento queda vacío, usar "noticia"
    if not text:
        return "noticia"
    
    # Limitar longitud para GitHub Pages
    if len(text) > 60:
        text = text[:60]
        # Asegurar que no termina con guión
        text = text.rsplit('-', 1)[0]
    
    return text

def main():
    print("🔄 Generando páginas estáticas para noticias...")
    
    try:
        # Leer noticias existentes
        with open(NOTICIAS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        noticias = data.get('items', [])
        print(f"📝 Encontradas {len(noticias)} noticias")
        
        # Generar página para cada noticia
        urls_generadas = []
        for i, noticia in enumerate(noticias):
            url = generar_pagina_noticia(noticia, i)
            urls_generadas.append(url)
            print(f"✅ Generada: {url}")
        
        # Generar sitemap simple
        with open('sitemap-noticias.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(urls_generadas))
        
        print(f"\n🎉 ¡Proceso completado!")
        print(f"📋 {len(urls_generadas)} páginas generadas en la carpeta '{OUTPUT_DIR}/'")
        print(f"📄 Sitemap generado: 'sitemap-noticias.txt'")
        print(f"\n➡️ Ahora actualiza los enlaces 'Compartir' en tu HTML para usar estas URLs estáticas")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {NOTICIAS_JSON}")
    except json.JSONDecodeError:
        print("❌ Error: El archivo JSON tiene formato incorrecto")

if __name__ == "__main__":
    main()