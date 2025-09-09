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

def generar_pagina_noticia(noticia, index):
    """Genera una página HTML estática para una noticia"""
    
    # Crear slug para el nombre del archivo
    slug = slugify(noticia.get('titulo', f'noticia-{index}'))
    output_file = os.path.join(OUTPUT_DIR, f"{slug}.html")
    
    # Datos de la noticia
    titulo = noticia.get('titulo', 'Noticia SINTRASPAP')
    fecha = noticia.get('fecha', '')
    imagen = noticia.get('imagen', '')
    contenido = noticia.get('cuerpo', '')
    resumen = noticia.get('resumen', '')
    
    # Plantilla HTML
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo} - SINTRASPAP</title>
    <meta name="description" content="{resumen}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{titulo} - SINTRASPAP">
    <meta property="og:description" content="{resumen}">
    <meta property="og:image" content="{SITE_URL}/{imagen}">
    <meta property="og:url" content="{SITE_URL}/{slug}.html">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{titulo} - SINTRASPAP">
    <meta name="twitter:description" content="{resumen}">
    <meta name="twitter:image" content="{SITE_URL}/{imagen}">
    
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
        <h1>{titulo}</h1>
        {f'<p><strong>Fecha:</strong> {fecha}</p>' if fecha else ''}
        
        {f'<img src="{imagen}" alt="{titulo}" class="noticia-img">' if imagen else ''}
        
        <div class="contenido">
            {contenido}
        </div>
        
        <a href="{SITE_URL}" class="volver">← Volver al inicio</a>
    </article>

    <!-- Comentarios de Facebook -->
    <div id="fb-root"></div>
    <script async defer crossorigin="anonymous" 
        src="https://connect.facebook.net/es_LA/sdk.js#xfbml=1&version=v19.0"
        nonce="sintraspap"></script>
    
    <div class="fb-comments"
         data-href="{SITE_URL}/{slug}.html"
         data-width="100%"
         data-numposts="3"></div>

</body>
</html>"""
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Guardar archivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return f"{SITE_URL}/{slug}.html"

def main():
    print("📰 Generando páginas estáticas para noticias...")
    
    try:
        # Leer noticias existentes
        with open(NOTICIAS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        noticias = data.get('items', [])
        print(f"📖 Encontradas {len(noticias)} noticias")
        
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
        print(f"📄 {len(urls_generadas)} páginas generadas en la carpeta '{OUTPUT_DIR}/'")
        print(f"🗺️ Sitemap generado: 'sitemap-noticias.txt'")
        print(f"\n👉 Ahora actualiza los enlaces 'Compartir' en tu HTML para usar estas URLs estáticas")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {NOTICIAS_JSON}")
    except json.JSONDecodeError:
        print("❌ Error: El archivo JSON tiene formato incorrecto")

if __name__ == "__main__":
    main()