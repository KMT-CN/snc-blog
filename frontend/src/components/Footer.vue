<script setup lang="ts">
import { ref, onMounted } from 'vue'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

const currentYear = new Date().getFullYear()

// 社交链接类型
interface SocialLink {
  name: string
  icon: string
  url: string
  title?: string
}

// 默认社交链接
const defaultSocialLinks: SocialLink[] = [
  { name: 'GitHub', icon: '💻', url: 'https://github.com' },
  { name: 'Email', icon: '📧', url: 'mailto:contact@snc.edu.cn' },
  { name: 'QQ', icon: '💬', url: '' }
]

const socialLinks = ref<SocialLink[]>(defaultSocialLinks)

// 默认联系信息
const contactInfo = ref({
  address: '学校地址',
  email: 'contact@snc.edu.cn',
  workTime: '周一至周五 9:00-17:00'
})

// 网站信息
const siteInfo = ref({
  name: '学生网络中心',
  description: '致力于为学校师生提供优质的网络服务和技术支持，推动校园信息化建设。'
})

const quickLinks = [
  { name: '首页', path: '/' },
  { name: '服务导航', path: '/services' },
  { name: '博客', path: '/blog' },
  { name: '活动', path: '/events' },
  { name: '关于我们', path: '/about' }
]

// 加载设置
const loadSettings = async () => {
  try {
    const response = await fetch(`${API_BASE}/settings/`)
    if (response.ok) {
      const settings = await response.json()
      
      // 更新网站信息
      if (settings.siteName) {
        siteInfo.value.name = settings.siteName
      }
      if (settings.siteDescription) {
        siteInfo.value.description = settings.siteDescription
      }
      
      // 更新联系信息
      if (settings.contactEmail) {
        contactInfo.value.email = settings.contactEmail
      }
      if (settings.address) {
        contactInfo.value.address = settings.address
      }
      if (settings.workTime) {
        contactInfo.value.workTime = settings.workTime
      }
      
      // 更新社交链接
      const newSocialLinks: SocialLink[] = []
      if (settings.github) {
        newSocialLinks.push({ name: 'GitHub', icon: '💻', url: settings.github })
      }
      if (settings.contactEmail) {
        newSocialLinks.push({ name: 'Email', icon: '📧', url: `mailto:${settings.contactEmail}` })
      }
      if (settings.qq) {
        newSocialLinks.push({ name: 'QQ群', icon: '💬', url: `https://qm.qq.com/q/${settings.qq}` })
      }
      if (settings.wechat) {
        newSocialLinks.push({ name: '微信', icon: '📱', url: '#', title: settings.wechat })
      }
      
      if (newSocialLinks.length > 0) {
        socialLinks.value = newSocialLinks
      }
    }
  } catch (error) {
    console.error('加载设置失败:', error)
    // 使用默认值
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<template>
  <footer class="footer">
    <div class="footer-wave">
      <svg class="waves" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 24 150 28" preserveAspectRatio="none" shape-rendering="auto">
        <defs>
          <path id="gentle-wave" d="M-160 44c30 0 58-30 88-30s 58 30 88 30 58-30 88-30 58 30 88 30 v44h-352z" />
        </defs>
        <g class="parallax">
          <use xlink:href="#gentle-wave" x="48" y="0" />
          <use xlink:href="#gentle-wave" x="48" y="3" />
          <use xlink:href="#gentle-wave" x="48" y="5" />
          <use xlink:href="#gentle-wave" x="48" y="7" />
        </g>
      </svg>
    </div>
    
    <div class="footer-content">
      <div class="container">
        <div class="footer-grid">
          <!-- 关于我们 -->
          <div class="footer-section">
            <h3>{{ siteInfo.name }}</h3>
            <p class="footer-description">
              {{ siteInfo.description }}
            </p>
            <div class="social-links">
              <a
                v-for="link in socialLinks"
                :key="link.name"
                :href="link.url"
                :title="link.title || link.name"
                class="social-link"
                target="_blank"
                rel="noopener noreferrer"
              >
                <span class="social-icon">{{ link.icon }}</span>
              </a>
            </div>
          </div>

          <!-- 快速链接 -->
          <div class="footer-section">
            <h4>快速链接</h4>
            <ul class="footer-links">
              <li v-for="link in quickLinks" :key="link.path">
                <router-link :to="link.path">{{ link.name }}</router-link>
              </li>
            </ul>
          </div>

          <!-- 联系我们 -->
          <div class="footer-section">
            <h4>联系我们</h4>
            <ul class="contact-info">
              <li>
                <span class="icon">📍</span>
                <span>{{ contactInfo.address }}</span>
              </li>
              <li>
                <span class="icon">📧</span>
                <span>{{ contactInfo.email }}</span>
              </li>
              <li>
                <span class="icon">⏰</span>
                <span>{{ contactInfo.workTime }}</span>
              </li>
            </ul>
          </div>
        </div>

        <div class="footer-bottom">
          <p>&copy; {{ currentYear }} {{ siteInfo.name }} (SNC). All rights reserved.</p>
          <p class="footer-motto">The best team on the campus.</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  position: relative;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: var(--bg-primary);
  margin-top: 80px;
}

.footer-wave {
  position: absolute;
  top: -15px;
  left: 0;
  width: 100%;
  overflow: hidden;
  line-height: 0;
}

.footer-wave .waves {
  position: relative;
  width: 100%;
  height: 80px;
  min-height: 60px;
  max-height: 100px;
  transform: rotate(180deg) scaleY(0.7);
}

.footer-wave .parallax > use {
  animation: move-forever 25s cubic-bezier(.55,.5,.45,.5) infinite;
  fill: rgba(255, 255, 255, 0.5);
}

.footer-wave .parallax > use:nth-child(1) {
  animation-delay: -1s;
  animation-duration: 16s;
}

.footer-wave .parallax > use:nth-child(2) {
  animation-delay: -3s;
  animation-duration: 24s;
}

.footer-wave .parallax > use:nth-child(3) {
  animation-delay: -5s;
  animation-duration: 20s;
}

.footer-wave .parallax > use:nth-child(4) {
  animation-delay: -7s;
  animation-duration: 28s;
}

@keyframes move-forever {
  0% {
    transform: translate3d(-90px, 0, 0);
  }
  100% {
    transform: translate3d(85px, 0, 0);
  }
}

.footer-content {
  padding: 120px 0 40px;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  margin-bottom: 40px;
}

.footer-section h3,
.footer-section h4 {
  font-size: 20px;
  margin-bottom: 20px;
  color: var(--bg-primary);
}

.footer-description {
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.8;
  margin-bottom: 24px;
}

.social-links {
  display: flex;
  gap: 12px;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transition: all 0.3s ease;
}

.social-link:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-4px);
}

.social-icon {
  font-size: 20px;
}

.footer-links {
  list-style: none;
}

.footer-links li {
  margin-bottom: 12px;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.9);
  transition: all 0.3s ease;
  display: inline-block;
}

.footer-links a:hover {
  color: var(--bg-primary);
  transform: translateX(4px);
}

.contact-info {
  list-style: none;
}

.contact-info li {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  color: rgba(255, 255, 255, 0.9);
}

.contact-info .icon {
  font-size: 20px;
  width: 24px;
}

.footer-bottom {
  padding-top: 40px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.footer-bottom p {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 8px;
}

.footer-motto {
  font-style: italic;
  font-size: 14px;
}

@media (max-width: 768px) {
  .footer-content {
    padding: 60px 0 30px;
  }

  .footer-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .footer-wave .waves {
    height: 40px;
    min-height: 40px;
  }
}
</style>
