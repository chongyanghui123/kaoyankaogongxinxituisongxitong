<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">邮件文案和信息表单管理</h3>
          <el-button type="primary" class="add-btn" @click="handleAddTemplate">添加新文案</el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索文案标题或关键词"
              clearable
              prefix-icon="Search"
              @keyup.enter="getTemplates"
            >
              <template #append>
                <el-button type="primary" @click="getTemplates">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="8">
            <el-select v-model="categoryFilter" placeholder="按分类筛选" clearable @change="getTemplates">
              <el-option label="全部" value="" />
              <el-option label="邮件文案" value="email" />
              <el-option label="表单文案" value="form" />
              <el-option label="推送文案" value="push" />
              <el-option label="其他文案" value="other" />
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-select v-model="statusFilter" placeholder="按状态筛选" clearable @change="getTemplates">
              <el-option label="全部" value="" />
              <el-option label="启用" value="1" />
              <el-option label="禁用" value="0" />
            </el-select>
          </el-col>
        </el-row>
      </div>
      
      <!-- 文案表格 -->
      <el-table :data="templates" style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="title" label="文案标题" width="200">
          <template #default="scope">
            <el-tag :type="getCategoryType(scope.row.category)">{{ scope.row.title }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="category_text" label="分类" width="120">
          <template #default="scope">
            <el-tag :type="getCategoryType(scope.row.category)">{{ scope.row.category_text }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="status_text" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
              {{ scope.row.status_text }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editTemplate(scope.row.id)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteTemplate(scope.row.id)" v-if="!scope.row.is_system">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑文案对话框 -->
    <el-dialog
      v-model="showDialog"
      :title="showAddDialog ? '添加新文案' : '编辑文案'"
      width="800px"
    >
      <el-form :model="templateForm" label-width="120px">
        <el-form-item label="文案标题" required>
          <el-input v-model="templateForm.title" placeholder="请输入文案标题" />
        </el-form-item>
        <el-form-item label="分类" required>
          <el-select v-model="templateForm.category" placeholder="请选择文案分类">
            <el-option label="邮件文案" value="email" />
            <el-option label="表单文案" value="form" />
            <el-option label="推送文案" value="push" />
            <el-option label="其他文案" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="templateForm.status" :active-value="1" :inactive-value="0" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="templateForm.description" type="textarea" placeholder="请输入文案描述" :rows="2" />
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input v-model="templateForm.content" type="textarea" placeholder="请输入文案内容" :rows="10" />
          <div class="field-hints">
            <div class="hint-title">支持的变量字段：</div>
            <div class="hint-list">
              <div class="hint-item"><strong>{username}</strong> - 用户名</div>
              <div class="hint-item"><strong>{real_name}</strong> - 真实姓名</div>
              <div class="hint-item"><strong>{email}</strong> - 邮箱</div>
              <div class="hint-item"><strong>{phone}</strong> - 手机号</div>
              <div class="hint-item"><strong>{product_name}</strong> - 产品名称</div>
              <div class="hint-item"><strong>{service_type}</strong> - 服务类型（考研/考公/双赛道）</div>
              <div class="hint-item"><strong>{start_date}</strong> - 服务开始日期</div>
              <div class="hint-item"><strong>{end_date}</strong> - 服务结束日期</div>
              <div class="hint-item"><strong>{duration}</strong> - 服务时长（天数）</div>
              <div class="hint-item"><strong>{price}</strong> - 价格</div>
            </div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeDialog">取消</el-button>
          <el-button type="primary" @click="saveTemplate">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 数据定义
const templates = ref([])
const loading = ref(false)
const searchQuery = ref('')
const categoryFilter = ref('')
const statusFilter = ref('')
const showDialog = ref(false)
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const currentTemplate = ref(null)
const templateForm = reactive({
  title: '',
  category: '',
  status: 1,
  description: '',
  content: ''
})

// 分类类型映射
const categoryMap = {
  email: '邮件文案',
  form: '表单文案',
  push: '推送文案',
  other: '其他文案'
}

// 获取分类颜色
const getCategoryType = (category) => {
  switch (category) {
    case 'email':
      return 'warning'
    case 'form':
      return 'info'
    case 'push':
      return 'success'
    case 'other':
      return 'danger'
    default:
      return 'info'
  }
}

// 获取模板列表
const getTemplates = async () => {
  try {
    loading.value = true
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/admin/configs', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        is_active: statusFilter.value === '1' ? true : statusFilter.value === '0' ? false : undefined
      }
    })
    // 过滤出邮件和表单文案
    templates.value = response.data.filter(config => {
      const isTemplate = config.key && (config.key.includes('email_') || config.key.includes('form_') || config.key.includes('push_'))
      if (!isTemplate) return false
      
      let matchCategory = true
      if (categoryFilter.value) {
        matchCategory = config.key.includes(categoryFilter.value)
      }
      
      let matchSearch = true
      if (searchQuery.value) {
        matchSearch = (config.description || config.key || '').toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                     (config.value || '').toLowerCase().includes(searchQuery.value.toLowerCase())
      }
      
      return matchCategory && matchSearch
    }).map(config => {
      // 解析配置键
      let category = 'other'
      if (config.key.includes('email_')) category = 'email'
      else if (config.key.includes('form_')) category = 'form'
      else if (config.key.includes('push_')) category = 'push'
      
      return {
        ...config,
        title: config.description || config.key,
        category: category,
        category_text: categoryMap[category],
        content: config.value,
        status_text: config.is_active ? '启用' : '禁用'
      }
    })
  } catch (error) {
    console.error('获取模板列表失败:', error)
    ElMessage.error('获取模板列表失败')
  } finally {
    loading.value = false
  }
}

