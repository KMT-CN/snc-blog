<template>
  <div class="settings-manage">
    <h1>系统设置</h1>

    <div class="settings-sections">
      <!-- 网站基本信息 -->
      <div class="settings-section">
        <h2>网站信息</h2>
        <div class="settings-form">
          <div class="form-group">
            <label>网站名称</label>
            <input v-model="settings.siteName" type="text" placeholder="学生网络中心" />
          </div>
          <div class="form-group">
            <label>网站描述</label>
            <textarea v-model="settings.siteDescription" rows="3" placeholder="网站描述..."></textarea>
          </div>
        </div>
      </div>

      <!-- 联系信息 -->
      <div class="settings-section">
        <h2>联系信息</h2>
        <div class="settings-form">
          <div class="form-group">
            <label>联系邮箱</label>
            <input v-model="settings.contactEmail" type="email" placeholder="admin@example.com" />
          </div>
          <div class="form-group">
            <label>地址</label>
            <input v-model="settings.address" type="text" placeholder="XX大学 信息中心" />
          </div>
          <div class="form-group">
            <label>工作时间</label>
            <input v-model="settings.workTime" type="text" placeholder="周一至周五 9:00-17:00" />
          </div>
          <div class="form-group">
            <label>联系电话</label>
            <input v-model="settings.phone" type="text" placeholder="010-12345678" />
          </div>
        </div>
      </div>

      <!-- 社交媒体 -->
      <div class="settings-section">
        <h2>社交媒体</h2>
        <div class="settings-form">
          <div class="form-group">
            <label>GitHub</label>
            <input v-model="settings.github" type="url" placeholder="https://github.com/..." />
          </div>
          <div class="form-group">
            <label>微信公众号</label>
            <input v-model="settings.wechat" type="text" placeholder="公众号ID" />
          </div>
          <div class="form-group">
            <label>QQ群</label>
            <input v-model="settings.qq" type="text" placeholder="QQ群号" />
          </div>
        </div>
      </div>

      <!-- 管理员账户 -->
      <div class="settings-section">
        <h2>修改密码</h2>
        <div class="settings-form">
          <div class="form-group">
            <label>当前密码</label>
            <input v-model="passwordForm.currentPassword" type="password" placeholder="当前密码" />
          </div>
          <div class="form-group">
            <label>新密码</label>
            <input v-model="passwordForm.newPassword" type="password" placeholder="新密码" />
          </div>
          <div class="form-group">
            <label>确认新密码</label>
            <input v-model="passwordForm.confirmPassword" type="password" placeholder="确认新密码" />
          </div>
          <button @click="changePassword" class="btn-secondary" :disabled="changingPassword">
            {{ changingPassword ? '修改中...' : '修改密码' }}
          </button>
        </div>
      </div>
    </div>

    <div class="actions">
      <button @click="saveSettings" class="btn-primary" :disabled="saving">
        {{ saving ? '保存中...' : '保存设置' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

const saving = ref(false)
const changingPassword = ref(false)

const settings = ref({
  siteName: '学生网络中心',
  siteDescription: '',
  contactEmail: '',
  address: '',
  workTime: '',
  phone: '',
  github: '',
  wechat: '',
  qq: ''
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

onMounted(async () => {
  await loadSettings()
})

const loadSettings = async () => {
  try {
    const res = await fetch(`${API_BASE}/settings/`)
    const data = await res.json()
    
    // 合并已有设置
    if (data.siteName) settings.value.siteName = data.siteName
    if (data.siteDescription) settings.value.siteDescription = data.siteDescription
    if (data.contactEmail) settings.value.contactEmail = data.contactEmail
    if (data.address) settings.value.address = data.address
    if (data.workTime) settings.value.workTime = data.workTime
    if (data.phone) settings.value.phone = data.phone
    if (data.github) settings.value.github = data.github
    if (data.wechat) settings.value.wechat = data.wechat
    if (data.qq) settings.value.qq = data.qq
  } catch (error) {
    console.error('加载设置失败:', error)
  }
}

const saveSettings = async () => {
  saving.value = true

  try {
    const token = localStorage.getItem('admin_token')
    
    // 保存每个设置
    for (const [key, value] of Object.entries(settings.value)) {
      await fetch(`${API_BASE}/settings/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ key, value, description: '' })
      })
    }

    alert('设置保存成功')
  } catch (error) {
    console.error('保存设置失败:', error)
    alert('保存失败')
  } finally {
    saving.value = false
  }
}

const changePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }

  if (passwordForm.value.newPassword.length < 6) {
    alert('密码长度至少6位')
    return
  }

  changingPassword.value = true

  try {
    const token = localStorage.getItem('admin_token')
    const res = await fetch(`${API_BASE}/auth/change-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        current_password: passwordForm.value.currentPassword,
        new_password: passwordForm.value.newPassword
      })
    })

    if (res.ok) {
      alert('密码修改成功')
      passwordForm.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    } else {
      const error = await res.json()
      alert('修改失败: ' + (error.detail || '未知错误'))
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    alert('修改失败')
  } finally {
    changingPassword.value = false
  }
}
</script>

<style scoped>
.settings-manage {
  max-width: 800px;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.settings-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.settings-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.settings-section h2 {
  font-size: 1.25rem;
  color: #333;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e0e0e0;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.actions {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
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

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e5e5e5;
  color: #333;
}

.btn-secondary:hover:not(:disabled) {
  background: #d4d4d4;
}
</style>
