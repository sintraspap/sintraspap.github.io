module.exports = function(eleventyConfig) {
  // Copiar tal cual al output
  eleventyConfig.addPassthroughCopy("data");
  eleventyConfig.addPassthroughCopy("images");
  eleventyConfig.addPassthroughCopy("assets");

  return {
    dir: {
      input: ".",      
      output: "_site", 
    },
  };
};
