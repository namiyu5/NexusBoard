const path = require('path')
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: path.resolve(__dirname, '../nexus_board/staticfiles'),
  assetsDir: '',
  publicPath: '/',
  indexPath: path.resolve(__dirname, '../nexus_board/templates/nexus_board/index.html'),
})



