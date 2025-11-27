<template>
  <div class="event-manage">
    <div class="header">
      <h1>活动管理</h1>
      <router-link to="/admin/events/new" class="btn-primary">
        ➕ 创建活动
      </router-link>
    </div>

    <div class="filters">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="搜索活动..."
        class="search-input"
      />
      <select v-model="filterCategory" class="filter-select">
        <option value="">全部分类</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
      <select v-model="filterStatus" class="filter-select">
        <option value="">全部状态</option>
        <option value="upcoming">即将开始</option>
        <option value="ongoing">进行中</option>
        <option value="completed">已结束</option>
      </select>
    </div>

    <div class="event-list">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="filteredEvents.length === 0" class="empty">暂无活动</div>
      <div v-else class="event-items">
        <div v-for="event in filteredEvents" :key="event._id" class="event-item">
          <div class="event-info">
            <h3>{{ event.title }}</h3>
            <p class="description">{{ event.description }}</p>
            <div class="meta">
              <span class="category">{{ event.category }}</span>
              <span class="date">📅 {{ formatDate(event.date) }}</span>
              <span class="location" v-if="event.location">📍 {{ event.location }}</span>
              <span :class="['status', event.status]">
                {{ statusText(event.status) }}
              </span>
              <span :class="['publish-status', event.published ? 'published' : 'draft']">
                {{ event.published ? '已发布' : '草稿' }}
              </span>
            </div>
          </div>
          <div class="event-actions">
            <router-link :to="`/admin/events/edit/${event._id}`" class="btn-edit">
              编辑
            </router-link>
            <button @click="deleteEvent(event._id)" class="btn-delete">
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

const events = ref<any[]>([])
const loading = ref(true)
const searchQuery = ref('')
const filterCategory = ref('')
const filterStatus = ref('')

const categories = computed(() => {
  const cats = new Set(events.value.map(e => e.category))
  return Array.from(cats)
})

const filteredEvents = computed(() => {
  return events.value.filter(event => {
    const matchesSearch = !searchQuery.value || 
      event.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      event.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesCategory = !filterCategory.value || event.category === filterCategory.value
    const matchesStatus = !filterStatus.value || event.status === filterStatus.value
    
    return matchesSearch && matchesCategory && matchesStatus
  })
})

onMounted(async () => {
  await loadEvents()
})

const loadEvents = async () => {
  try {
    const token = localStorage.getItem('admin_token')
    const res = await fetch(`${API_BASE}/events?published=false`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    events.value = await res.json()
  } catch (error) {
    console.error('加载活动失败:', error)
  } finally {
    loading.value = false
  }
}

const deleteEvent = async (id: string) => {
  if (!confirm('确定要删除这个活动吗？')) return

  try {
    const token = localStorage.getItem('admin_token')
    const res = await fetch(`${API_BASE}/events/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (res.ok) {
      events.value = events.value.filter(e => e._id !== id)
    }
  } catch (error) {
    console.error('删除活动失败:', error)
  }
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const statusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'upcoming': '即将开始',
    'ongoing': '进行中',
    'completed': '已结束'
  }
  return statusMap[status] || status
}
</script>

<style scoped>
.event-manage {
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
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
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
  flex-wrap: wrap;
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
  min-width: 200px;
}

.filter-select {
  min-width: 150px;
}

.event-list {
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

.event-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.event-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: box-shadow 0.3s;
}

.event-item:hover {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.event-info {
  flex: 1;
}

.event-info h3 {
  font-size: 1.25rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.description {
  color: #666;
  margin-bottom: 0.75rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  flex-wrap: wrap;
  align-items: center;
}

.category {
  background: #f5f5f5;
  color: var(--primary-color);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
}

.date,
.location {
  color: #666;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
}

.status.upcoming {
  background: #fef3c7;
  color: #d97706;
}

.status.ongoing {
  background: #d1fae5;
  color: #047857;
}

.status.completed {
  background: #e5e7eb;
  color: #6b7280;
}

.publish-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
}

.publish-status.published {
  background: #d1fae5;
  color: #047857;
}

.publish-status.draft {
  background: #fee2e2;
  color: #b91c1c;
}

.event-actions {
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
  background: #f5f5f5;
  color: var(--primary-color);
  text-decoration: none;
}

.btn-edit:hover {
  background: #e0e0e0;
}

.btn-delete {
  background: #fee2e2;
  color: #b91c1c;
}

.btn-delete:hover {
  background: #fecaca;
}
</style>
