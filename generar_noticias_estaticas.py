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
OUTPUT_DIR = "noticias"

def slugify(text):
    """Convierte texto a formato slug para URLs"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text

def generar_pagina_noticia(noticia, index):
    """Genera HTML estático para una noticia"""
    
    # Crear slug para la URL
    slug = slugify(noticia.get('titulo', f'noticia-{index}'))
    
    # Plantilla HTML
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{noticia.get('titulo', '')} - SINTRASPAP</title>
    <meta name="description" content="{noticia.get('resumen', '')}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{noticia.get('titulo', '')} - SINTRASPAP">
    <meta property="og:description" content="{noticia.get('resumen', '')}">
    <meta property="og:image" content="{noticia.get('imagen', '')}">
    <meta property="og:url" content="{SITE_URL}/{slug}.html">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{noticia.get('titulo', '')} - SINTRASPAP">
    <meta name="twitter:description" content="{noticia.get('resumen', '')}">
    <meta name="twitter:image" content="{noticia.get('imagen', '')}">
    
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        .noticia-img {{
            width: 100%;
            max-height: 400px;
            object-fit: cover;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .volver {{
            display: inline-block;
            margin-top: 30px;
            padding: 10px 15px;
            background: #0b2a59;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <article>
        <h1>{noticia.get('titulo', '')}</h1>
        <p><strong>Fecha:</strong> {noticia.get('fecha', '')}</p>
        
        {f'<img src="{noticia["imagen"]}" alt="{noticia.get("titulo", "")}" class="noticia-img">' if noticia.get('imagen') else ''}
        
        <div class="contenido">
            {noticia.get('cuerpo', '')}
        </div>
        
        <a href="{SITE_URL}" class="volver">← Volver al inicio</a>
    </article>
</body>
</html>"""
    
    # Crear directorio si no existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Guardar archivo
    filename = f"{OUTPUT_DIR}/{slug}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return f"{SITE_URL}/{slug}.html"

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