module.exports = function(eleventyConfig) {
  // Copiar tal cual al sitio final (tu index, css, js, assets, admin, etc.)
  eleventyConfig.addPassthroughCopy({ "assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "admin": "admin" });
  eleventyConfig.addPassthroughCopy("favicon.ico");
  eleventyConfig.addPassthroughCopy("favicon-16x16.png");
  eleventyConfig.addPassthroughCopy("favicon-32x32.png");
  eleventyConfig.addPassthroughCopy("logo-sintraspap.png");
  eleventyConfig.addPassthroughCopy("logo-cnt.png");
  eleventyConfig.addPassthroughCopy("logo-citsp.png");
  eleventyConfig.addPassthroughCopy("secretario-conflictos.jpg");
  eleventyConfig.addPassthroughCopy("banner-1.png");
  eleventyConfig.addPassthroughCopy("banner-2.png");

  // Tu index.html actual y demás páginas estáticas pasan tal cual
  eleventyConfig.addPassthroughCopy("index.html");

  // Colección de noticias (ordenadas por fecha desc)
  eleventyConfig.addCollection("noticias", (collection) => {
    return collection.getFilteredByGlob("content/noticias/*.md")
      .sort((a,b) => (b.data.date || 0) - (a.data.date || 0));
  });

  return {
    dir: { input: ".", includes: "_includes", data: "_data", output: "_site" }
  };
};
