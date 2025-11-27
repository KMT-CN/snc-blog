<script setup lang="ts">
defineProps<{
  loading: boolean
}>();
</script>

<template>
  <Transition name="fade-blur">
    <div v-if="loading" class="loading-screen">
      <div class="content">
        <div class="logo-box">
          <span class="logo-text">SNC</span>
        </div>
        <div class="loading-bar">
          <div class="progress"></div>
        </div>
        <div class="loading-status">SYSTEM INITIALIZING...</div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #000000;
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #ffffff;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.logo-box {
  border: 2px solid #ffffff;
  padding: 1rem 2rem;
  position: relative;
  overflow: hidden;
}

.logo-text {
  font-size: 3rem;
  font-weight: 900;
  letter-spacing: 0.5rem;
  font-family: 'Courier New', Courier, monospace;
  position: relative;
  z-index: 1;
}

/* 扫描线效果 */
.logo-box::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to bottom,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: rotate(45deg);
  animation: scan 2s infinite;
}

.loading-bar {
  width: 200px;
  height: 2px;
  background-color: #333;
  position: relative;
  overflow: hidden;
}

.progress {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background-color: #ffffff;
  transform: translateX(-100%);
  animation: load 1.5s ease-in-out infinite;
}

.loading-status {
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.8rem;
  letter-spacing: 2px;
  opacity: 0.7;
  animation: blink 1s infinite;
}

@keyframes scan {
  0% { transform: translateY(-100%) rotate(45deg); }
  100% { transform: translateY(100%) rotate(45deg); }
}

@keyframes load {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(0); }
  100% { transform: translateX(100%); }
}

@keyframes blink {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 0.3; }
}

/* 虚化消散动画 - 升级版：超光速跳跃 */
.fade-blur-leave-active {
  animation: hyperspace-exit 0.8s cubic-bezier(0.65, 0, 0.35, 1) forwards;
}

.fade-blur-leave-active .content {
  animation: content-explode 0.5s cubic-bezier(0.65, 0, 0.35, 1) forwards;
}

@keyframes hyperspace-exit {
  0% {
    opacity: 1;
    transform: scale(1);
    filter: brightness(1);
  }
  30% {
    /* 蓄力阶段：变暗，轻微收缩，营造紧张感 */
    opacity: 1;
    transform: scale(0.98);
    filter: brightness(0.8);
  }
  40% {
    /* 能量积聚：高亮 */
    opacity: 1;
    transform: scale(0.98);
    filter: brightness(1.5);
  }
  100% {
    /* 爆发：横向极度拉伸，纵向压缩，模拟光速穿梭 */
    opacity: 0;
    transform: scaleX(4) scaleY(0.02);
    filter: brightness(5) blur(10px);
  }
}

@keyframes content-explode {
  0% {
    opacity: 1;
    transform: scale(1);
    letter-spacing: normal;
  }
  100% {
    /* 内容向四周炸开并虚化 */
    opacity: 0;
    transform: scale(2);
    filter: blur(20px);
    letter-spacing: 2rem;
  }
}
</style>
