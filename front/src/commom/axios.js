import axios from 'axios'
import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)
// import store from './vuex'
// 引入notify模块 以便axios在response 异常的时候弹出提示信息
// import { Notification } from 'element-ui';

// 设置默认ajax请求源地址
axios.defaults.baseURL = process.env.API_ENDPOINT

// 设置axios拦截器，设置ajax请求Authorization的header都从cookie中读取
axios.interceptors.request.use(function (config) {
    // Do something before request is sent
    let access_token = Vue.cookie.get('kafkaid')
    if (config.url && !config.url.startsWith('http://127.0.0.1:8000')) {
      if (access_token) {
        config.headers['Authorization'] =access_token
        config.headers['Content-Type'] = "application/json"
      }
    }
    // ajax开始后，顶部进度条显示
    // store.commit('set_processing', true)
    return config;
  }, function (error) {
    // Do something with request error
    return Promise.reject(error);
});

// // 请求完成后的拦截
// axios.interceptors.response.use(response => {
//   // ajax结束后，进度条隐藏
//   store.commit('set_processing', false)
//   return response
// }, error => {
//   store.commit('set_processing', false)
//   // 这里我们把错误信息扶正, 后面就不需要写 catch 了
//   Notification.error({
//     title: '请求发生异常！状态码：' + error.response.status,
//     message: error.response.statusText
//   });
//   return Promise.resolve(error.response)
// })

// 可在vue中使用this.axios来调用axios模块
Vue.prototype.axios = axios

export default axios
