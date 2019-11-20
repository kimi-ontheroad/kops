'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  // API_ENDPOINT: '"http://127.0.0.1:8000"',
  API_ENDPOINT: '"http://127.0.0.1:8000"',
  // 后端服务器地址和端口
  // API_ENDPOINT: '"http://10.222.57.149:8000"',
})
