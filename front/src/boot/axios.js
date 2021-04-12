import Vue from 'vue'
import axios from 'axios'

Vue.prototype.$axios = axios


const api = axios.create({
    baseURL: 'http://localhost:9000'
})
// api.defaults.headers.common['Authorization'] = AUTH_TOKEN;
api.defaults.headers.post['Content-Type'] = 'application/json';
Vue.prototype.$api = api

export { axios, api }