import HomeView from '@/views/HomeView.vue';
import SearchView from '@/views/SearchView.vue';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/search',
    name: 'Search',
    component: SearchView,
  },
//   {
//     path: '/:pathMatch(.*)*',
//     name: 'NotFound',
//     component: () => import('../views/NotFoundView.vue'),
//   },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
