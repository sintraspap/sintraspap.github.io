#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generador de páginas estáticas para noticias de SINTRASPAP
Para mejorar el compartido en redes sociales
"""

import json
import os
import re
import html
from datetime import datetime

# Configuración
SITE_URL = "https://sintraspap.github.io"
NOTICIAS_JSON = "data/noticias.json"
OUTPUT_DIR = "."  # Esto pondrá los archivos en la raíz

def slugify(text):
    """Convierte texto a formato slug para URLs"""
    if not text:
        return "noticia"
    
    # Convertir a minúsculas y quitar acentos básicos
    text = text.lower().strip()
    text = re.sub(r'[áàäâ]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöô]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'ñ', 'n', text)
    
    # Eliminar caracteres especiales
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    text = text.strip('-')
    
    # Si queda vacío, usar "noticia"
    if not text:
        return "noticia"
    
    # Limitar longitud
    if len(text) > 60:
        text = text[:60].rsplit('-', 1)[0]
    
    return text

def generar_pagina_noticia(noticia, index):
    """Genera una página HTML estática para una noticia"""
    
    # Crear slug para el nombre del archivo
    slug = slugify(noticia.get('titulo', f'noticia-{index}'))
    output_file = os.path.join(OUTPUT_DIR, f"{slug}.html")
    
    # Datos de la noticia (escapar HTML)
    titulo = html.escape(noticia.get('titulo', 'Noticia SINTRASPAP'))
    fecha = html.escape(noticia.get('fecha', ''))
    imagen = noticia.get('imagen', '')
    contenido = noticia.get('cuerpo', '')  # Ya es HTML, no escapar
    resumen = html.escape(noticia.get('resumen', ''))
    
    # URL completa de la imagen
    if imagen and not imagen.startswith(('http://', 'https://')):
        imagen_url = f"{SITE_URL}/{imagen}"
    else:
        imagen_url = imagen
    
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
    <meta property="og:image" content="{imagen_url}">
    <meta property="og:url" content="{SITE_URL}/{slug}.html">
    <meta property="og:site_name" content="SINTRASPAP">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{titulo} - SINTRASPAP">
    <meta name="twitter:description" content="{resumen}">
    <meta name="twitter:image" content="{imagen_url}">
    
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background: #fff;
            color: #333;
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
            font-weight: bold;
        }}
        .volver:hover {{
            background: #1e4f9a;
        }}
        .contenido p {{
            margin-bottom: 1em;
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
    
    return f"{slug}.html"

def main():
    print("📰 Generando páginas estáticas para noticias...")
    
    try:
        # Leer noticias existentes
        with open(NOTICIAS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        noticias = data if isinstance(data, list) else data.get('items', [])
        print(f"📖 Encontradas {len(noticias)} noticias")
        
        # Generar página para cada noticia
        urls_generadas = []
        for i, noticia in enumerate(noticias):
            url = generar_pagina_noticia(noticia, i)
            urls_generadas.append(f"{SITE_URL}/{url}")
            print(f"✅ Generada: {url}")
        
        # Generar sitemap simple
        with open('sitemap-noticias.txt', 'w', encoding='utf-8') as f:
            f.write("\n".join(urls_generadas))
        
        print(f"\n🎉 ¡Proceso completado!")
        print(f"📄 {len(urls_generadas)} páginas generadas")
        print(f"🗺️ Sitemap generado: 'sitemap-noticias.txt'")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {NOTICIAS_JSON}")
        print("💡 Asegúrate de que el archivo data/noticias.json existe")
    except json.JSONDecodeError as e:
        print(f"❌ Error: El archivo JSON tiene formato incorrecto: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()