// 处理添加模板
const handleAddTemplate = () => {
  showDialog.value = true
  showAddDialog.value = true
  showEditDialog.value = false
  currentTemplate.value = null
  templateForm.title = ''
  templateForm.category = ''
  templateForm.status = 1
  templateForm.description = ''
  templateForm.content = ''
}

// 编辑模板
const editTemplate = async (id) => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`/api/v1/admin/configs/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    currentTemplate.value = response.data
    
    // 解析配置键
    let category = 'other'
    if (response.data.key.includes('email_')) category = 'email'
    else if (response.data.key.includes('form_')) category = 'form'
    else if (response.data.key.includes('push_')) category = 'push'
    
    // 填充表单
    templateForm.title = response.data.description || response.data.key
    templateForm.category = category
    templateForm.status = response.data.is_active ? 1 : 0
    templateForm.description = response.data.description
    templateForm.content = response.data.value
    
    showDialog.value = true
    showAddDialog.value = false
    showEditDialog.value = true
  } catch (error) {
    console.error('获取模板详情失败:', error)
    ElMessage.error('获取模板详情失败')
  }
}

// 保存模板
const saveTemplate = async () => {
  try {
    const token = localStorage.getItem('token')
    const configKey = `${templateForm.category}_${templateForm.title.toLowerCase().replace(/\s+/g, '_')}`
    const configData = {
      key: configKey,
      value: templateForm.content,
      description: templateForm.description || templateForm.title,
      is_active: templateForm.status === 1,
      is_system: false
    }
    
    let response
    if (currentTemplate.value) {
      // 更新
      response = await axios.put(`/api/v1/admin/configs/${currentTemplate.value.id}`, configData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      ElMessage.success('模板更新成功')
    } else {
      // 创建
      response = await axios.post('/api/v1/admin/configs', configData, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      ElMessage.success('模板创建成功')
    }
    
    // 关闭对话框
    showDialog.value = false
    showAddDialog.value = false
    showEditDialog.value = false
    currentTemplate.value = null
    
    // 重置表单
    templateForm.title = ''
    templateForm.category = ''
    templateForm.status = 1
    templateForm.description = ''
    templateForm.content = ''
    
    getTemplates()
  } catch (error) {
    console.error('保存模板失败:', error)
    ElMessage.error('保存模板失败')
  }
}

// 删除模板
const deleteTemplate = async (id) => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`/api/v1/admin/configs/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    ElMessage.success('模板删除成功')
    getTemplates()
  } catch (error) {
    console.error('删除模板失败:', error)
    ElMessage.error('删除模板失败')
  }
}

// 关闭对话框
const closeDialog = () => {
  showDialog.value = false
  showAddDialog.value = false
  showEditDialog.value = false
  currentTemplate.value = null
  // 重置表单
  templateForm.title = ''
  templateForm.category = ''
  templateForm.status = 1
  templateForm.description = ''
  templateForm.content = ''
}

onMounted(() => {
  getTemplates()
})
</script>

<style scoped>
.admin-content {
  padding: 20px;
}

.content-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.search-filter {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.field-hints {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 12px;
  color: #606266;
}

.hint-title {
  font-weight: bold;
  margin-bottom: 5px;
  color: #303133;
}

.hint-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 3px;
}

.hint-item {
  line-height: 1.4;
}

.hint-item strong {
  color: #409eff;
  margin-right: 5px;
}
</style>
