import Vue from 'vue'
import axios from 'axios';
import Vuetify from 'vuetify/lib'
import 'vuetify/src/stylus/app.styl'
import store from '../store/index'
import router from './router'

Vue.use(Vuetify, {
  iconfont: 'md',
})

Vue.prototype.$axios = axios.create();

import App from './App.vue'

Vue.config.productionTip = false

new Vue({
	router,
	store,
	render: h => h(App),
}).$mount('#app')
