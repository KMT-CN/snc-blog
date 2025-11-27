<template>
  <div class="event-editor">
    <div class="header">
      <h1>{{ isEdit ? '编辑活动' : '创建活动' }}</h1>
      <div class="actions">
        <button @click="router.back()" class="btn-secondary">取消</button>
        <button @click="saveEvent" class="btn-primary" :disabled="saving">
          {{ saving ? '保存中...' : '保存' }}
        </button>
      </div>
    </div>

    <div class="editor-form">
      <div class="form-group">
        <label>活动标题</label>
        <input v-model="form.title" type="text" placeholder="活动标题" required />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>分类</label>
          <input v-model="form.category" type="text" placeholder="分类" required />
        </div>
        <div class="form-group">
          <label>主办方</label>
          <input v-model="form.organizer" type="text" placeholder="主办方" />
        </div>
        <div class="form-group">
          <label>状态</label>
          <select v-model="form.status">
            <option value="upcoming">即将开始</option>
            <option value="ongoing">进行中</option>
            <option value="completed">已结束</option>
          </select>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>活动时间</label>
          <input v-model="form.dateInput" type="datetime-local" required />
        </div>
        <div class="form-group">
          <label>活动地点</label>
          <input v-model="form.location" type="text" placeholder="活动地点" />
        </div>
        <div class="form-group">
          <label>最大参与人数</label>
          <input v-model.number="form.max_participants" type="number" placeholder="0 表示不限" />
        </div>
      </div>

      <div class="form-group">
        <label>报名链接</label>
        <input v-model="form.registration_url" type="url" placeholder="https://..." />
      </div>

      <div class="form-group">
        <label>活动描述</label>
        <textarea v-model="form.description" rows="6" placeholder="活动描述..." required></textarea>
      </div>

      <div class="form-group">
        <label>
          <input v-model="form.published" type="checkbox" />
          发布活动
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const API_BASE = import.meta.env.VITE_API_URL || '/api'

const isEdit = computed(() => !!route.params.id)
const saving = ref(false)

const form = ref({
  title: '',
  description: '',
  date: new Date().toISOString(),
  dateInput: '',
  location: '',
  category: '',
  organizer: '',
  status: 'upcoming',
  max_participants: 0,
  registration_url: '',
  published: true
})

// 处理日期输入
watch(() => form.value.dateInput, (val) => {
  if (val) {
    form.value.date = new Date(val).toISOString()
  }
})

onMounted(async () => {
  // 设置默认日期为当前时间
  const now = new Date()
  form.value.dateInput = now.toISOString().slice(0, 16)
  
  if (isEdit.value) {
    await loadEvent()
  }
})

const loadEvent = async () => {
  try {
    const res = await fetch(`${API_BASE}/events/${route.params.id}`)
    const event = await res.json()
    form.value = { 
      ...event,
      dateInput: new Date(event.date).toISOString().slice(0, 16)
    }
  } catch (error) {
    console.error('加载活动失败:', error)
  }
}

const saveEvent = async () => {
  saving.value = true

  try {
    const token = localStorage.getItem('admin_token')
    const method = isEdit.value ? 'PUT' : 'POST'
    const url = isEdit.value 
      ? `${API_BASE}/events/${route.params.id}`
      : `${API_BASE}/events`

    // 准备提交数据，移除 dateInput
    const submitData = { ...form.value }
    delete (submitData as any).dateInput

    const res = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(submitData)
    })

    if (res.ok) {
      router.push('/admin/events')
    } else {
      const error = await res.json()
      alert('保存失败: ' + (error.detail || '未知错误'))
    }
  } catch (error) {
    console.error('保存活动失败:', error)
    alert('保存失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.event-editor {
  max-width: 800px;
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

.actions {
  display: flex;
  gap: 1rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e5e5e5;
  color: #333;
}

.btn-secondary:hover {
  background: #d4d4d4;
}

.editor-form {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-group input[type="text"],
.form-group input[type="url"],
.form-group input[type="number"],
.form-group input[type="datetime-local"],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.form-group input[type="checkbox"] {
  margin-right: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
