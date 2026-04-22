# 双赛道情报通 - 产品说明书

## 一、产品概述

双赛道情报通是一款面向考研和考公学生的资讯推送服务系统，为用户提供及时、准确的考研和考公相关资讯，帮助用户掌握最新考试动态。

### 产品定位
- **目标用户**：考研学生、考公学生、同时准备考研和考公的用户
- **核心价值**：及时推送考研/考公资讯，让用户不错过任何重要信息
- **服务形式**：微信小程序 + 管理后台

---

## 二、系统架构

### 技术栈
- **后端**：Python + FastAPI + MySQL + Redis + Celery
- **前端**：Vue3 + Element Plus + Vite
- **小程序**：微信小程序原生开发
- **任务队列**：Celery + Redis

### 项目结构
```
考研考公双赛道情报监控系统/
├── backend/               # 后端服务
│   ├── api/v1/          # API接口
│   ├── core/            # 核心模块
│   ├── models/          # 数据模型
│   └── schemas/         # 数据验证
├── frontend/             # 管理后台前端
│   ├── src/views/       # 页面组件
│   └── src/components/  # 公共组件
├── kaoyankaogong-weapp/ # 微信小程序
└── docs/                # 文档
```

---

## 三、功能模块

### 1. 用户模块

#### 1.1 用户注册
- 支持手机号注册
- 支持邮箱注册
- 支持设置考研/考公需求
- 注册成功后发送欢迎邮件（包含原始密码）

#### 1.2 用户登录
- 手机号密码登录
- 邮箱密码登录
- Token认证
- 密码修改功能

#### 1.3 用户管理（管理后台）
- 用户列表查看
- 用户详情查看
- 用户搜索（按用户名/邮箱/手机号）
- 用户删除

### 2. 资讯模块

#### 2.1 考研资讯
- 资讯列表展示
- 资讯分类筛选
- 资讯搜索
- 资讯管理（增删改查）

#### 2.2 考公资讯
- 资讯列表展示
- 资讯分类筛选
- 资讯搜索
- 资讯管理（增删改查）

### 3. 推送模块

#### 3.1 推送设置
- 用户可以设置关注省份
- 用户可以设置关注学校
- 用户可以设置关注专业
- 用户可以设置关键词

#### 3.2 推送历史
- 推送记录列表
- 推送记录删除
- 推送统计

#### 3.3 推送方式
- 邮件推送
- 短信推送（预留）
- 微信服务通知（预留）

### 4. 支付模块

#### 4.1 产品管理
- 产品列表
- 产品创建
- 产品编辑
- 产品删除
- 产品类型：考研、考公、考研+考公

#### 4.2 订单管理
- 订单创建
- 订单支付（模拟支付/微信支付/支付宝支付）
- 订单查询
- 订单取消

#### 4.3 支付方式
- 模拟支付（测试用）
- 微信支付
- 支付宝支付

### 5. 学习资料模块

#### 5.1 资料管理
- 资料分类
- 资料上传
- 资料下载

#### 5.2 用户下载记录
- 下载历史
- 下载统计

### 6. 反馈模块

#### 6.1 用户反馈
- 提交反馈
- 反馈列表查看
- 反馈处理状态

### 7. 爬虫模块

#### 7.1 考研爬虫
- 爬虫配置
- 爬虫启动/停止
- 爬虫日志

#### 7.2 考公爬虫
- 爬虫配置
- 爬虫启动/停止
- 爬虫日志

### 8. 系统管理

#### 8.1 系统配置
- 基本配置
- 邮件配置
- 微信配置
- 支付宝配置

#### 8.2 学校管理
- 学校库管理
- 专业管理

---

## 四、用户使用流程

### 4.1 游客流程
1. 访问首页 → 查看资讯
2. 填写需求表单 → 创建订单
3. 完成支付 → 开通VIP
4. 登录小程序 → 接收推送

### 4.2 用户流程
1. 登录小程序/管理后台
2. 设置推送需求（省份、学校、专业、关键词）
3. 接收推送通知
4. 查看资讯详情

### 4.3 管理员流程
1. 登录管理后台
2. 管理用户
3. 管理资讯
4. 管理订单
5. 配置爬虫
6. 查看统计数据

---

## 五、接口清单

### 认证接口 `/api/v1/auth`
| 接口 | 方法 | 说明 |
|------|------|------|
| /register | POST | 用户注册 |
| /login | POST | 用户登录 |
| /logout | POST | 用户登出 |
| /refresh | POST | 刷新Token |
| /change-password | POST | 修改密码 |
| /reset-password | POST | 重置密码 |

### 用户接口 `/api/v1/users`
| 接口 | 方法 | 说明 |
|------|------|------|
| /profile | GET | 获取用户信息 |
| /profile | PUT | 更新用户信息 |

