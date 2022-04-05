import Vue from 'vue';
import VueRouter from 'vue-router';
import Main from '../components/Main.vue';
import DefaultDeduction from "../components/delault_deduction/DefaultDeduction.vue";
import Login from "../components/Login";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main
  },
  {
    path: '/default-deduction',
    name: 'DefaultDeduction',
    component: DefaultDeduction
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  if (authRequired && !loggedIn) {
    return next('/login');
  }
  next();
});
