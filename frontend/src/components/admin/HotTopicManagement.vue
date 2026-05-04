<template>
  <div class="hot-topic-management">
    <h2 class="page-title">热点管理</h2>
    
    <el-card class="management-card">
      <template #header>
        <div class="card-header">
          <span>热点列表</span>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加热点
          </el-button>
        </div>
      </template>
      
      <div class="search-filter">
        <el-input
          v-model="searchForm.title"
          placeholder="搜索热点标题"
          prefix-icon="Search"
          style="width: 300px; margin-right: 10px;"
          @keyup.enter="handleSearch"
        />
        <el-select
          v-model="searchForm.category"
          placeholder="分类筛选"
          style="width: 120px; margin-right: 10px;"
          @change="handleSearch"
          clearable
        >
          <el-option label="全部" value="" />
          <el-option label="考研" value="考研" />
          <el-option label="考公" value="考公" />
          <el-option label="通用" value="通用" />
        </el-select>
        <el-select
          v-model="searchForm.is_active"
          placeholder="状态筛选"
          style="width: 120px; margin-right: 10px;"
          @change="handleSearch"
          clearable
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
      
      <el-table
        :data="topics"
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column
          prop="id"
          label="ID"
          width="60"
        />
        <el-table-column
          prop="title"
          label="标题"
          min-width="200"
          show-overflow-tooltip
        />
        <el-table-column
          prop="cover_image"
          label="封面"
          width="100"
        >
          <template #default="scope">
            <el-image
              v-if="scope.row.cover_image"
              :src="getFullImageUrl(scope.row.cover_image)"
              fit="cover"
              style="width: 60px; height: 40px; border-radius: 4px;"
              preview-teleported
            />
            <span v-else>无</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="category"
          label="分类"
          width="80"
        >
          <template #default="scope">
            <el-tag :type="getCategoryType(scope.row.category)">
              {{ scope.row.category || '通用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="source"
          label="来源"
          width="100"
          show-overflow-tooltip
        />
        <el-table-column
          prop="views"
          label="浏览量"
          width="80"
        />
        <el-table-column
          prop="sort_order"
          label="排序"
          width="80"
        />
        <el-table-column
          prop="is_active"
          label="状态"
          width="80"
        >
          <template #default="scope">
            <el-switch
              v-model="scope.row.is_active"
              :active-value="true"
              :inactive-value="false"
              @change="handleStatusChange(scope.row)"
            />
          </template>
        </el-table-column>
        <el-table-column
          prop="created_at"
          label="创建时间"
          width="150"
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
    
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加热点' : '编辑热点'"
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
          label="标题"
          prop="title"
        >
          <el-input
            v-model="form.title"
            placeholder="请输入热点标题"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item
          label="内容"
          prop="content"
        >
          <el-input
            v-model="form.content"
            placeholder="请输入热点内容"
            type="textarea"
            :rows="4"
          />
        </el-form-item>
        
        <el-form-item
          label="封面图片"
          prop="cover_image"
        >
          <el-upload
            class="avatar-uploader"
            :action="uploadUrl"
            :show-file-list="false"
            :on-success="handleImageUploadSuccess"
            :before-upload="beforeImageUpload"
            :headers="{ 'Authorization': `Bearer ${token}` }"
          >
            <el-image
              v-if="form.cover_image"
              :src="getFullImageUrl(form.cover_image)"
              fit="cover"
              style="width: 120px; height: 80px; border-radius: 4px; cursor: pointer;"
            />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        
        <el-form-item
          label="跳转链接"
          prop="link_url"
        >
          <el-input
            v-model="form.link_url"
            placeholder="请输入跳转链接URL（可选）"
          />
        </el-form-item>
        
        <el-form-item
          label="分类"
          prop="category"
        >
          <el-select v-model="form.category" placeholder="请选择分类">
            <el-option label="考研" value="考研" />
            <el-option label="考公" value="考公" />
            <el-option label="通用" value="通用" />
          </el-select>
        </el-form-item>
        
        <el-form-item
          label="来源"
          prop="source"
        >
          <el-input
            v-model="form.source"
            placeholder="请输入来源（可选）"
          />
        </el-form-item>
        
        <el-form-item
          label="排序"
          prop="sort_order"
        >
          <el-input-number
            v-model="form.sort_order"
            :min="0"
            :max="999"
            placeholder="排序值，数字越大越靠前"
          />
        </el-form-item>
        
        <el-form-item
          label="状态"
          prop="is_active"
        >
          <el-switch
            v-model="form.is_active"
            :active-value="true"
            :inactive-value="false"
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
import { ref, reactive, onMounted, computed } from 'vue'
import {
  Plus, Edit, Delete, Search, Refresh
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from '@/utils/axios'

const topics = ref([])
const loading = ref(false)
const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})
const searchForm = reactive({
  title: '',
  category: '',
  is_active: ''
})
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref()
const form = reactive({
  id: null,
  title: '',
  content: '',
  cover_image: '',
  link_url: '',
  category: '',
  source: '',
  sort_order: 0,
  is_active: true
})
const formRules = reactive({
  title: [
    { required: true, message: '请输入热点标题', trigger: 'blur' }
  ]
})

const uploadUrl = computed(() => {
  return import.meta.env.VITE_API_BASE_URL ? `${import.meta.env.VITE_API_BASE_URL}/utils/upload` : 'http://localhost:8000/api/v1/utils/upload'
})

const token = computed(() => {
  return localStorage.getItem('token') || ''
})

const getFullImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  const baseUrl = import.meta.env.VITE_API_BASE_URL ? import.meta.env.VITE_API_BASE_URL.replace('/api/v1', '') : 'http://localhost:8000'
  return baseUrl + url
}

