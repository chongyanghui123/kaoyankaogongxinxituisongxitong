# 学习资料下载功能数据库表结构设计

## 1. 学习资料表 (learning_materials)

| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `PRIMARY KEY AUTO_INCREMENT` | 资料ID |
| `title` | `VARCHAR(255)` | `NOT NULL` | 资料标题 |
| `description` | `TEXT` | `NOT NULL` | 资料描述 |
| `type` | `TINYINT` | `NOT NULL` | 资料类型：1-考研，2-考公 |
| `category_id` | `INT` | `NOT NULL` | 资料分类ID，关联material_categories表 |
| `subject` | `VARCHAR(100)` | `NOT NULL` | 科目：如数学、英语、政治等 |
| `file_path` | `VARCHAR(255)` | `NOT NULL` | 文件存储路径 |
| `file_url` | `VARCHAR(255)` | `NOT NULL` | 文件下载URL |
| `file_size` | `BIGINT` | `NOT NULL` | 文件大小，单位：字节 |
| `file_extension` | `VARCHAR(50)` | `NOT NULL` | 文件扩展名 |
| `cover_image` | `VARCHAR(255)` | | 封面图片URL |
| `uploader_id` | `INT` | `NOT NULL` | 上传者ID，关联users表 |
| `upload_time` | `DATETIME` | `NOT NULL` | 上传时间 |
| `download_count` | `INT` | `DEFAULT 0` | 下载次数 |
| `rating` | `FLOAT` | `DEFAULT 0` | 评分 |
| `is_valid` | `TINYINT(1)` | `DEFAULT 1` | 是否有效 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

## 2. 资料分类表 (material_categories)

| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `PRIMARY KEY AUTO_INCREMENT` | 分类ID |
| `name` | `VARCHAR(100)` | `NOT NULL` | 分类名称 |
| `type` | `TINYINT` | `NOT NULL` | 适用类型：1-考研，2-考公，3-通用 |
| `description` | `TEXT` | | 分类描述 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

## 3. 用户下载记录表 (user_downloads)

| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `PRIMARY KEY AUTO_INCREMENT` | 下载记录ID |
| `user_id` | `INT` | `NOT NULL` | 用户ID，关联users表 |
| `material_id` | `INT` | `NOT NULL` | 资料ID，关联learning_materials表 |
| `download_time` | `DATETIME` | `NOT NULL` | 下载时间 |
| `ip_address` | `VARCHAR(50)` | | 下载IP地址 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

## 4. 资料评分表 (material_ratings) (可选)

| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `PRIMARY KEY AUTO_INCREMENT` | 评分ID |
| `user_id` | `INT` | `NOT NULL` | 用户ID，关联users表 |
| `material_id` | `INT` | `NOT NULL` | 资料ID，关联learning_materials表 |
| `rating` | `TINYINT` | `NOT NULL` | 评分，1-5星 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

## 5. 资料评论表 (material_comments) (可选)

| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `id` | `INT` | `PRIMARY KEY AUTO_INCREMENT` | 评论ID |
| `user_id` | `INT` | `NOT NULL` | 用户ID，关联users表 |
| `material_id` | `INT` | `NOT NULL` | 资料ID，关联learning_materials表 |
| `comment` | `TEXT` | `NOT NULL` | 评论内容 |
| `created_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `DATETIME` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

## 索引设计

1. **learning_materials表**：
   - `idx_type`：对type字段创建索引，加速按类型查询
   - `idx_category_id`：对category_id字段创建索引，加速按分类查询
   - `idx_subject`：对subject字段创建索引，加速按科目查询
   - `idx_upload_time`：对upload_time字段创建索引，加速按上传时间排序

2. **user_downloads表**：
   - `idx_user_id`：对user_id字段创建索引，加速查询用户的下载记录
   - `idx_material_id`：对material_id字段创建索引，加速查询资料的下载记录

3. **material_ratings表**：
   - `idx_user_id_material_id`：对user_id和material_id字段创建联合索引，确保每个用户对每个资料只评分一次

4. **material_comments表**：
   - `idx_material_id`：对material_id字段创建索引，加速查询资料的评论

## 外键关系

1. **learning_materials表**：
   - `category_id` → `material_categories.id`
   - `uploader_id` → `users.id`

2. **user_downloads表**：
   - `user_id` → `users.id`
   - `material_id` → `learning_materials.id`

3. **material_ratings表**：
   - `user_id` → `users.id`
   - `material_id` → `learning_materials.id`

4. **material_comments表**：
   - `user_id` → `users.id`
   - `material_id` → `learning_materials.id`

## 数据插入示例

### 1. 插入资料分类

```sql
INSERT INTO material_categories (name, type, description) VALUES
('考研真题', 1, '历年考研真题'),
('考研模拟题', 1, '考研模拟试题'),
('考研复习资料', 1, '考研复习资料'),
('考公真题', 2, '历年考公真题'),
('考公模拟题', 2, '考公模拟试题'),
('考公复习资料', 2, '考公复习资料'),
('通用资料', 3, '通用学习资料');
```

### 2. 插入学习资料

```sql
INSERT INTO learning_materials (title, description, type, category_id, subject, file_path, file_url, file_size, file_extension, cover_image, uploader_id, upload_time) VALUES
('2024年考研数学一真题', '2024年考研数学一真题及答案解析', 1, 1, '数学', '/path/to/files/2024_math1.pdf', 'http://example.com/files/2024_math1.pdf', 2048000, 'pdf', 'http://example.com/covers/math1.jpg', 1, '2024-01-01 00:00:00'),
('2024年考研英语一真题', '2024年考研英语一真题及答案解析', 1, 1, '英语', '/path/to/files/2024_english1.pdf', 'http://example.com/files/2024_english1.pdf', 1536000, 'pdf', 'http://example.com/covers/english1.jpg', 1, '2024-01-01 00:00:00'),
('2024年国考真题', '2024年国家公务员考试真题及答案解析', 2, 4, '行测', '/path/to/files/2024_gongkao.pdf', 'http://example.com/files/2024_gongkao.pdf', 3072000, 'pdf', 'http://example.com/covers/gongkao.jpg', 1, '2024-01-01 00:00:00');
```

### 3. 插入用户下载记录

```sql
INSERT INTO user_downloads (user_id, material_id, download_time, ip_address) VALUES
(1, 1, '2024-01-02 12:00:00', '127.0.0.1'),
(1, 2, '2024-01-03 13:00:00', '127.0.0.1'),
(2, 3, '2024-01-04 14:00:00', '127.0.0.1');
```
