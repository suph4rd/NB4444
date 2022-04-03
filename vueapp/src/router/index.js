import Vue from 'vue';
import VueRouter from 'vue-router';
import Main from '../components/Main.vue';
import DefaultDeduction from "../components/delault_deduction/DefaultDeduction.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main
  },
  {
    path: '/default-deduction',
    name: 'default_deduction',
    component: DefaultDeduction
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