const getCategoryType = (category) => {
  const types = {
    '考研': 'primary',
    '考公': 'success',
    '通用': 'info'
  }
  return types[category] || 'info'
}

const handleImageUploadSuccess = (response) => {
  if (response.success) {
    form.cover_image = response.data.file_url
  }
}

const beforeImageUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB')
    return false
  }
  return true
}

const getTopics = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size
    }
    if (searchForm.title) params.title = searchForm.title
    if (searchForm.category) params.category = searchForm.category
    if (searchForm.is_active !== '' && searchForm.is_active !== null && searchForm.is_active !== undefined) {
      params.is_active = searchForm.is_active
    }
    const response = await axios.get('/api/v1/admin/hot-topics', { params })
    if (response.success) {
      topics.value = response.data
      pagination.total = response.total
    }
  } catch (error) {
    console.error('获取热点列表失败:', error)
    ElMessage.error('获取热点列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  getTopics()
}

const handleReset = () => {
  searchForm.title = ''
  searchForm.category = ''
  searchForm.is_active = ''
  pagination.page = 1
  getTopics()
}

const handleSizeChange = (size) => {
  pagination.page_size = size
  pagination.page = 1
  getTopics()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  getTopics()
}

const showAddDialog = () => {
  dialogType.value = 'add'
  Object.keys(form).forEach(key => {
    if (key === 'is_active') {
      form[key] = true
    } else if (key === 'sort_order') {
      form[key] = 0
    } else {
      form[key] = ''
    }
  })
  form.id = null
  dialogVisible.value = true
}

const showEditDialog = (row) => {
  dialogType.value = 'edit'
  form.id = row.id
  form.title = row.title
  form.content = row.content || ''
  form.cover_image = row.cover_image || ''
  form.link_url = row.link_url || ''
  form.category = row.category || ''
  form.source = row.source || ''
  form.sort_order = row.sort_order || 0
  form.is_active = row.is_active
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    
    const url = dialogType.value === 'add'
      ? '/api/v1/admin/hot-topics'
      : `/api/v1/admin/hot-topics/${form.id}`
      
    const method = dialogType.value === 'add' ? 'post' : 'put'
    
    const response = await axios[method](url, form)
    
    if (response.success || response.id) {
      ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
      dialogVisible.value = false
      getTopics()
    }
  } catch (error) {
    console.error('提交表单失败:', error)
    ElMessage.error('操作失败')
  }
}

const handleStatusChange = async (row) => {
  try {
    const response = await axios.put(
      `/api/v1/admin/hot-topics/${row.id}`,
      { is_active: row.is_active }
    )
    
    if (response.success || response.id) {
      ElMessage.success('状态更新成功')
      getTopics()
    } else {
      ElMessage.error(response.message || '更新失败')
      row.is_active = !row.is_active
    }
  } catch (error) {
    console.error('更新状态失败:', error)
    ElMessage.error('网络请求失败')
    row.is_active = !row.is_active
  }
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该热点吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await axios.delete(`/api/v1/admin/hot-topics/${id}`)
    if (response.success) {
      ElMessage.success('删除成功')
      getTopics()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  getTopics()
})
</script>

<style scoped>
.hot-topic-management {
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
  flex-wrap: wrap;
  gap: 10px;
}

:deep(.el-table__cell) {
  padding: 12px 0;
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

.avatar-uploader {
  display: flex;
  align-items: center;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.avatar-uploader-icon:hover {
  border-color: #409eff;
  color: #409eff;
}
</style>
