module.exports = function (eleventyConfig) {
  // Copiar tal cual a _site
  eleventyConfig.addPassthroughCopy("data");            // <-- aquí vive noticias.json
  eleventyConfig.addPassthroughCopy("images");          // para /images/uploads
  eleventyConfig.addPassthroughCopy("assets");          // si usas /assets

  return {
    dir: {
      input: ".",      // raíz del repo
      output: "_site", // carpeta de publicación
    },
  };
};
