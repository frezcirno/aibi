import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  // must be placed here!
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    name: 'Root',
    path: '/',
    redirect: '/Organization',
  },
  {
    name: 'Organization',
    path: '/Organization',
    component: Layout,
    meta: { title: '组织查询', icon: 'el-icon-zoom-in' },
    redirect: '/Organization/Detail',
    children: [
      {
        name: 'OrganizationDetail',
        path: 'Detail/:hasPermId?',
        component: () => import('@/views/Organization.vue'),
        meta: { title: '组织信息查询', icon: 'table' }
      },
      {
        name: 'OrganizationFuzzy',
        path: 'Fuzzy/:name?',
        component: () => import('@/views/OrgByName.vue'),
        meta: { title: '组织名称模糊查询', icon: 'table' }
      },
    ]
  },
  {
    name: 'Person',
    path: '/Person',
    component: Layout,
    meta: { title: '人员查询', icon: 'user' },
    redirect: '/Person/Detail',
    children: [
      {
        name: 'PersonDetail',
        path: 'Detail/:hasPermId?',
        component: () => import('@/views/Person'),
        meta: { title: '人员信息查询', icon: 'user' }
      },
      {
        name: 'PersonFuzzy',
        path: 'Fuzzy/:name?',
        component: () => import('@/views/PerByName'),
        meta: { title: '人名模糊查询', icon: 'user' }
      },
    ]
  },
  {
    name: 'Graph',
    path: '/Graph',
    component: Layout,
    children: [
      {
        name: 'Graph1',
        path: '/Graph',
        component: () => import('@/views/Graph'),
        meta: { title: '网络浏览', icon: 'el-icon-help' },
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
