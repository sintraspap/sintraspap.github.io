modulemodule.exports = function(eleventyConfig) {
  // Copiar estas carpetas y archivos tal cual a _site
  eleventyConfig.addPassthroughCopy("data");
  eleventyConfig.addPassthroughCopy("images");
  eleventyConfig.addPassthroughCopy("assets");

  return {
    dir: {
      input: ".",      // entrada = raíz
      output: "_site", // salida = _site
    },
  };
};
