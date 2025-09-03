// generador-sintraspap.js
// Script simple para generar páginas con metadatos correctos para redes sociales

const fs = require('fs');

// Tu configuración específica
const CONFIG = {
  baseUrl: 'https://sintraspappy2025.github.io/sintraspap.github.io',
  noticiasJson: './data/noticias.json',
  outputDir: './n', // Directorio corto para URLs más limpias
};

// Función para normalizar título a slug (igual que tu noticia.html)
function normalizar(texto = "") {
  return texto.toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9\s-]/g, "")
    .trim().replace(/\s+/g, "-");
}

// Función para escapar HTML
function escapeHtml(text) {
  return text.replace(/[&<>"']/g, function(m) {
    return {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    }[m];
  });
}

// Template optimizado para tu caso
const TEMPLATE = `<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{{TITULO}} – SINTRASPAP</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{{RESUMEN}}">
  
  <!-- Metadatos Open Graph para redes sociales -->
  <meta property="og:title" content="{{TITULO}}">
  <meta property="og:description" content="{{RESUMEN}}">
  <meta property="og:image" content="{{IMAGE_URL}}">
  <meta property="og:url" content="{{PAGE_URL}}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="SINTRASPAP">
  
  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{TITULO}}">
  <meta name="twitter:description" content="{{RESUMEN}}">
  <meta name="twitter:image" content="{{IMAGE_URL}}">
  
  <!-- Redirección inmediata para usuarios normales -->
  <script>
    // Detectar crawlers de redes sociales
    const userAgent = navigator.userAgent;
    const isCrawler = /facebookexternalhit|twitterbot|WhatsApp|TelegramBot|LinkedInBot/i.test(userAgent);
    
    if (!isCrawler) {
      // Redirigir usuarios normales al sistema dinámico original
      window.location.replace('../noticia.html?slug={{SLUG}}');
    }
  </script>
  
  <style>
    body {
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      max-width: 800px;
      margin: 20px auto;
      padding: 0 16px;
      line-height: 1.6;
    }
    img { max-width: 100%; border-radius: 8px; margin: 16px 0; }
    .muted { color: #777; font-size: 14px; margin-top: 10px; }
    a { color: #0b2a59; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .loading { text-align: center; padding: 40px; color: #666; }
  </style>
</head>
<body>
  <!-- Contenido estático para crawlers -->
  <a href="../index.html#inicio">← Volver al inicio</a>
  
  <article style="margin-top:14px">
    <h1>{{TITULO}}</h1>
    {{FECHA_HTML}}
    {{IMAGEN_HTML}}
    <div>{{CUERPO}}</div>
    
    <p style="margin-top: 30px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
      <strong>SINTRASPAP</strong> - Sindicato Nacional de Trabajadores de la Seguridad Privada y Afines del Paraguay
    </p>
  </article>
  
  <!-- Mensaje temporal para usuarios mientras redirige -->
  <div class="loading" id="loading">
    <p>Redirigiendo a la versión completa...</p>
    <p><a href="../noticia.html?slug={{SLUG}}">Haz clic aquí si no te redirige</a></p>
  </div>
  
  <script>
    // Ocultar mensaje de carga para crawlers
    if (/facebookexternalhit|twitterbot|WhatsApp|TelegramBot|LinkedInBot/i.test(navigator.userAgent)) {
      document.getElementById('loading').style.display = 'none';
    }
  </script>
</body>
</html>`;

function generarPaginas() {
  try {
    console.log('🚀 Generando páginas para SINTRASPAP...');
    
    // Leer noticias.json
    const data = JSON.parse(fs.readFileSync(CONFIG.noticiasJson, 'utf8'));
    const noticias = data.items || [];
    
    console.log(`📰 Encontradas ${noticias.length} noticias`);
    
    // Crear directorio si no existe
    if (!fs.existsSync(CONFIG.outputDir)) {
      fs.mkdirSync(CONFIG.outputDir, { recursive: true });
    }
    
    // Generar archivo para cada noticia
    noticias.forEach((noticia, index) => {
      const slug = normalizar(noticia.titulo);
      const fileName = `${slug}.html`;
      const filePath = `${CONFIG.outputDir}/${fileName}`;
      
      // URLs completas
      const pageUrl = `${CONFIG.baseUrl}/${CONFIG.outputDir}/${fileName}`;
      const imageUrl = noticia.imagen 
        ? `${CONFIG.baseUrl}/${noticia.imagen}`
        : `${CONFIG.baseUrl}/images/logo-sintraspap.png`;
      
      // HTML condicional
      const fechaHtml = noticia.fecha 
        ? `<p class="muted">${escapeHtml(noticia.fecha)}</p>` 
        : '';
      const imagenHtml = noticia.imagen 
        ? `<img src="${escapeHtml(noticia.imagen)}" alt="${escapeHtml(noticia.titulo)}">` 
        : '';
      
      // Generar HTML
      let html = TEMPLATE
        .replace(/{{TITULO}}/g, escapeHtml(noticia.titulo))
        .replace(/{{RESUMEN}}/g, escapeHtml(noticia.resumen))
        .replace(/{{IMAGE_URL}}/g, imageUrl)
        .replace(/{{PAGE_URL}}/g, pageUrl)
        .replace(/{{SLUG}}/g, slug)
        .replace(/{{FECHA_HTML}}/g, fechaHtml)
        .replace(/{{IMAGEN_HTML}}/g, imagenHtml)
        .replace(/{{CUERPO}}/g, noticia.cuerpo);
      
      // Guardar archivo
      fs.writeFileSync(filePath, html, 'utf8');
      console.log(`✅ ${index + 1}. ${fileName}`);
    });
    
    // Generar archivo de índice para fácil acceso
    let indexHtml = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Noticias SINTRASPAP - Índice</title>
</head>
<body>
  <h1>Noticias Generadas - SINTRASPAP</h1>
  <ul>`;
    
    noticias.forEach(noticia => {
      const slug = normalizar(noticia.titulo);
      indexHtml += `
    <li>
      <a href="${slug}.html">${escapeHtml(noticia.titulo)}</a>
      <br><small>${escapeHtml(noticia.fecha)} - Para compartir: ${CONFIG.baseUrl}/${CONFIG.outputDir}/${slug}.html</small>
    </li>`;
    });
    
    indexHtml += `
  </ul>
  <p><a href="../index.html">← Volver al sitio principal</a></p>
</body>
</html>`;
    
    fs.writeFileSync(`${CONFIG.outputDir}/index.html`, indexHtml, 'utf8');
    
    console.log('\n🎉 ¡Completado!');
    console.log(`📂 Páginas generadas en: /${CONFIG.outputDir}/`);
    console.log('\n📱 URLs para compartir en redes sociales:');
    
    noticias.forEach(noticia => {
      const slug = normalizar(noticia.titulo);
      console.log(`• ${CONFIG.baseUrl}/${CONFIG.outputDir}/${slug}.html`);
    });
    
    console.log('\n🔍 Para verificar el compartir:');
    console.log('Facebook: https://developers.facebook.com/tools/debug/');
    console.log('Twitter: https://cards-dev.twitter.com/validator');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

// Ejecutar
generarPaginas();
