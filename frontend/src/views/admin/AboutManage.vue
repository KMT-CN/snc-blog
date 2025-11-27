<template>
  <div class="about-manage">
    <h1>关于我们管理</h1>

    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.key"
        :class="['tab', { active: activeTab === tab.key }]"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- 团队成员 -->
    <div v-if="activeTab === 'team'" class="section">
      <div class="section-header">
        <h2>团队成员</h2>
        <button @click="addTeamMember" class="btn-add">➕ 添加成员</button>
      </div>
      <div class="items-list">
        <div v-for="(member, index) in teamMembers" :key="index" class="item-card">
          <div class="item-header">
            <span class="item-avatar">{{ member.avatar }}</span>
            <input v-model="member.name" placeholder="姓名" class="input-name" />
            <button @click="removeTeamMember(index)" class="btn-remove">🗑️</button>
          </div>
          <input v-model="member.role" placeholder="职位" class="input-full" />
          <input v-model="member.description" placeholder="描述" class="input-full" />
          <input v-model="member.avatar" placeholder="头像 Emoji" class="input-full" />
          <input v-model="skillsInput[index]" placeholder="技能（用逗号分隔）" class="input-full" 
                 @input="updateSkills(index, $event)" />
        </div>
      </div>
    </div>

    <!-- 发展历程 -->
    <div v-if="activeTab === 'timeline'" class="section">
      <div class="section-header">
        <h2>发展历程</h2>
        <button @click="addTimeline" class="btn-add">➕ 添加里程碑</button>
      </div>
      <div class="items-list">
        <div v-for="(item, index) in timeline" :key="index" class="item-card">
          <div class="item-header">
            <input v-model="item.year" placeholder="年份" class="input-year" />
            <input v-model="item.title" placeholder="标题" class="input-title" />
            <button @click="removeTimeline(index)" class="btn-remove">🗑️</button>
          </div>
          <textarea v-model="item.description" placeholder="描述" rows="2" class="input-full"></textarea>
        </div>
      </div>
    </div>

    <!-- 核心价值观 -->
    <div v-if="activeTab === 'values'" class="section">
      <div class="section-header">
        <h2>核心价值观</h2>
        <button @click="addValue" class="btn-add">➕ 添加价值观</button>
      </div>
      <div class="items-list">
        <div v-for="(value, index) in values" :key="index" class="item-card">
          <div class="item-header">
            <input v-model="value.icon" placeholder="图标" class="input-icon" />
            <input v-model="value.title" placeholder="标题" class="input-title" />
            <button @click="removeValue(index)" class="btn-remove">🗑️</button>
          </div>
          <textarea v-model="value.description" placeholder="描述" rows="2" class="input-full"></textarea>
        </div>
      </div>
    </div>

    <!-- 统计数据 -->
    <div v-if="activeTab === 'stats'" class="section">
      <div class="section-header">
        <h2>统计数据</h2>
        <button @click="addStat" class="btn-add">➕ 添加统计</button>
      </div>
      <div class="items-list stats-grid">
        <div v-for="(stat, index) in stats" :key="index" class="stat-card">
          <input v-model="stat.icon" placeholder="图标" class="input-icon" />
          <input v-model="stat.value" placeholder="数值" class="input-value" />
          <input v-model="stat.label" placeholder="标签" class="input-label" />
          <button @click="removeStat(index)" class="btn-remove-small">🗑️</button>
        </div>
      </div>
    </div>

    <!-- 使命与联系方式 -->
    <div v-if="activeTab === 'mission'" class="section">
      <div class="section-header">
        <h2>使命与联系方式</h2>
      </div>
      <div class="mission-form">
        <div class="form-group">
          <label>使命标题</label>
          <input v-model="mission.title" placeholder="我们的使命" class="input-full" />
        </div>
        <div class="form-group">
          <label>使命内容</label>
          <textarea v-model="mission.content" rows="5" placeholder="使命描述..." class="input-full"></textarea>
        </div>
        <h3>联系方式</h3>
        <div class="form-row">
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="contact.email" type="email" placeholder="contact@example.com" />
          </div>
          <div class="form-group">
            <label>GitHub</label>
            <input v-model="contact.github" placeholder="https://github.com/..." />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>微信公众号</label>
            <input v-model="contact.wechat" placeholder="公众号ID" />
          </div>
          <div class="form-group">
            <label>QQ群</label>
            <input v-model="contact.qq" placeholder="QQ群号" />
          </div>
        </div>
      </div>
    </div>

    <div class="actions">
      <button @click="saveAll" class="btn-primary" :disabled="saving">
        {{ saving ? '保存中...' : '保存所有更改' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

const tabs = [
  { key: 'team', label: '团队成员' },
  { key: 'timeline', label: '发展历程' },
  { key: 'values', label: '核心价值观' },
  { key: 'stats', label: '统计数据' },
  { key: 'mission', label: '使命与联系' }
]

const activeTab = ref('team')
const saving = ref(false)

const teamMembers = ref<any[]>([])
const timeline = ref<any[]>([])
const values = ref<any[]>([])
const stats = ref<any[]>([])
const mission = ref({ title: '', content: '' })
const contact = ref({ email: '', github: '', wechat: '', qq: '' })

// 用于处理技能输入
const skillsInput = ref<string[]>([])

// 监听团队成员变化，更新技能输入
watch(teamMembers, (members) => {
  skillsInput.value = members.map(m => (m.skills || []).join(', '))
}, { deep: true, immediate: true })

const updateSkills = (index: number, event: Event) => {
  const value = (event.target as HTMLInputElement).value
  teamMembers.value[index].skills = value.split(',').map(s => s.trim()).filter(Boolean)
}

onMounted(async () => {
  await loadData()
})

const loadData = async () => {
  try {
    const res = await fetch(`${API_BASE}/about`)
    if (res.ok) {
      const data = await res.json()
      if (data.team_members) teamMembers.value = data.team_members
      if (data.timeline) timeline.value = data.timeline
      if (data.values) values.value = data.values
      if (data.stats) stats.value = data.stats
      if (data.mission) mission.value = data.mission
      if (data.contact) contact.value = data.contact
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

// 团队成员操作
const addTeamMember = () => {
  teamMembers.value.push({
    name: '',
    role: '',
    avatar: '👤',
    description: '',
    skills: []
  })
}

const removeTeamMember = (index: number) => {
  teamMembers.value.splice(index, 1)
}

// 发展历程操作
const addTimeline = () => {
  timeline.value.push({
    year: new Date().getFullYear().toString(),
    title: '',
    description: ''
  })
}

const removeTimeline = (index: number) => {
  timeline.value.splice(index, 1)
}

// 价值观操作
const addValue = () => {
  values.value.push({
    icon: '⭐',
    title: '',
    description: ''
  })
}

const removeValue = (index: number) => {
  values.value.splice(index, 1)
}

// 统计数据操作
const addStat = () => {
  stats.value.push({
    icon: '📊',
    value: '0',
    label: ''
  })
}

const removeStat = (index: number) => {
  stats.value.splice(index, 1)
}

// 保存所有数据
const saveAll = async () => {
  saving.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    const res = await fetch(`${API_BASE}/about`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        team_members: teamMembers.value,
        timeline: timeline.value,
        values: values.value,
        stats: stats.value,
        mission: mission.value,
        contact: contact.value
      })
    })
    
    if (res.ok) {
      alert('保存成功！')
    } else {
      const error = await res.json()
      alert('保存失败: ' + (error.detail || '未知错误'))
    }
  } catch (error) {
    console.error('保存失败:', error)
    alert('保存失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.about-manage {
  max-width: 1000px;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.tab {
  padding: 0.75rem 1.5rem;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.tab:hover {
  border-color: var(--primary-color);
}

.tab.active {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
  color: white;
  border-color: transparent;
}

.section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e0e0e0;
}

.section-header h2 {
  font-size: 1.25rem;
  color: #333;
}

.btn-add {
  padding: 0.5rem 1rem;
  background: #f5f5f5;
  color: var(--primary-color);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.btn-add:hover {
  background: #e0e0e0;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.item-card {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.item-avatar {
  font-size: 1.5rem;
}

.input-name {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-weight: 600;
}

.input-year {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-weight: 600;
}

.input-icon {
  width: 60px;
  padding: 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  text-align: center;
  font-size: 1.25rem;
}

.input-title {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-weight: 500;
}

.input-full {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.btn-remove {
  padding: 0.25rem 0.5rem;
  background: #fee2e2;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-remove:hover {
  background: #fecaca;
}

/* 统计数据网格 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: relative;
}

.input-value {
  font-size: 1.25rem;
  font-weight: 600;
  padding: 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.input-label {
  padding: 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.btn-remove-small {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  padding: 0.25rem;
  background: transparent;
  border: none;
  cursor: pointer;
  opacity: 0.5;
}

.btn-remove-small:hover {
  opacity: 1;
}

/* 使命表单 */
.mission-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.mission-form h3 {
  margin-top: 1rem;
  color: #333;
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
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

/* 保存按钮 */
.actions {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
