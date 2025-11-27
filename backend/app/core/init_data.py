"""
数据库初始化数据
在数据库为空时自动填充示例数据
"""

from datetime import datetime, timedelta


# 示例博客文章
DEMO_BLOGS = [
    {
        "title": "Vue 3 组合式 API 深度解析",
        "excerpt": "探索 Vue 3 Composition API 的设计理念和最佳实践，学习如何使用组合式 API 构建更加灵活和可维护的应用。",
        "content": """# Vue 3 组合式 API 深度解析

## 引言

Vue 3 带来了全新的组合式 API（Composition API），它为我们提供了更灵活的代码组织方式和更好的类型推断。

## 核心概念

### 1. setup 函数

```javascript
import { ref, computed } from 'vue'

export default {
  setup() {
    const count = ref(0)
    const double = computed(() => count.value * 2)
    
    function increment() {
      count.value++
    }
    
    return { count, double, increment }
  }
}
```

### 2. 响应式 API

- **ref**: 创建响应式引用
- **reactive**: 创建响应式对象
- **computed**: 计算属性
- **watch**: 侦听器

## 总结

组合式 API 为 Vue 3 带来了更强大和灵活的开发体验。
""",
        "author": "张三",
        "date": datetime.now() - timedelta(days=5),
        "read_time": "8 分钟",
        "category": "前端开发",
        "tags": ["Vue", "JavaScript", "前端"],
        "cover": "",
        "published": True
    },
    {
        "title": "Linux 服务器性能优化指南",
        "excerpt": "从系统配置、网络调优、应用优化等多个维度，全面提升 Linux 服务器性能。",
        "content": """# Linux 服务器性能优化指南

## 系统配置优化

### 1. 内核参数调优

编辑 `/etc/sysctl.conf`：

```bash
# 增加 TCP 连接数
net.ipv4.tcp_max_syn_backlog = 8192
net.core.somaxconn = 8192

# 启用 TCP Fast Open
net.ipv4.tcp_fastopen = 3
```

### 2. 文件描述符限制

编辑 `/etc/security/limits.conf`：

```
* soft nofile 65535
* hard nofile 65535
```

## 性能监控

- **top/htop**: 实时系统监控
- **iostat**: I/O 统计
- **vmstat**: 虚拟内存统计

## 总结

服务器性能优化是一个持续的过程，需要根据实际业务场景进行针对性调整。
""",
        "author": "李四",
        "date": datetime.now() - timedelta(days=10),
        "read_time": "12 分钟",
        "category": "运维技术",
        "tags": ["Linux", "运维", "性能优化"],
        "cover": "",
        "published": True
    },
    {
        "title": "Docker 容器化部署实践",
        "excerpt": "使用 Docker 进行应用容器化的完整指南，包括镜像构建、容器编排、网络配置等核心内容。",
        "content": """# Docker 容器化部署实践

## Docker 基础

Docker 是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中。

## Dockerfile 编写

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

## Docker Compose

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
  db:
    image: mongo:latest
    volumes:
      - mongo-data:/data/db
```

## 最佳实践

1. 使用多阶段构建减小镜像体积
2. 合理使用缓存层
3. 不要在容器中存储数据
""",
        "author": "王五",
        "date": datetime.now() - timedelta(days=15),
        "read_time": "10 分钟",
        "category": "运维技术",
        "tags": ["Docker", "容器", "DevOps"],
        "cover": "",
        "published": True
    },
    {
        "title": "TypeScript 类型体操技巧",
        "excerpt": "TypeScript 高级类型技巧和实用工具类型的深入讲解，帮助你写出更加类型安全的代码。",
        "content": """# TypeScript 类型体操技巧

## 基础类型操作

### 条件类型

```typescript
type IsString<T> = T extends string ? true : false;

type A = IsString<'hello'>; // true
type B = IsString<123>; // false
```

### 映射类型

```typescript
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};
```

## 实用工具类型

- `Partial<T>`: 将所有属性变为可选
- `Required<T>`: 将所有属性变为必需
- `Pick<T, K>`: 从类型中选择指定属性
- `Omit<T, K>`: 从类型中排除指定属性

## 总结

掌握 TypeScript 的高级类型可以帮助我们写出更加健壮的代码。
""",
        "author": "赵六",
        "date": datetime.now() - timedelta(days=20),
        "read_time": "15 分钟",
        "category": "前端开发",
        "tags": ["TypeScript", "JavaScript", "类型系统"],
        "cover": "",
        "published": True
    },
    {
        "title": "Python 异步编程入门",
        "excerpt": "深入理解 Python asyncio 库，掌握异步编程的核心概念和应用场景。",
        "content": """# Python 异步编程入门

## 什么是异步编程

异步编程是一种编程范式，允许程序在等待 I/O 操作时继续执行其他任务。

## asyncio 基础

```python
import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

asyncio.run(hello())
```

## 并发执行

```python
async def main():
    tasks = [
        asyncio.create_task(fetch_data(url))
        for url in urls
    ]
    results = await asyncio.gather(*tasks)
    return results
```

## 适用场景

- 网络请求
- 文件 I/O
- 数据库操作
""",
        "author": "孙七",
        "date": datetime.now() - timedelta(days=25),
        "read_time": "11 分钟",
        "category": "后端开发",
        "tags": ["Python", "异步编程", "asyncio"],
        "cover": "",
        "published": True
    },
    {
        "title": "Git 工作流最佳实践",
        "excerpt": "介绍常见的 Git 工作流模式，包括 Git Flow、GitHub Flow 等，以及团队协作的最佳实践。",
        "content": """# Git 工作流最佳实践

## Git Flow

Git Flow 是一种经典的分支管理策略：

- `main`: 生产分支
- `develop`: 开发分支
- `feature/*`: 功能分支
- `release/*`: 发布分支
- `hotfix/*`: 热修复分支

## GitHub Flow

更简单的工作流：

1. 从 main 创建分支
2. 添加提交
3. 创建 Pull Request
4. 代码审查
5. 合并到 main

## 提交规范

```
feat: 添加新功能
fix: 修复 bug
docs: 更新文档
style: 代码格式调整
refactor: 重构代码
```
""",
        "author": "周八",
        "date": datetime.now() - timedelta(days=30),
        "read_time": "9 分钟",
        "category": "开发工具",
        "tags": ["Git", "版本控制", "团队协作"],
        "cover": "",
        "published": True
    }
]


