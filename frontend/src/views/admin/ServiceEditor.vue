<template>
  <div class="service-editor">
    <div class="header">
      <h1>{{ isEdit ? '编辑服务' : '添加服务' }}</h1>
      <div class="actions">
        <button @click="router.back()" class="btn-secondary">取消</button>
        <button @click="saveService" class="btn-primary" :disabled="saving">
          {{ saving ? '保存中...' : '保存' }}
        </button>
      </div>
    </div>

    <div class="editor-form">
      <div class="form-group">
        <label>服务名称</label>
        <input v-model="form.name" type="text" placeholder="服务名称" required />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>图标（Emoji）</label>
          <input v-model="form.icon" type="text" placeholder="🔗" />
        </div>
        <div class="form-group">
          <label>分类</label>
          <input v-model="form.category" type="text" placeholder="分类" required />
        </div>
        <div class="form-group">
          <label>排序</label>
          <input v-model.number="form.order" type="number" placeholder="0" />
        </div>
      </div>

      <div class="form-group">
        <label>链接地址</label>
        <input v-model="form.url" type="url" placeholder="https://..." required />
      </div>

      <div class="form-group">
        <label>描述</label>
        <textarea v-model="form.description" rows="4" placeholder="服务描述..." required></textarea>
      </div>

      <div class="form-group">
        <label>
          <input v-model="form.active" type="checkbox" />
          启用服务
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const API_BASE = import.meta.env.VITE_API_URL || '/api'

const isEdit = computed(() => !!route.params.id)
const saving = ref(false)

const form = ref({
  name: '',
  description: '',
  url: '',
  icon: '🔗',
  category: '',
  order: 0,
  active: true
})

onMounted(async () => {
  if (isEdit.value) {
    await loadService()
  }
})

const loadService = async () => {
  try {
    const res = await fetch(`${API_BASE}/services/${route.params.id}`)
    if (res.ok) {
      const service = await res.json()
      form.value = { ...service }
    } else {
      console.error('服务不存在')
      router.push('/admin/services')
    }
  } catch (error) {
    console.error('加载服务失败:', error)
  }
}

const saveService = async () => {
  saving.value = true

  try {
    const token = localStorage.getItem('admin_token')
    const method = isEdit.value ? 'PUT' : 'POST'
    const url = isEdit.value 
      ? `${API_BASE}/services/${route.params.id}`
      : `${API_BASE}/services`

    const res = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(form.value)
    })

    if (res.ok) {
      router.push('/admin/services')
    } else {
      alert('保存失败')
    }
  } catch (error) {
    console.error('保存服务失败:', error)
    alert('保存失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.service-editor {
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
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
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
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #06b6d4;
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
