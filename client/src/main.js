import Vue from 'vue';
import App from './app';
import router from './router';
import store from './store';

import VueDragTree from 'vue-drag-tree';
import 'vue-drag-tree/dist/vue-drag-tree.min.css';

Vue.config.productionTip = false;

Vue.use(VueDragTree);
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});
