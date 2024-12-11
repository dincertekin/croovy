<script setup lang="js">
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useDark, useToggle } from '@vueuse/core';
import axios from 'axios';
import MoonIcon from '@/components/MoonIcon.vue';
import SunIcon from '@/components/SunIcon.vue';

const isDark = useDark();
const toggleDark = useToggle(isDark);

const route = useRoute();
const router = useRouter();
const query = ref(route.query.q || '');
const results = ref([]);

function validateSearchQuery(searchQuery) {
  searchQuery = searchQuery.trim();

  if (searchQuery.length < 2) {
    return false;
  }

  if (searchQuery.length > 100) {
    return false;
  }

  const sanitizedQuery = searchQuery
    .replace(/[<>]/g, '') 
    .replace(/['"]/g, '')
    .replace(/[()]/g, '')
    .replace(/[;]/g, '');

  const maliciousPatterns = [
    /<script>/i,
    /javascript:/i,
    /onerror=/i,
    /alert\(/i,
    /\beval\b/i
  ];

  const hasMaliciousPattern = maliciousPatterns.some(pattern => pattern.test(searchQuery));
  
  if (hasMaliciousPattern) {
    return false;
  }

  return sanitizedQuery;
}

watch(() => route.query.q, (newQuery) => {
  if (newQuery) {
    const validatedQuery = validateSearchQuery(newQuery);
    if (validatedQuery) {
      query.value = validatedQuery;
      postSearch(validatedQuery);
    }
  }
}, { immediate: true });

async function postSearch(searchQuery) {
  try {
    const { data } = await axios.post('http://127.0.0.1:5000/search', { query: searchQuery }, {
      timeout: 10000,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    });
    
    results.value = data.results || [];
  } catch (error) {
    console.error('Search error:', error);
    results.value = [];
  }
}

function handleSearch() {
  const validatedQuery = validateSearchQuery(query.value);
  
  if (validatedQuery) {
    router.push({ path: '/search', query: { q: validatedQuery } });
  }
}
</script>

<template>
  <header class="p-4 border-b border-gray-200 dark:border-gray-700">
    <div class="max-w-5xl mx-auto flex items-center justify-between">
      <!-- Logo and search bar -->
      <div class="flex items-center space-x-8">
        <router-link to="/" class="no-underline">
          <h1
            class="text-3xl font-bold text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-500 transition-colors"
          >
            Croovy
          </h1>
        </router-link>

        <form @submit.prevent="handleSearch" class="w-full max-w-xl relative">
          <input
            v-model="query"
            type="text"
            placeholder="Search the web..."
            class="w-full px-4 py-2 pr-12 border border-gray-300 dark:border-gray-700 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
          />
          <button
            type="submit"
            class="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="text-gray-500 dark:text-gray-300"
            >
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          </button>
        </form>
      </div>

      <!-- Dark mode toggle -->
      <button
        @click="toggleDark()"
        class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        aria-label="Toggle Dark Mode"
      >
        <SunIcon v-if="isDark" />
        <MoonIcon v-else />
      </button>
    </div>
  </header>

  <main class="max-w-5xl mx-auto w-full flex-grow px-4 py-8">
    <div v-if="results.length > 0" class="text-gray-600 dark:text-gray-300 mb-4">
      About {{ results.length }} results for "{{ query }}"
    </div>

    <!-- Render results -->
    <div v-if="results.length > 0">
      <div v-for="result in results" :key="result.url" class="mb-8">
        <a :href="result.url" class="block" target="_blank" rel="noopener noreferrer">
          <h2
            class="text-xl font-semibold text-blue-700 dark:text-blue-400 hover:underline"
          >
            {{ result.title }}
          </h2>
        </a>
        <div class="text-green-700 dark:text-green-400 text-sm">
          {{ result.url }}
        </div>
        <p class="text-gray-600 dark:text-gray-300 mt-2">
          {{ result.description }}
        </p>
      </div>
    </div>

    <!-- Show no results message -->
    <div v-else class="text-center text-gray-600 dark:text-gray-300">
      <p class="text-2xl mb-4">No results found.</p>
      <p>Try different keywords or check your spelling</p>
    </div>
  </main>

  <footer
    class="p-4 text-center text-gray-500 dark:text-gray-400 border-t border-gray-200 dark:border-gray-700"
  >
    <p>&copy; 2024 Croovy Search</p>
  </footer>
</template>