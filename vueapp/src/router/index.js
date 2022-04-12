import Vue from 'vue';
import VueRouter from 'vue-router';
import Main from '../components/Main.vue';
import DefaultDeduction from "../components/delault_deduction/DefaultDeduction.vue";
import Login from "../components/Login";
import Note from "../components/note/Note";
import PlanList from "../components/plan/PlanList";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/default-deduction',
    name: 'DefaultDeduction',
    component: DefaultDeduction
  },
  {
    path: '/note',
    name: 'Note',
    component: Note
  },
  {
    path: '/plan-list',
    name: 'PlanList',
    component: PlanList
  },
];

const router = new VueRouter({
  mode: 'history',
  base: 'vueapp',
  routes
});

export default router;

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = sessionStorage.getItem('user');

  if (authRequired && !loggedIn) {
    return next('/login');
  }
  next();
});