# 示例服务
DEMO_SERVICES = [
    # 学习平台
    {
        "name": "在线课程平台",
        "description": "在线课程学习、作业提交",
        "url": "https://online.example.edu",
        "icon": "📚",
        "category": "学习平台",
        "order": 1,
        "active": True
    },
    {
        "name": "教务管理系统",
        "description": "选课、课表查询、成绩查询",
        "url": "https://jwgl.example.edu",
        "icon": "🎓",
        "category": "学习平台",
        "order": 2,
        "active": True
    },
    {
        "name": "图书馆",
        "description": "图书检索、数据库访问、座位预约",
        "url": "https://lib.example.edu",
        "icon": "📖",
        "category": "学习平台",
        "order": 3,
        "active": True
    },
    {
        "name": "雨课堂",
        "description": "智慧教学工具平台",
        "url": "https://yuketang.cn",
        "icon": "☁️",
        "category": "学习平台",
        "order": 4,
        "active": True
    },
    # 校园服务
    {
        "name": "校园VPN",
        "description": "校外访问校内资源",
        "url": "https://vpn.example.edu",
        "icon": "🔐",
        "category": "校园服务",
        "order": 1,
        "active": True
    },
    {
        "name": "学校邮箱",
        "description": "校园邮件服务",
        "url": "https://mail.example.edu",
        "icon": "✉️",
        "category": "校园服务",
        "order": 2,
        "active": True
    },
    {
        "name": "校园卡服务",
        "description": "校园卡查询、充值",
        "url": "https://card.example.edu",
        "icon": "💳",
        "category": "校园服务",
        "order": 3,
        "active": True
    },
    {
        "name": "正版软件",
        "description": "Office、WPS等正版软件下载",
        "url": "https://software.example.edu",
        "icon": "💿",
        "category": "校园服务",
        "order": 4,
        "active": True
    },
    # 开发工具
    {
        "name": "GitHub",
        "description": "代码托管与协作",
        "url": "https://github.com",
        "icon": "💻",
        "category": "开发工具",
        "order": 1,
        "active": True
    },
    {
        "name": "GitLab",
        "description": "校内Git仓库",
        "url": "https://gitlab.example.edu",
        "icon": "🦊",
        "category": "开发工具",
        "order": 2,
        "active": True
    },
    {
        "name": "VS Code",
        "description": "轻量级代码编辑器",
        "url": "https://code.visualstudio.com",
        "icon": "📝",
        "category": "开发工具",
        "order": 3,
        "active": True
    },
    {
        "name": "Stack Overflow",
        "description": "编程问答社区",
        "url": "https://stackoverflow.com",
        "icon": "❓",
        "category": "开发工具",
        "order": 4,
        "active": True
    },
    # 学习资源
    {
        "name": "课程资料库",
        "description": "各类课程学习资料",
        "url": "#",
        "icon": "📁",
        "category": "学习资源",
        "order": 1,
        "active": True
    },
    {
        "name": "MDN Web Docs",
        "description": "Web开发权威文档",
        "url": "https://developer.mozilla.org",
        "icon": "🌐",
        "category": "学习资源",
        "order": 2,
        "active": True
    },
    {
        "name": "LeetCode",
        "description": "算法练习平台",
        "url": "https://leetcode.cn",
        "icon": "🧩",
        "category": "学习资源",
        "order": 3,
        "active": True
    }
]


