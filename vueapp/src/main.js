import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false;
Vue.use(VueAxios, axios);
// Vue.prototype.$apiHost = window.location.origin;
Vue.prototype.$apiHost = 'http://0.0.0.0:8000';

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app');
