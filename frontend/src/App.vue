<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import Navigation from './components/Navigation.vue'
import Footer from './components/Footer.vue'
import ParticleBackground from './components/ParticleBackground.vue'
import LoadingScreen from './components/LoadingScreen.vue'

const isLoading = ref(true)

onMounted(() => {
  // 模拟加载过程，实际项目中可以根据资源加载情况控制
  setTimeout(() => {
    isLoading.value = false
  }, 2000)
})
</script>

<template>
  <div id="app">
    <LoadingScreen :loading="isLoading" />
    <ParticleBackground />
    <Navigation />
    <main>
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
    <Footer />
  </div>
</template>

<style scoped>
main {
  flex: 1;
  padding-top: 70px; /* 导航栏高度 */
}

/* 页面过渡动画 */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