### 考研接口 `/api/v1/kaoyan`
| 接口 | 方法 | 说明 |
|------|------|------|
| /info/list | GET | 资讯列表 |
| /info/{id} | GET | 资讯详情 |
| /info | POST | 创建资讯 |
| /info/{id} | PUT | 更新资讯 |
| /info/{id} | DELETE | 删除资讯 |
| /crawler/config | GET | 爬虫配置 |
| /crawler/config | PUT | 更新爬虫配置 |
| /crawler/start | POST | 启动爬虫 |
| /crawler/stop | POST | 停止爬虫 |

### 考公接口 `/api/v1/kaogong`
| 接口 | 方法 | 说明 |
|------|------|------|
| /info/list | GET | 资讯列表 |
| /info/{id} | GET | 资讯详情 |
| /info | POST | 创建资讯 |
| /info/{id} | PUT | 更新资讯 |
| /info/{id} | DELETE | 删除资讯 |
| /crawler/config | GET | 爬虫配置 |
| /crawler/config | PUT | 更新爬虫配置 |
| /crawler/start | POST | 启动爬虫 |
| /crawler/stop | POST | 停止爬虫 |

### 支付接口 `/api/v1/payments`
| 接口 | 方法 | 说明 |
|------|------|------|
| /orders | POST | 创建订单 |
| /orders | GET | 订单列表 |
| /orders/{id} | GET | 订单详情 |
| /orders/{id}/pay | POST | 支付订单 |
| /products | GET | 产品列表 |
| /products | POST | 创建产品 |
| /admin/orders | GET | 管理订单列表 |
| /admin/products | GET | 管理产品列表 |

### 推送接口 `/api/v1/push`
| 接口 | 方法 | 说明 |
|------|------|------|
| /settings | GET | 获取推送设置 |
| /settings | POST | 保存推送设置 |
| /history | GET | 推送历史 |
| /history/{id} | DELETE | 删除推送记录 |
| /stats | GET | 推送统计 |
| /templates | GET | 推送模板 |

### 消息接口 `/api/v1/message`
| 接口 | 方法 | 说明 |
|------|------|------|
| /list | GET | 消息列表 |
| /read/{id} | POST | 标记已读 |

### 学习资料接口 `/api/v1/learning_materials`
| 接口 | 方法 | 说明 |
|------|------|------|
| /categories | GET | 分类列表 |
| /materials | GET | 资料列表 |
| /materials | POST | 上传资料 |
| /download | POST | 下载记录 |

### 管理后台接口 `/api/v1/admin`
| 接口 | 方法 | 说明 |
|------|------|------|
| /users | GET | 用户列表 |
| /users/{id} | GET | 用户详情 |
| /users/{id} | PUT | 更新用户 |
| /users/{id} | DELETE | 删除用户 |
| /feedbacks | GET | 反馈列表 |
| /system/config | GET | 系统配置 |
| /system/config | PUT | 更新系统配置 |

---

## 六、数据库表结构

### 用户相关表
- `users` - 用户表
- `orders` - 订单表
- `user_subscriptions` - 用户订阅表
- `user_keywords` - 用户关键词表
- `push_logs` - 推送日志表
- `push_settings` - 推送设置表

### 资讯相关表
- `kaoyan_infos` - 考研资讯表
- `kaoyan_categories` - 考研分类表
- `kaogong_infos` - 考公资讯表
- `kaogong_categories` - 考公分类表

### 运营相关表
- `products` - 产品表
- `learning_materials` - 学习资料表
- `material_categories` - 资料分类表
- `feedbacks` - 用户反馈表
- `schools` - 学校表

---

## 七、部署说明

### 环境要求
- Python 3.9+
- Node.js 18+
- MySQL 8.0+
- Redis 6.0+

### 后端启动
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

### 小程序
使用微信开发者工具打开 `kaoyankaogong-weapp` 目录

---

## 八、配置说明

### 环境变量 (.env)
```env
# 数据库配置
DATABASE_USER=root
DATABASE_PASSWORD=123456789
DATABASE_HOST=localhost
DATABASE_PORT=3306
COMMON_DB=common_db
KAOYAN_DB=kaoyan_db
KAOGONG_DB=kaogong_db

# 微信配置
WECHAT_APP_ID=your_app_id
WECHAT_APP_SECRET=your_app_secret

# 支付宝配置
ALIPAY_APP_ID=your_app_id
ALIPAY_PRIVATE_KEY=your_private_key

# 微信支付配置
WXPAY_APP_ID=your_app_id
WXPAY_MCH_ID=your_mch_id
WXPAY_API_KEY=your_api_key
```

---

## 九、版本信息

- 当前版本：1.0.0
- 最后更新：2026年

---

## 十、联系支持

如有问题，请联系技术支持。
