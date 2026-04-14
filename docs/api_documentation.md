# 双赛道情报通 API 接口文档

## 1. 概述

本文档描述了双赛道情报通系统的所有API接口，包括认证、用户管理、考研情报、考公情报、爬虫管理、支付、推送通知和系统配置等模块。

## 2. 基础信息

- API基础URL: `http://localhost:8000/api/v1`
- 认证方式: JWT Token
- 请求/响应格式: JSON
- 错误处理: 统一返回错误码和错误信息

## 3. 认证接口

### 3.1 注册

- **路径**: `/auth/register`
- **方法**: POST
- **请求体**:
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "phone": "13800138000"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "注册成功",
    "data": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "phone": "13800138000",
      "is_admin": false,
      "is_active": true,
      "created_at": "2026-01-01T00:00:00"
    }
  }
  ```

### 3.2 登录

- **路径**: `/auth/login`
- **方法**: POST
- **请求体**:
  ```json
  {
    "email": "test@example.com",
    "password": "password123"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "登录成功",
    "data": {
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "token_type": "bearer",
      "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "is_admin": false,
        "is_active": true
      }
    }
  }
  ```

### 3.3 刷新Token

- **路径**: `/auth/refresh`
- **方法**: POST
- **请求头**: `Authorization: Bearer {token}`
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "Token刷新成功",
    "data": {
      "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "token_type": "bearer"
    }
  }
  ```

### 3.4 登出

- **路径**: `/auth/logout`
- **方法**: POST
- **请求头**: `Authorization: Bearer {token}`
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "登出成功",
    "data": null
  }
  ```

## 4. 用户管理接口

### 4.1 获取用户信息

- **路径**: `/users/profile`
- **方法**: GET
- **请求头**: `Authorization: Bearer {token}`
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "获取用户信息成功",
    "data": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "phone": "13800138000",
      "is_admin": false,
      "is_active": true,
      "created_at": "2026-01-01T00:00:00",
      "updated_at": "2026-01-01T00:00:00"
    }
  }
  ```

### 4.2 更新用户信息

- **路径**: `/users/profile`
- **方法**: PUT
- **请求头**: `Authorization: Bearer {token}`
- **请求体**:
  ```json
  {
    "username": "newname",
    "phone": "13900139000"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "更新用户信息成功",
    "data": {
      "id": 1,
      "username": "newname",
      "email": "test@example.com",
      "phone": "13900139000",
      "is_admin": false,
      "is_active": true,
      "created_at": "2026-01-01T00:00:00",
      "updated_at": "2026-01-02T00:00:00"
    }
  }
  ```

### 4.3 修改密码

- **路径**: `/users/change-password`
- **方法**: POST
- **请求头**: `Authorization: Bearer {token}`
- **请求体**:
  ```json
  {
    "old_password": "password123",
    "new_password": "newpassword123"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "密码修改成功",
    "data": null
  }
  ```

## 5. 考研情报接口

### 5.1 获取考研情报列表

- **路径**: `/kaoyan/info`
- **方法**: GET
- **参数**:
  - `skip`: 跳过条数 (默认: 0)
  - `limit`: 限制条数 (默认: 10)
  - `province`: 省份
  - `category`: 分类
  - `keyword`: 关键词
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "获取考研情报列表成功",
    "data": {
      "items": [
        {
          "id": 1,
          "title": "2026年全国硕士研究生招生考试公告",
          "content": "根据《2026年全国硕士研究生招生工作管理规定》...",
          "source": "中国研究生招生信息网",
          "url": "https://yz.chsi.com.cn/",
          "province": "全国",
          "school": "教育部",
          "major": "全部",
          "category": "政策通知",
          "publish_date": "2026-09-24T00:00:00",
          "read_count": 12345,
          "like_count": 678
        }
      ],
      "total": 1
    }
  }
  ```

### 5.2 获取考研情报详情

- **路径**: `/kaoyan/info/{id}`
- **方法**: GET
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "获取考研情报详情成功",
    "data": {
      "id": 1,
      "title": "2026年全国硕士研究生招生考试公告",
      "content": "根据《2026年全国硕士研究生招生工作管理规定》...",
      "source": "中国研究生招生信息网",
      "url": "https://yz.chsi.com.cn/",
      "province": "全国",
      "school": "教育部",
      "major": "全部",
      "category": "政策通知",
      "publish_date": "2026-09-24T00:00:00",
      "read_count": 12345,
      "like_count": 678
    }
  }
  ```

### 5.3 点赞考研情报

- **路径**: `/kaoyan/info/{id}/like`
- **方法**: POST
- **请求头**: `Authorization: Bearer {token}`
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "点赞成功",
    "data": {
      "like_count": 679
    }
  }
  ```

## 6. 考公情报接口

### 6.1 获取考公情报列表

- **路径**: `/kaogong/info`
- **方法**: GET
- **参数**:
  - `skip`: 跳过条数 (默认: 0)
  - `limit`: 限制条数 (默认: 10)
  - `province`: 省份
  - `category`: 分类
  - `keyword`: 关键词
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "获取考公情报列表成功",
    "data": {
      "items": [
        {
          "id": 1,
          "title": "2026年国家公务员招考公告",
          "content": "根据公务员法和公务员录用有关规定...",
          "source": "国家公务员局",
          "url": "https://www.scs.gov.cn/",
          "province": "全国",
          "position_type": "公务员",
          "major": "全部",
          "education": "不限",
          "category": "招考公告",
          "publish_date": "2026-10-14T00:00:00",
          "read_count": 23456,
          "like_count": 1234
        }
      ],
      "total": 1
    }
  }
  ```

