#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generador de páginas estáticas para noticias de SINTRASPAP
Autor: SINTRASPAP
Descripción: Genera páginas HTML estáticas para cada noticia con meta tags optimizados
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

def normalizar_texto(texto):
    """Convierte texto a slug para URLs amigables"""
    if not texto:
        return "noticia"
    
    # Convertir a minúsculas, quitar acentos y caracteres especiales
    texto = texto.lower()
    texto = re.sub(r'[áäà]', 'a', texto)
    texto = re.sub(r'[éëè]', 'e', texto)
    texto = re.sub(r'[íïì]', 'i', texto)
    texto = re.sub(r'[óöò]', 'o', texto)
    texto = re.sub(r'[úüù]', 'u', texto)
    texto = re.sub(r'[ñ]', 'n', texto)
    texto = re.sub(r'[^a-z0-9\s-]', '', texto)  # Remover caracteres especiales
    texto = re.sub(r'\s+', '-', texto.strip())   # Reemplazar espacios con guiones
    texto = re.sub(r'-+', '-', texto)            # Remover guiones múltiples
    
    return texto[:50]  # Limitar longitud

def generar_html_noticia(noticia, base_url="https://sintraspap.github.io"):
    """Genera el HTML completo para una noticia"""
    
    # Crear slug único para la URL
    slug = normalizar_texto(noticia.get('titulo', ''))
    
    # URL completa de la imagen
    imagen_url = f"{base_url}/{noticia.get('imagen', '')}" if noticia.get('imagen') else f"{base_url}/logo-sintraspap.png"
    
    # HTML template con meta tags optimizados
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{noticia.get('titulo', 'Noticia SINTRASPAP')} - SINTRASPAP</title>
    <meta name="description" content="{noticia.get('resumen', 'Noticia del Sindicato Nacional de Trabajadores de la Seguridad Privada')}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{base_url}/n/{slug}.html">
    <meta property="og:title" content="{noticia.get('titulo', 'Noticia SINTRASPAP')}">
    <meta property="og:description" content="{noticia.get('resumen', 'Noticia del Sindicato Nacional de Trabajadores de la Seguridad Privada')}">
    <meta property="og:image" content="{imagen_url}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="{base_url}/n/{slug}.html">
    <meta property="twitter:title" content="{noticia.get('titulo', 'Noticia SINTRASPAP')}">
    <meta property="twitter:description" content="{noticia.get('resumen', 'Noticia del Sindicato Nacional de Trabajadores de la Seguridad Privada')}">
    <meta property="twitter:image" content="{imagen_url}">
    
    <style>
        body {{
            font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background: #fff;
            color: #111;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #0b2a59;
            padding-bottom: 15px;
        }}
        .logo {{
            height: 80px;
            margin-bottom: 10px;
        }}
        .noticia-titulo {{
            color: #0b2a59;
            margin: 10px 0;
        }}
        .noticia-fecha {{
            color: #666;
            font-size: 14px;
        }}
        .noticia-imagen {{
            width: 100%;
            max-height: 400px;
            object-fit: cover;
            border-radius: 10px;
            margin: 15px 0;
        }}
        .noticia-cuerpo {{
            margin-top: 20px;
        }}
        .volver-inicio {{
            display: inline-block;
            margin-top: 30px;
            padding: 10px 15px;
            background: #0b2a59;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
    </style>
    
    <!-- Redirección para usuarios normales -->
    <script>
        // Detectar bots de redes sociales
        const userAgent = navigator.userAgent;
        const isCrawler = /facebookexternalhit|twitterbot|WhatsApp|TelegramBot|LinkedInBot/i.test(userAgent);
        
        if (!isCrawler) {{
            // Redirigir usuarios al sitio principal
            window.location.href = "{base_url}/#inicio";
        }}
    </script>
</head>
<body>
    <div class="header">
        <a href="{base_url}">
            <img src="{base_url}/logo-sintraspap.png" alt="SINTRASPAP" class="logo" onerror="this.style.display='none'">
        </a>
        <h1>SINTRASPAP</h1>
        <p>Sindicato Nacional de Trabajadores de la Seguridad Privada y Afines del Paraguay</p>
    </div>

    <article>
        <h2 class="noticia-titulo">{noticia.get('titulo', '')}</h2>
        <p class="noticia-fecha">📅 {noticia.get('fecha', '')}</p>
        
        {f'<img src="{imagen_url}" alt="{noticia.get("titulo", "")}" class="noticia-imagen" onerror="this.style.display=\'none\'">' if noticia.get('imagen') else ''}
        
        {f'<p class="noticia-resumen"><strong>{noticia.get("resumen", "")}</strong></p>' if noticia.get('resumen') else ''}
        
        <div class="noticia-cuerpo">
            {noticia.get('cuerpo', '')}
        </div>
    </article>

    <a href="{base_url}" class="volver-inicio">← Volver al inicio</a>

    <!-- Ocultar contenido para bots de redes sociales -->
    <script>
        if (!/facebookexternalhit|twitterbot|WhatsApp|TelegramBot|LinkedInBot/i.test(navigator.userAgent)) {{
            document.body.innerHTML = '<div style="text-align:center;padding:50px;"><p>Redirigiendo al sitio principal...</p><p><a href="{base_url}">Haz clic aquí si no te redirige</a></p></div>';
        }}
    </script>
</body>
</html>"""
    
    return html_template, slug

def generar_paginas_noticias():
    """Función principal que genera todas las páginas"""
    
    print("🚀 Generador de páginas estáticas para noticias SINTRASPAP")
    print("=" * 60)
    
    # Crear directorio si no existe
    Path("n").mkdir(exist_ok=True)
    
    try:
        # Cargar noticias desde JSON
        with open('data/noticias.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        noticias = datos.get('items', [])
        print(f"📰 Encontradas {len(noticias)} noticias")
        
        # Generar página para cada noticia
        for i, noticia in enumerate(noticias, 1):
            html_content, slug = generar_html_noticia(noticia)
            
            # Guardar archivo HTML
            nombre_archivo = f"n/{slug}.html"
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ {i}. {slug}.html")
        
        # Generar índice de noticias
        generar_indice(noticias)
        
        print(f"\n🎉 ¡Completado! {len(noticias)} páginas generadas en la carpeta 'n/'")
        print("🌐 URLs para compartir en redes sociales:")
        
        for noticia in noticias:
            slug = normalizar_texto(noticia.get('titulo', ''))
            print(f"   • https://sintraspap.github.io/n/{slug}.html")
            
    except FileNotFoundError:
        print("❌ Error: No se encontró data/noticias.json")
    except json.JSONDecodeError:
        print("❌ Error: El archivo JSON tiene formato incorrecto")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def generar_indice(noticias):
    """Genera una página índice con todas las noticias"""
    
    indice_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice de Noticias - SINTRASPAP</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #0b2a59; }
        .noticia { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .fecha { color: #666; font-size: 14px; }
        .enlace { color: #0b2a59; text-decoration: none; }
    </style>
</head>
<body>
    <h1>📰 Índice de Noticias SINTRASPAP</h1>
    <p><a href="../index.html">← Volver al sitio principal</a></p>
    <hr>
"""
    
    for noticia in sorted(noticias, key=lambda x: x.get('fecha', ''), reverse=True):
        slug = normalizar_texto(noticia.get('titulo', ''))
        indice_html += f"""
    <div class="noticia">
        <h3><a class="enlace" href="{slug}.html">{noticia.get('titulo', '')}</a></h3>
        <p class="fecha">📅 {noticia.get('fecha', '')}</p>
        <p>{noticia.get('resumen', '')}</p>
    </div>
"""
    
    indice_html += """
</body>
</html>"""
    
    with open('n/index.html', 'w', encoding='utf-8') as f:
        f.write(indice_html)
    
    print("📋 Índice de noticias generado: n/index.html")

if __name__ == "__main__":
    generar_paginas_noticias()
