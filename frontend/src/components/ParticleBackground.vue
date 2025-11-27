<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';

const canvasRef = ref<HTMLCanvasElement | null>(null);
let animationFrameId: number;
let particles: Particle[] = [];
let w = 0;
let h = 0;

// 鼠标位置
const mouse = {
  x: -1000,
  y: -1000
};

// 配置
const config = {
  particleColor: 'rgba(0, 0, 0, 0.3)',
  lineColor: 'rgba(0, 0, 0, 0.05)',
  particleAmount: 60,
  defaultSpeed: 0.5,
  variantSpeed: 0.5,
  linkRadius: 140,
  mouseRadius: 200, // 鼠标影响范围
};

class Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;

  constructor() {
    this.x = Math.random() * w;
    this.y = Math.random() * h;
    this.vx = (Math.random() - 0.5) * config.defaultSpeed;
    this.vy = (Math.random() - 0.5) * config.defaultSpeed;
    this.size = Math.random() * 2 + 1;
  }

  update() {
    this.x += this.vx;
    this.y += this.vy;

    // 边界检查
    if (this.x < 0 || this.x > w) this.vx *= -1;
    if (this.y < 0 || this.y > h) this.vy *= -1;

    // 鼠标吸引
    const dx = mouse.x - this.x;
    const dy = mouse.y - this.y;
    const distance = Math.sqrt(dx * dx + dy * dy);

    if (distance < config.mouseRadius) {
      const forceDirectionX = dx / distance;
      const forceDirectionY = dy / distance;
      const force = (config.mouseRadius - distance) / config.mouseRadius;
      const directionX = forceDirectionX * force * 0.05; // 吸引力度
      const directionY = forceDirectionY * force * 0.05;
      
      this.vx += directionX;
      this.vy += directionY;
    }
    
    // 摩擦力，防止速度无限增加
    // 实际上简单的反弹模型不需要摩擦力，但为了吸引后不乱飞，可以限制最大速度
    const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
    const maxSpeed = 2;
    if (speed > maxSpeed) {
        this.vx = (this.vx / speed) * maxSpeed;
        this.vy = (this.vy / speed) * maxSpeed;
    }
  }

  draw(ctx: CanvasRenderingContext2D) {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = config.particleColor;
    ctx.fill();
  }
}

const init = () => {
  const canvas = canvasRef.value;
  if (!canvas) return;
  
  resize();
  
  // 初始化粒子
  particles = [];
  // 根据屏幕面积调整粒子数量
  const amount = Math.floor((w * h) / 15000); 
  const finalAmount = Math.min(Math.max(amount, 30), 100); // 限制在 30-100 之间

  for (let i = 0; i < finalAmount; i++) {
    particles.push(new Particle());
  }
  
  animate();
};

const resize = () => {
  if (!canvasRef.value) return;
  w = window.innerWidth;
  h = window.innerHeight;
  canvasRef.value.width = w;
  canvasRef.value.height = h;
};

const animate = () => {
  const canvas = canvasRef.value;
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  ctx.clearRect(0, 0, w, h);

  // 更新和绘制粒子
  particles.forEach(p => {
    p.update();
    p.draw(ctx);
  });

  // 绘制连线
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < config.linkRadius) {
        ctx.beginPath();
        ctx.strokeStyle = `rgba(0, 0, 0, ${0.15 * (1 - distance / config.linkRadius)})`;
        ctx.lineWidth = 1;
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.stroke();
      }
    }
    
    // 鼠标连线 (可选，如果想要鼠标也像一个粒子一样连接)
    const dx = mouse.x - particles[i].x;
    const dy = mouse.y - particles[i].y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    if (distance < config.linkRadius) {
        ctx.beginPath();
        ctx.strokeStyle = `rgba(0, 0, 0, ${0.2 * (1 - distance / config.linkRadius)})`;
        ctx.lineWidth = 1;
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(mouse.x, mouse.y);
        ctx.stroke();
    }
  }

  animationFrameId = requestAnimationFrame(animate);
};

const onMouseMove = (e: MouseEvent) => {
  mouse.x = e.clientX;
  mouse.y = e.clientY;
};

const onMouseLeave = () => {
    mouse.x = -1000;
    mouse.y = -1000;
}

onMounted(() => {
  window.addEventListener('resize', resize);
  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('mouseout', onMouseLeave);
  init();
});

onUnmounted(() => {
  window.removeEventListener('resize', resize);
  window.removeEventListener('mousemove', onMouseMove);
  window.removeEventListener('mouseout', onMouseLeave);
  cancelAnimationFrame(animationFrameId);
});
</script>

<template>
  <canvas ref="canvasRef" class="particle-background"></canvas>
</template>

<style scoped>
.particle-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1; /* 放在最底层 */
  pointer-events: none; /* 不阻挡点击事件 */
}
</style>
