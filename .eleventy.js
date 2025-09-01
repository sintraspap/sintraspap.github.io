module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy("data");
  eleventyConfig.addPassthroughCopy("images");
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("admin");   // <- NECESARIO para que sirva /admin
  return { dir: { input: ".", output: "_site" } };
};
