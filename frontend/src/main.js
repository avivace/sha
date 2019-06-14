import Vue from 'vue'
import axios from 'axios';
import BootstrapVue from 'bootstrap-vue'

import store from '../store/index'
import router from './router'

Vue.use(BootstrapVue)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'typeface-inter'
Vue.prototype.$axios = axios.create();

import App from './App.vue'

Vue.config.productionTip = false

new Vue({
	router,
	store,
	render: h => h(App),
}).$mount('#app')
