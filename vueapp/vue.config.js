const static_dir = '../vueapp_core/static/vueapp_core';
const static_path = '/static/vueapp_core';
const BundleTracker = require("webpack-bundle-tracker");
const isProduction = process.env.NODE_ENV === "production";

module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  publicPath: isProduction ? static_path : "/",
  outputDir: isProduction ? static_dir : 'dist/',
  configureWebpack: (config) => {
    if (isProduction) {
      config.plugins.push(new BundleTracker());
    }
  },
}
