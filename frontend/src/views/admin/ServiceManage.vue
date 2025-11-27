<template>
  <div class="service-manage">
    <div class="header">
      <h1>服务管理</h1>
      <router-link to="/admin/services/new" class="btn-primary">
        ➕ 添加服务
      </router-link>
    </div>

    <div class="filters">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="搜索服务..."
        class="search-input"
      />
      <select v-model="filterCategory" class="filter-select">
        <option value="">全部分类</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
    </div>

    <div class="service-list">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="filteredServices.length === 0" class="empty">暂无服务</div>
      <div v-else class="service-items">
        <div v-for="service in filteredServices" :key="service._id" class="service-item">
          <div class="service-info">
            <div class="service-header">
              <span class="service-icon">{{ service.icon }}</span>
              <h3>{{ service.name }}</h3>
            </div>
            <p class="description">{{ service.description }}</p>
            <div class="meta">
              <span class="category">{{ service.category }}</span>
              <a :href="service.url" target="_blank" class="url">{{ service.url }}</a>
              <span :class="['status', service.active ? 'active' : 'inactive']">
                {{ service.active ? '启用' : '禁用' }}
              </span>
            </div>
          </div>
          <div class="service-actions">
            <router-link :to="`/admin/services/edit/${service._id}`" class="btn-edit">
              编辑
            </router-link>
            <button @click="deleteService(service._id)" class="btn-delete">
              删除
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

const services = ref<any[]>([])
const loading = ref(true)
const searchQuery = ref('')
const filterCategory = ref('')

const categories = computed(() => {
  const cats = new Set(services.value.map(s => s.category))
  return Array.from(cats)
})

const filteredServices = computed(() => {
  return services.value.filter(service => {
    const matchesSearch = !searchQuery.value || 
      service.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      service.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesCategory = !filterCategory.value || service.category === filterCategory.value
    
    return matchesSearch && matchesCategory
  })
})

onMounted(async () => {
  await loadServices()
})

const loadServices = async () => {
  try {
    const token = localStorage.getItem('admin_token')
    const res = await fetch(`${API_BASE}/services?active=false`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    services.value = await res.json()
  } catch (error) {
    console.error('加载服务失败:', error)
  } finally {
    loading.value = false
  }
}

const deleteService = async (id: string) => {
  if (!confirm('确定要删除这个服务吗？')) return

  try {
    const token = localStorage.getItem('admin_token')
    const res = await fetch(`${API_BASE}/services/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (res.ok) {
      services.value = services.value.filter(s => s._id !== id)
    }
  } catch (error) {
    console.error('删除服务失败:', error)
  }
}
</script>

<style scoped>
.service-manage {
  max-width: 1200px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2rem;
  color: #333;
}

.btn-primary {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-input,
.filter-select {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
}

.search-input {
  flex: 1;
}

.filter-select {
  min-width: 150px;
}

.service-list {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.loading,
.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.service-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.service-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: box-shadow 0.3s;
}

.service-item:hover {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.service-info {
  flex: 1;
}

.service-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.service-icon {
  font-size: 1.5rem;
}

.service-info h3 {
  font-size: 1.25rem;
  color: #333;
}

.description {
  color: #666;
  margin-bottom: 0.75rem;
}

.meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  flex-wrap: wrap;
  align-items: center;
}

.category {
  background: #e0f2fe;
  color: #0891b2;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
}

.url {
  color: #666;
  text-decoration: none;
}

.url:hover {
  color: #0891b2;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
}

.status.active {
  background: #d1fae5;
  color: #047857;
}

.status.inactive {
  background: #fee2e2;
  color: #b91c1c;
}

.service-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit,
.btn-delete {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background 0.3s;
  border: none;
}

.btn-edit {
  background: #e0f2fe;
  color: #0891b2;
  text-decoration: none;
}

.btn-edit:hover {
  background: #bae6fd;
}

.btn-delete {
  background: #fee2e2;
  color: #b91c1c;
}

.btn-delete:hover {
  background: #fecaca;
}
</style>
