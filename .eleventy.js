module.exports = function(eleventyConfig) {
  eleventyConfig.addPassthroughCopy("data");
  eleventyConfig.addPassthroughCopy("images");
  eleventyConfig.addPassthroughCopy("assets");
  return { dir: { input: ".", output: "_site" } };
};
