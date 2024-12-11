<script setup lang="js">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useDark, useToggle } from '@vueuse/core';
import MoonIcon from '@/components/MoonIcon.vue';
import SunIcon from '@/components/SunIcon.vue';

const isDark = useDark();
const toggleDark = useToggle(isDark);
const router = useRouter();
const query = ref('');

function search(query) {
  router.push({
    name: 'Search',
    query: {
      q: query
    }
  });
}
</script>

<template>
  <header class="p-4 flex justify-end items-center">
    <!-- Dark mode toggle -->
    <button
      @click="toggleDark()"
      class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      aria-label="Toggle Dark Mode"
    >
      <SunIcon v-if="isDark" />
      <MoonIcon v-else />
    </button>
  </header>

  <main class="flex flex-col items-center justify-center flex-grow px-4">
    <!-- Croovy Logo -->
    <router-link to="/" class="no-underline">
      <h1
        class="text-6xl font-bold mb-12 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-500 transition-colors cursor-pointer"
      >
        Croovy
      </h1>
    </router-link>

    <!-- Search Container -->
    <div class="w-full max-w-xl relative">
      <form class="flex">
        <input
          v-model="query"
          type="text"
          placeholder="Search the web..."
          class="w-full px-4 py-3 pr-12 border border-gray-300 dark:border-gray-700 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
        />
        <button
          @click.prevent="search(query)"
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
  </main>

  <footer class="p-4 text-center text-gray-500 dark:text-gray-400">
    <p>&copy; 2024 Croovy Search</p>
  </footer>
</template>