### 6.2 获取考公情报详情

- **路径**: `/kaogong/info/{id}`
- **方法**: GET
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "获取考公情报详情成功",
    "data": {
      "id": 1,
      "title": "2026年国家公务员招考公告",
      "content": "根据公务员法和公务员录用有关规定...",
      "source": "国家公务员局",
      "url": "https://www.scs.gov.cn/",
      "province": "全国",
      "position_type": "公务员",
      "major": "全部",
      "education": "不限",
      "category": "招考公告",
      "publish_date": "2026-10-14T00:00:00",
      "read_count": 23456,
      "like_count": 1234
    }
  }
  ```

### 6.3 点赞考公情报

- **路径**: `/kaogong/info/{id}/like`
- **方法**: POST
- **请求头**: `Authorization: Bearer {token}`
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "点赞成功",
    "data": {
      "like_count": 1235
    }
  }
  ```

## 7. 爬虫管理接口

### 7.1 获取考研爬虫配置列表

- **路径**: `/crawlers/kaoyan/configs`
- **方法**: GET
- **请求头**: `Authorization: Bearer {token}` (管理员)
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "获取考研爬虫配置列表成功",
    "data": [
      {
        "id": 1,
        "name": "研招网爬虫",
        "url": "https://yz.chsi.com.cn/",
        "interval": 3600,
        "priority": 1,
        "is_active": true,
        "config": {
          "headers": {
            "User-Agent": "Mozilla/5.0..."
          }
        },
        "created_at": "2026-01-01T00:00:00",
        "updated_at": "2026-01-01T00:00:00"
      }
    ]
  }
  ```

### 7.2 启动考研爬虫

- **路径**: `/crawlers/kaoyan/{id}/start`
- **方法**: POST
- **请求头**: `Authorization: Bearer {token}` (管理员)
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "爬虫启动成功",
    "data": null
  }
  ```

### 7.3 停止考研爬虫

- **路径**: `/crawlers/kaoyan/{id}/stop`
- **方法**: POST
- **请求头**: `Authorization: Bearer {token}` (管理员)
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "爬虫停止成功",
    "data": null
  }
  ```

## 8. 支付接口

### 8.1 创建订单

- **路径**: `/payments/orders`
- **方法**: POST
- **请求头**: `Authorization: Bearer {token}`
- **请求体**:
  ```json
  {
    "product_id": 1,
    "payment_method": "wechat"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "订单创建成功",
    "data": {
      "id": 1,
      "user_id": 1,
      "product_id": 1,
      "amount": 19.9,
      "status": "pending",
      "payment_method": "wechat",
      "created_at": "2026-01-01T00:00:00"
    }
  }
  ```

### 8.2 获取订单列表

- **路径**: `/payments/orders`
- **方法**: GET
- **请求头**: `Authorization: Bearer {token}`
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "获取订单列表成功",
    "data": [
      {
        "id": 1,
        "user_id": 1,
        "product_id": 1,
        "amount": 19.9,
        "status": "completed",
        "payment_method": "wechat",
        "transaction_id": "wx1234567890",
        "created_at": "2026-01-01T00:00:00",
        "paid_at": "2026-01-01T00:05:00"
      }
    ]
  }
  ```

## 9. 推送通知接口

### 9.1 发送推送

- **路径**: `/push/send`
- **方法**: POST
- **请求头**: `Authorization: Bearer {token}` (管理员)
- **请求体**:
  ```json
  {
    "template_id": 1,
    "user_id": 1,
    "content": "测试推送内容",
    "params": {
      "title": "测试标题"
    }
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "推送发送成功",
    "data": {
      "id": 1,
      "template_id": 1,
      "user_id": 1,
      "content": "测试推送内容",
      "status": "sent",
      "created_at": "2026-01-01T00:00:00"
    }
  }
  ```

## 10. 系统配置接口

### 10.1 获取系统配置列表

- **路径**: `/system/configs`
- **方法**: GET
- **请求头**: `Authorization: Bearer {token}` (管理员)
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "获取系统配置列表成功",
    "data": [
      {
        "id": 1,
        "key": "system_name",
        "value": "双赛道情报通",
        "description": "系统名称",
        "is_active": true,
        "created_at": "2026-01-01T00:00:00",
        "updated_at": "2026-01-01T00:00:00"
      }
    ]
  }
  ```

### 10.2 获取系统统计信息

- **路径**: `/system/stats`
- **方法**: GET
- **请求头**: `Authorization: Bearer {token}` (管理员)
- **响应**:
  ```json
  {
    "success": true,
    "code": 200,
    "message": "获取系统统计信息成功",
    "data": {
      "user_count": 100,
      "kaoyan_count": 1000,
      "kaogong_count": 800,
      "order_count": 50,
      "push_count": 200,
      "timestamp": "2026-01-01T00:00:00"
    }
  }
  ```

## 11. 错误码说明

| 错误码 | 含义 |
|-------|------|
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 12. 示例请求

### 使用curl发送登录请求

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### 使用curl发送带认证的请求

```bash
curl -X GET http://localhost:8000/api/v1/users/profile \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```
