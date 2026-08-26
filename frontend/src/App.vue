<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useDark, useToggle } from '@vueuse/core';
import { Search, Sun, Moon, Loader2 } from 'lucide-vue-next';
import { fetchSearchResults } from './api';

const isDark = useDark({
  selector: 'html',
  attribute: 'class',
  valueDark: 'dark',
  valueLight: '',
});
const toggleDark = useToggle(isDark);

const query = ref('');
const activeQuery = ref('');
const results = ref([]);
const duration = ref(0);
const loading = ref(false);
const error = ref('');
const inputRef = ref(null);

// Global hotkey '/' to focus input
const handleKeyDown = (e) => {
  if (e.key === '/' && document.activeElement !== inputRef.value) {
    e.preventDefault();
    inputRef.value?.focus();
  }
};

onMounted(() => window.addEventListener('keydown', handleKeyDown));
onUnmounted(() => window.removeEventListener('keydown', handleKeyDown));

const handleSearch = async () => {
  if (!query.value.trim()) return;

  loading.value = true;
  error.value = '';
  activeQuery.value = query.value.trim();

  try {
    const data = await fetchSearchResults(query.value.trim());
    results.value = data.results;
    duration.value = data.duration;
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to fetch search results.';
    results.value = [];
  } finally {
    loading.value = false;
  }
};

const handleReset = () => {
  query.value = '';
  activeQuery.value = '';
  results.value = [];
  error.value = '';
};
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 flex flex-col font-sans transition-colors duration-200">
    <!-- Header -->
<header class="p-4 border-b border-gray-100 dark:border-gray-800/60 relative z-10">
  <div class="max-w-6xl mx-auto flex items-center justify-between gap-4">
    <!-- Search Section -->
    <div v-if="activeQuery" class="flex items-center gap-6 flex-1 max-w-3xl">
      <button
        @click="handleReset"
        class="text-2xl font-black text-blue-600 dark:text-blue-400 tracking-tight hover:opacity-80 shrink-0"
      >
        Croovy
      </button>
      <form @submit.prevent="handleSearch" class="relative w-full">
        <input
          ref="inputRef"
          v-model="query"
          type="text"
          placeholder="Search..."
          class="w-full px-5 py-2.5 pr-12 text-sm border border-gray-300 dark:border-gray-700 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white shadow-sm"
        />
        <button
          type="submit"
          aria-label="Submit Search"
          class="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full text-gray-400 hover:text-blue-500"
        >
          <Search class="w-4 h-4" />
        </button>
      </form>
    </div>

    <!-- Spacer when on landing page -->
    <div v-else />

    <!-- Dark Mode Button with Larger Target & High Z-Index -->
    <button
      type="button"
      @click="toggleDark()"
      class="relative z-20 p-3 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 dark:text-gray-400 cursor-pointer transition-colors shrink-0"
      aria-label="Toggle Theme"
    >
      <Sun v-if="isDark" class="w-6 h-6 pointer-events-none" />
      <Moon v-else class="w-6 h-6 pointer-events-none" />
    </button>
  </div>
</header>

    <!-- Main Content -->
    <main class="flex-grow flex flex-col max-w-6xl w-full mx-auto px-4">
      <!-- Landing View -->
      <div v-if="!activeQuery" class="flex-grow flex flex-col items-center justify-center -mt-16">
        <h1 class="text-7xl font-black text-blue-600 dark:text-blue-400 mb-8 tracking-tight">
          Croovy
        </h1>
        <form @submit.prevent="handleSearch" class="w-full max-w-xl relative">
          <input
            ref="inputRef"
            v-model="query"
            type="text"
            placeholder="Search the web... (Press '/' to focus)"
            class="w-full px-6 py-4 pr-14 text-base border border-gray-300 dark:border-gray-700 rounded-full shadow-sm focus:shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white transition-all"
          />
          <button
            type="submit"
            aria-label="Submit Search"
            class="absolute right-3 top-1/2 -translate-y-1/2 p-2.5 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-400 hover:text-blue-500"
          >
            <Search class="w-5 h-5" />
          </button>
        </form>
      </div>

      <!-- Results View -->
      <div v-else class="py-6">
        <div v-if="loading" class="flex items-center gap-2 py-12 text-gray-500">
          <Loader2 class="w-5 h-5 animate-spin" />
          <span>Searching RediSearch index...</span>
        </div>

        <div v-else-if="error" class="p-4 bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400 rounded-lg max-w-xl border border-red-200 dark:border-red-900">
          {{ error }}
        </div>

        <div v-else-if="results.length > 0" class="max-w-2xl">
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-6">
            About {{ results.length }} results ({{ duration }} seconds)
          </p>
          <div class="space-y-6">
            <article v-for="result in results" :key="result.url" class="group">
              <a
                :href="result.url"
                target="_blank"
                rel="noopener noreferrer"
                class="block"
              >
                <span class="text-xs text-gray-500 dark:text-gray-400 block truncate mb-0.5">
                  {{ result.url }}
                </span>
                <h2 class="text-xl font-medium text-blue-700 dark:text-blue-400 group-hover:underline">
                  {{ result.title }}
                </h2>
              </a>
              <p class="text-sm text-gray-600 dark:text-gray-300 mt-1 line-clamp-2 leading-relaxed">
                {{ result.description }}
              </p>
            </article>
          </div>
        </div>

        <div v-else class="py-12 text-gray-500">
          <p class="text-lg font-medium mb-1">No results found for "{{ activeQuery }}"</p>
          <p class="text-sm">Try different keywords or run a crawler job to index documents.</p>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="p-4 text-center text-xs text-gray-500 dark:text-gray-400 border-t border-gray-100 dark:border-gray-800/60">
      &copy; 2026 Croovy Search • Privacy-Focused Engine
    </footer>
  </div>
</template>
