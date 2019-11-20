import Vue from 'vue'
import Router from 'vue-router'
import Consume from '@/components/consume'
import Topic from '@/components/topic'
import Monitor from '@/components/monitor'
import Login from '@/components/login'
Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    
      {
        path: '/login',
        name: 'login',
        component: Login
      },
      {
        path: '/topic',
        name: 'topic',
        component: Topic,
    
    },
    {
          
      path: '/comsume/',
      name: 'consume',
      component: Consume
    },
    {
      path: '/monitor/',
      name: 'monitor',
      component: Monitor
    }
    
   
  ]
})

router.beforeEach((to, from, next) => {
  if(to.path !== '/login' && !Vue.cookie.get('Authorization')){
    // next('/ui/login')
    next('/login?next=' + to.path)
  }else if(to.path === '/') {
    next('/topic')
  }else {
    next()
  }
});
export default router