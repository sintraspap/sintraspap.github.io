const fs = require('fs');
const path = require('path');

// Leer el archivo noticias.json
const noticiasData = JSON.parse(fs.readFileSync('noticias.json', 'utf8'));
const noticias = noticiasData.items;

// Crear directorio de noticias si no existe
const noticiasDir = 'noticias';
if (!fs.existsSync(noticiasDir)) {
  fs.mkdirSync(noticiasDir);
}

// Función para generar slug
function generarSlug(texto) {
  return texto.toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9 ]/g, "")
    .trim().replace(/\s+/g, "-");
}

// Base URL
const baseUrl = "https://sintraspappy2025.github.io/sintraspap.github.io";

// Generar HTML para cada noticia
noticias.forEach(noticia => {
  const slug = generarSlug(noticia.titulo);
  const imageUrl = noticia.imagen.startsWith('http') ? noticia.imagen : `${baseUrl}/${noticia.imagen}`;
  
  const html = `<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${noticia.titulo} - SINTRASPAP</title>
    <meta name="description" content="${noticia.resumen}">
    
    <!-- Metadatos Open Graph -->
    <meta property="og:title" content="${noticia.titulo}">
    <meta property="og:description" content="${noticia.resumen}">
    <meta property="og:image" content="${imageUrl}">
    <meta property="og:url" content="${baseUrl}/noticias/${slug}.html">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="SINTRASPAP">
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${noticia.titulo}">
    <meta name="twitter:description" content="${noticia.resumen}">
    <meta name="twitter:image" content="${imageUrl}">
    
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            max-width: 800px;
            margin: 20px auto;
            padding: 0 16px;
            line-height: 1.6;
            color: #333;
        }
        img {
            max-width: 100%;
            border-radius: 8px;
            margin: 16px 0;
        }
        .muted {
            color: #777;
            font-size: 14px;
        }
        a {
            color: #0b2a59;
            text-decoration: none;
            font-weight: 500;
        }
        a:hover {
            text-decoration: underline;
        }
        .volver-inicio {
            display: inline-block;
            margin-bottom: 20px;
            padding: 8px 16px;
            background: #f0f4f9;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <a href="../index.html" class="volver-inicio">← Volver al inicio</a>
    
    <article>
        <h1>${noticia.titulo}</h1>
        ${noticia.fecha ? `<p class="muted">${noticia.fecha}</p>` : ''}
        
        <img src="${noticia.imagen}" alt="${noticia.titulo}" onerror="this.src='../images/logo-sintraspap.png'">
        
        <div>${noticia.cuerpo}</div>
        
        <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666;">
            <strong>SINTRASPAP</strong><br>
            Sindicato Nacional de Trabajadores de la Seguridad Privada y Afines del Paraguay
        </p>
    </article>
</body>
</html>`;

  // Guardar archivo
  fs.writeFileSync(path.join(noticiasDir, `${slug}.html`), html);
  console.log(`✓ Generada: noticias/${slug}.html`);
});

console.log('¡Todas las noticias han sido generadas!');