# 示例活动
DEMO_EVENTS = [
    {
        "title": "Web 开发技术分享会",
        "description": "深入探讨现代Web开发技术栈，包括Vue 3、React、TypeScript等前端技术，以及Node.js后端开发实践。本次分享会将由经验丰富的开发者带来实战经验分享。",
        "date": datetime.now() + timedelta(days=7),
        "location": "教学楼 A301",
        "category": "技术分享",
        "organizer": "学生网络中心",
        "status": "upcoming",
        "max_participants": 50,
        "registration_url": "",
        "published": True
    },
    {
        "title": "Linux 系统运维工作坊",
        "description": "Linux服务器配置、维护与故障排查实战。涵盖系统安装、用户管理、权限配置、网络设置、服务管理等核心内容。",
        "date": datetime.now() - timedelta(days=10),
        "location": "实验室 B205",
        "category": "工作坊",
        "organizer": "运维团队",
        "status": "completed",
        "max_participants": 30,
        "registration_url": "",
        "published": True
    },
    {
        "title": "开源项目贡献指南",
        "description": "如何参与开源项目，从提交第一个PR开始。本次讲座将介绍Git/GitHub的基本使用、如何寻找适合的开源项目、贡献流程和注意事项等。",
        "date": datetime.now() - timedelta(days=20),
        "location": "线上直播",
        "category": "讲座",
        "organizer": "开源社区",
        "status": "completed",
        "max_participants": 100,
        "registration_url": "",
        "published": True
    },
    {
        "title": "Python 数据分析入门",
        "description": "使用Python进行数据分析的基础知识，包括NumPy、Pandas、Matplotlib等常用库的使用，以及实际案例分析。",
        "date": datetime.now() + timedelta(days=14),
        "location": "计算机楼 C102",
        "category": "工作坊",
        "organizer": "数据科学小组",
        "status": "upcoming",
        "max_participants": 40,
        "registration_url": "",
        "published": True
    },
    {
        "title": "网络安全与隐私保护",
        "description": "网络安全基础知识、常见攻击手段及防护措施，个人隐私保护的最佳实践。帮助大家建立安全意识，保护个人信息安全。",
        "date": datetime.now() - timedelta(days=30),
        "location": "教学楼 A201",
        "category": "讲座",
        "organizer": "安全团队",
        "status": "completed",
        "max_participants": 60,
        "registration_url": "",
        "published": True
    }
]


