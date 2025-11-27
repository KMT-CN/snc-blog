<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

interface Service {
  _id?: string
  id?: number
  name: string
  description: string
  url: string
  icon: string
  category: string
}

// 默认服务数据
const defaultServices: Service[] = [
  // 学习平台
  {
    id: 1,
    name: '在线课程平台',
    description: '在线课程学习、作业提交',
    url: 'https://online.example.edu',
    icon: '📚',
    category: '学习平台'
  },
  {
    id: 2,
    name: '教务管理系统',
    description: '选课、课表查询、成绩查询',
    url: 'https://jwgl.example.edu',
    icon: '🎓',
    category: '学习平台'
  },
  {
    id: 3,
    name: '图书馆',
    description: '图书检索、数据库访问、座位预约',
    url: 'https://lib.example.edu',
    icon: '📖',
    category: '学习平台'
  },
  // 校园服务
  {
    id: 5,
    name: '校园VPN',
    description: '校外访问校内资源',
    url: 'https://vpn.example.edu',
    icon: '🔐',
    category: '校园服务'
  },
  {
    id: 6,
    name: '学校邮箱',
    description: '校园邮件服务',
    url: 'https://mail.example.edu',
    icon: '✉️',
    category: '校园服务'
  },
  // 开发工具
  {
    id: 9,
    name: 'GitHub',
    description: '代码托管与协作',
    url: 'https://github.com',
    icon: '💻',
    category: '开发工具'
  },
  {
    id: 11,
    name: 'VS Code',
    description: '轻量级代码编辑器',
    url: 'https://code.visualstudio.com',
    icon: '📝',
    category: '开发工具'
  },
  // 学习资源
  {
    id: 15,
    name: 'MDN Web Docs',
    description: 'Web开发权威文档',
    url: 'https://developer.mozilla.org',
    icon: '🌐',
    category: '学习资源'
  },
  {
    id: 16,
    name: 'LeetCode',
    description: '算法练习平台',
    url: 'https://leetcode.cn',
    icon: '🧩',
    category: '学习资源'
  }
]

const services = ref<Service[]>([])
const loading = ref(true)

// 从后端加载服务
onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/services?active=true`)
    if (res.ok) {
      const data = await res.json()
      if (data && data.length > 0) {
        services.value = data
      } else {
        services.value = defaultServices
      }
    } else {
      services.value = defaultServices
    }
  } catch (error) {
    console.error('加载服务失败:', error)
    services.value = defaultServices
  } finally {
    loading.value = false
  }
})

const categories = computed(() => {
  const cats = new Set(services.value.map(s => s.category))
  return ['全部', ...Array.from(cats)]
})

const selectedCategory = ref('全部')

const filteredServices = computed(() => {
  if (selectedCategory.value === '全部') {
    return services.value
  }
  return services.value.filter(s => s.category === selectedCategory.value)
})

const groupedServices = computed(() => {
  const groups: Record<string, Service[]> = {}
  filteredServices.value.forEach(service => {
    if (!groups[service.category]) {
      groups[service.category] = []
    }
    groups[service.category].push(service)
  })
  return groups
})
</script>

<template>
  <div class="services-page">
    <!-- Page Header -->
    <section class="page-header">
      <div class="container">
        <h1 class="page-title fade-in">服务导航</h1>
        <p class="page-subtitle fade-in">快速访问常用服务和工具</p>
      </div>
    </section>

    <!-- Category Filter -->
    <section class="category-section">
      <div class="container">
        <div class="category-tabs">
          <button
            v-for="category in categories"
            :key="category"
            class="category-tab"
            :class="{ active: selectedCategory === category }"
            @click="selectedCategory = category"
          >
            {{ category }}
          </button>
        </div>
      </div>
    </section>

    <!-- Services Grid -->
    <section class="services-content">
      <div class="container">
        <div v-if="selectedCategory === '全部'">
          <div
            v-for="(serviceList, category) in groupedServices"
            :key="category"
            class="service-group"
          >
            <h2 class="group-title">{{ category }}</h2>
            <div class="services-grid">
              <a
                v-for="service in serviceList"
                :key="service.id"
                :href="service.url"
                target="_blank"
                rel="noopener noreferrer"
                class="service-card card"
              >
                <div class="service-icon">{{ service.icon }}</div>
                <h3 class="service-name">{{ service.name }}</h3>
                <p class="service-description">{{ service.description }}</p>
                <span class="service-arrow">→</span>
              </a>
            </div>
          </div>
        </div>

        <div v-else class="services-grid">
          <a
            v-for="service in filteredServices"
            :key="service.id"
            :href="service.url"
            target="_blank"
            rel="noopener noreferrer"
            class="service-card card"
          >
            <div class="service-icon">{{ service.icon }}</div>
            <h3 class="service-name">{{ service.name }}</h3>
            <p class="service-description">{{ service.description }}</p>
            <span class="service-arrow">→</span>
          </a>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-header {
  padding: 80px 0 60px;
  text-align: center;
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
  color: var(--bg-primary);
}

.page-title {
  font-size: 3rem;
  margin-bottom: 16px;
}

.page-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  color: var(--bg-primary);
}

/* Category Section */
.category-section {
  padding: 40px 0;
  background: var(--bg-primary);
  position: sticky;
  top: 70px;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.category-tabs {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.category-tab {
  padding: 10px 20px;
  border: 2px solid var(--primary-color);
  background: white;
  color: var(--primary-color);
  border-radius: var(--radius-lg);
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-tab:hover {
  background: var(--primary-light);
  color: white;
  border-color: var(--primary-light);
}

.category-tab.active {
  background: var(--primary-color);
  color: white;
}

/* Services Content */
.services-content {
  padding: 60px 0 80px;
}

.service-group {
  margin-bottom: 60px;
}

.group-title {
  font-size: 1.75rem;
  margin-bottom: 32px;
  color: var(--text-primary);
  padding-bottom: 16px;
  border-bottom: 2px solid var(--primary-color);
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.service-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 32px 24px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.service-card:hover {
  border-color: var(--primary-color);
  transform: translateY(-8px);
}

.service-icon {
  font-size: 3.5rem;
  margin-bottom: 20px;
  transition: transform 0.3s ease;
}

.service-card:hover .service-icon {
  transform: scale(1.1);
}

.service-name {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.service-description {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 16px;
}

.service-arrow {
  position: absolute;
  bottom: 20px;
  right: 24px;
  font-size: 1.5rem;
  color: var(--primary-color);
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}

.service-card:hover .service-arrow {
  opacity: 1;
  transform: translateX(0);
}

/* 响应式 */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .category-section {
    top: 60px;
    padding: 20px 0;
  }

  .category-tabs {
    gap: 8px;
  }

  .category-tab {
    padding: 8px 16px;
    font-size: 14px;
  }

  .services-grid {
    grid-template-columns: 1fr;
  }

  .group-title {
    font-size: 1.5rem;
  }
}
</style>
