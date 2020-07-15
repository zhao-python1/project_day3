import Vue from 'vue'
import Router from 'vue-router'
import Index from "../components/Index";
import Login from "../components/Login";
import Register from "../components/Register";
import Course from "../components/Course";
import CourseDetail from "../components/CourseDetail";
import Shop from "../components/Shop";



Vue.use(Router);

export default new Router({
  routes: [
    {
          path: '/',
          name:'Index',
          component:Index,
    },
    {
          path: '/index',
          name:'Index',
          component:Index,
    },
    {
          path: '/login',
          name:'Login',
          component:Login,
    },
    {
          path: '/register',
          name:'Register',
          component:Register,
    },
    {
          path: '/python',
          name:'Course',
          component:Course,
    },
    {
          path: '/detail/:id',
          name:'CourseDetail',
          component:CourseDetail,
    },
    {
          path: '/shop',
          name:'Shop',
          component:Shop,
    },


  ]
})