# 关于我们页面数据
DEMO_ABOUT = {
    "team_members": [
        {
            "name": "张三",
            "role": "技术负责人",
            "avatar": "👨‍💻",
            "description": "全栈开发工程师，热爱开源",
            "skills": ["Vue", "Node.js", "Docker"]
        },
        {
            "name": "李四",
            "role": "运维工程师",
            "avatar": "👨‍🔧",
            "description": "Linux 系统专家",
            "skills": ["Linux", "Kubernetes", "CI/CD"]
        },
        {
            "name": "王五",
            "role": "前端开发",
            "avatar": "👩‍💻",
            "description": "用户界面设计与开发",
            "skills": ["React", "TypeScript", "UI/UX"]
        },
        {
            "name": "赵六",
            "role": "后端开发",
            "avatar": "👨‍💼",
            "description": "服务端架构设计",
            "skills": ["Python", "Django", "PostgreSQL"]
        }
    ],
    "timeline": [
        {
            "year": "2020",
            "title": "社团成立",
            "description": "学生网络中心正式成立，开始为校园提供网络服务"
        },
        {
            "year": "2021",
            "title": "服务扩展",
            "description": "推出多项新服务，用户数突破5000+"
        },
        {
            "year": "2022",
            "title": "技术创新",
            "description": "开源多个项目，举办首届技术分享会"
        },
        {
            "year": "2023",
            "title": "影响力提升",
            "description": "与多个高校技术社团建立合作关系"
        },
        {
            "year": "2024",
            "title": "持续发展",
            "description": "服务用户超过10000+，技术团队不断壮大"
        }
    ],
    "values": [
        {
            "icon": "🎯",
            "title": "追求卓越",
            "description": "不断提升技术能力，为用户提供最优质的服务"
        },
        {
            "icon": "🤝",
            "title": "团队协作",
            "description": "相互学习，共同成长，打造高效团队"
        },
        {
            "icon": "💡",
            "title": "创新精神",
            "description": "勇于尝试新技术，推动校园信息化建设"
        },
        {
            "icon": "🌍",
            "title": "开源分享",
            "description": "积极参与开源社区，分享技术经验"
        }
    ],
    "stats": [
        {"label": "服务用户", "value": "10,000+", "icon": "👥"},
        {"label": "技术文章", "value": "200+", "icon": "📝"},
        {"label": "举办活动", "value": "50+", "icon": "🎪"},
        {"label": "开源项目", "value": "30+", "icon": "💻"}
    ],
    "mission": {
        "title": "我们的使命",
        "content": "学生网络中心成立于2020年，是一个由学生自发组织的技术社团。我们的目标是为校园师生提供稳定可靠的网络服务，推动校园信息化建设，培养学生的技术能力和创新精神。通过定期举办技术讲座、工作坊和交流活动，我们为同学们创造了一个学习交流的平台。同时，我们也积极参与开源社区，贡献自己的力量。"
    },
    "contact": {
        "email": "contact@snc.example.edu",
        "github": "https://github.com/snc-example",
        "wechat": "SNC_Official",
        "qq": "123456789"
    }
}


# 默认设置
DEMO_SETTINGS = [
    {"key": "siteName", "value": "SNC Blog", "description": "网站名称"},
    {"key": "siteDescription", "value": "学生网络中心技术博客", "description": "网站描述"},
    {"key": "contactEmail", "value": "contact@snc.example.edu", "description": "联系邮箱"},
    {"key": "github", "value": "https://github.com/snc-example", "description": "GitHub地址"},
    {"key": "wechat", "value": "SNC_Official", "description": "微信公众号"},
    {"key": "qq", "value": "123456789", "description": "QQ群号"}
]


async def init_demo_data(db):
    """初始化示例数据"""
    from datetime import datetime
    
    # 检查并初始化博客
    blog_count = await db.blogs.count_documents({})
    if blog_count == 0:
        for blog in DEMO_BLOGS:
            blog["created_at"] = datetime.now()
            blog["updated_at"] = datetime.now()
        await db.blogs.insert_many(DEMO_BLOGS)
        print(f"✅ 已初始化 {len(DEMO_BLOGS)} 篇示例博客")
    
    # 检查并初始化服务
    service_count = await db.services.count_documents({})
    if service_count == 0:
        for service in DEMO_SERVICES:
            service["created_at"] = datetime.now()
        await db.services.insert_many(DEMO_SERVICES)
        print(f"✅ 已初始化 {len(DEMO_SERVICES)} 个示例服务")
    
    # 检查并初始化活动
    event_count = await db.events.count_documents({})
    if event_count == 0:
        for event in DEMO_EVENTS:
            event["created_at"] = datetime.now()
        await db.events.insert_many(DEMO_EVENTS)
        print(f"✅ 已初始化 {len(DEMO_EVENTS)} 个示例活动")
    
    # 检查并初始化设置
    settings_count = await db.settings.count_documents({})
    if settings_count == 0:
        for setting in DEMO_SETTINGS:
            setting["updated_at"] = datetime.now()
        await db.settings.insert_many(DEMO_SETTINGS)
        print(f"✅ 已初始化 {len(DEMO_SETTINGS)} 个默认设置")
    
    # 检查并初始化"关于我们"数据
    about = await db.about.find_one({})
    if not about:
        about_data = {
            **DEMO_ABOUT,
            "updated_at": datetime.now()
        }
        await db.about.insert_one(about_data)
        print("✅ 已初始化关于我们页面数据")
