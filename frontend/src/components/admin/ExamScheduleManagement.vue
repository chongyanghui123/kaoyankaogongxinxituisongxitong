<template>
  <div class="exam-schedule-management">
    <h2 class="page-title">考试日程管理</h2>
    
    <el-card class="management-card">
      <!-- 操作按钮 -->
      <template #header>
        <div class="card-header">
          <span>考试日程列表</span>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加考试日程
          </el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-input
          v-model="searchForm.name"
          placeholder="搜索考试名称"
          prefix-icon="Search"
          style="width: 200px; margin-right: 10px;"
          @keyup.enter="handleSearch"
        />
        <el-select
          v-model="searchForm.exam_type"
          placeholder="类型筛选"
          style="width: 120px; margin-right: 10px;"
          @change="handleSearch"
        >
          <el-option label="全部" :value="''" />
          <el-option label="考研" :value="1" />
          <el-option label="考公" :value="2" />
        </el-select>
        <el-select
          v-model="searchForm.is_active"
          placeholder="状态筛选"
          style="width: 120px; margin-right: 10px;"
          @change="handleSearch"
        >
          <el-option label="全部" :value="''" />
          <el-option label="启用" :value="true" />
          <el-option label="禁用" :value="false" />
        </el-select>
        <el-button type="primary" @click="handleSearch">
          <el-icon><Search /></el-icon>
          搜索
        </el-button>
        <el-button @click="handleReset">
          <el-icon><Refresh /></el-icon>
          重置
        </el-button>
      </div>
      
      <!-- 考试日程列表 -->
      <el-table
        :data="schedules"
        v-loading="loading"
        style="width: 100%"
        @sort-change="handleSortChange"
      >
        <el-table-column
          prop="id"
          label="ID"
          width="60"
          sortable="custom"
        />
        <el-table-column
          prop="name"
          label="考试名称"
          min-width="180"
          sortable="custom"
        />
        <el-table-column
          prop="exam_type"
          label="类型"
          width="80"
          sortable="custom"
        >
          <template #default="scope">
            <el-tag
              :type="scope.row.exam_type === 1 ? 'success' : 'primary'"
              size="small"
            >
              {{ scope.row.exam_type === 1 ? '考研' : '考公' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="exam_date"
          label="考试日期"
          width="160"
          sortable="custom"
        >
          <template #default="scope">
            {{ formatDate(scope.row.exam_date) }}
          </template>
        </el-table-column>
        <el-table-column
          prop="description"
          label="描述"
          min-width="200"
          show-overflow-tooltip
        />
        <el-table-column
          prop="is_active"
          label="状态"
          width="80"
        >
          <template #default="scope">
            <el-switch
              v-model="scope.row.is_active"
              @change="handleStatusChange(scope.row)"
            />
          </template>
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="创建时间"
          width="150"
          sortable="custom"
        />
        <el-table-column
          prop="updated_at"
          label="更新时间"
          width="150"
          sortable="custom"
        />
        <el-table-column
          label="操作"
          width="150"
          fixed="right"
        >
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="showEditDialog(scope.row)"
            >
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(scope.row.id)"
            >
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-card>
    
    <!-- 添加/编辑考试日程对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加考试日程' : '编辑考试日程'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-width="100px"
        size="default"
      >
        <el-form-item
          label="考试名称"
          prop="name"
        >
          <el-input
            v-model="form.name"
            placeholder="请输入考试名称"
            maxlength="255"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item
          label="考试类型"
          prop="exam_type"
        >
          <el-radio-group v-model="form.exam_type">
            <el-radio :value="1">考研</el-radio>
            <el-radio :value="2">考公</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item
          label="考试日期"
          prop="exam_date"
        >
          <el-date-picker
            v-model="form.exam_date"
            type="datetime"
            placeholder="选择考试日期"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item
          label="考试描述"
          prop="description"
        >
          <el-input
            v-model="form.description"
            placeholder="请输入考试描述"
            type="textarea"
            :rows="3"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item
          label="状态"
          prop="is_active"
        >
          <el-switch
            v-model="form.is_active"
            active-text="启用"
            inactive-text="禁用"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  Plus, Edit, Delete, Search, Refresh
} from '@element-plus/icons-vue'
import axios from '@/utils/axios'

// 数据
const schedules = ref([])
const loading = ref(false)
const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})
const searchForm = reactive({
  name: '',
  exam_type: '',
  is_active: ''
})
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref()
const form = reactive({
  id: null,
  name: '',
  exam_type: 1,
  exam_date: '',
  description: '',
  is_active: true
})
const formRules = reactive({
  name: [
    { required: true, message: '请输入考试名称', trigger: 'blur' },
    { min: 1, max: 255, message: '考试名称长度在 1 到 255 个字符之间', trigger: 'blur' }
  ],
  exam_type: [
    { required: true, message: '请选择考试类型', trigger: 'change' }
  ],
  exam_date: [
    { required: true, message: '请选择考试日期', trigger: 'change' }
  ],
  description: [
    { max: 500, message: '考试描述长度不能超过 500 个字符', trigger: 'blur' }
  ]
})

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 获取考试日程列表
const getSchedules = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      name: searchForm.name,
      exam_type: searchForm.exam_type,
      is_active: searchForm.is_active
    }
    const response = await axios.get('/api/v1/learning_materials/exam-schedules', { params })
    // axios拦截器已经返回了response.data，所以response就是数据本身
    if (response.success) {
      schedules.value = response.data.items
      pagination.total = response.data.total
    }
  } catch (error) {
    console.error('获取考试日程列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  getSchedules()
}

// 重置搜索条件
const handleReset = () => {
  searchForm.name = ''
  searchForm.exam_type = ''
  searchForm.is_active = ''
  pagination.page = 1
  getSchedules()
}

// 排序
const handleSortChange = ({ prop, order }) => {
  console.log('排序:', prop, order)
  // 可以在这里实现排序逻辑
}

// 分页大小改变
const handleSizeChange = (size) => {
  pagination.page_size = size
  pagination.page = 1
  getSchedules()
}

// 页码改变
const handleCurrentChange = (page) => {
  pagination.page = page
  getSchedules()
}

// 显示添加对话框
const showAddDialog = () => {
  dialogType.value = 'add'
  Object.keys(form).forEach(key => {
    if (key === 'is_active') {
      form[key] = true
    } else if (key === 'exam_type') {
      form[key] = 1
    } else {
      form[key] = ''
    }
  })
  form.id = null
  dialogVisible.value = true
}

// 显示编辑对话框
const showEditDialog = (row) => {
  dialogType.value = 'edit'
  Object.assign(form, row)
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    
    const url = dialogType.value === 'add'
      ? '/api/v1/learning_materials/exam-schedules'
      : `/api/v1/learning_materials/exam-schedules/${form.id}`
      
    const method = dialogType.value === 'add' ? 'post' : 'put'
    
    const response = await axios[method](url, form)
    
    if (response.success) {
      dialogVisible.value = false
      getSchedules()
    }
  } catch (error) {
    console.error('提交表单失败:', error)
  }
}

// 状态改变
const handleStatusChange = async (row) => {
  try {
    const response = await axios.put(
      `/api/v1/learning_materials/exam-schedules/${row.id}`,
      { is_active: row.is_active }
    )
    if (response.success) {
      // 状态已更新
    } else {
      row.is_active = !row.is_active
    }
  } catch (error) {
    row.is_active = !row.is_active
    console.error('更新状态失败:', error)
  }
}

// 删除
const handleDelete = async (id) => {
  try {
    await axios.delete(`/api/v1/learning_materials/exam-schedules/${id}`)
    getSchedules()
  } catch (error) {
    console.error('删除失败:', error)
  }
}

// 初始化
onMounted(() => {
  getSchedules()
})
</script>

<style scoped>
.exam-schedule-management {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.management-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-filter {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.search-filter .el-input,
.search-filter .el-select {
  margin-right: 10px;
}

:deep(.el-table__cell) {
  padding: 12px 0;
}

:deep(.el-table__header-wrapper) {
  background-color: #f5f7fa;
}

:deep(.el-table__header-wrapper th) {
  background-color: #f5f7fa !important;
  color: #333;
  font-weight: 600;
}

:deep(.el-pagination) {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  text-align: right;
}
</style>
