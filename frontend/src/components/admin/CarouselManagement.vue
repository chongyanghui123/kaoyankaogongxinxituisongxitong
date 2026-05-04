<template>
  <div class="carousel-management">
    <h2 class="page-title">轮播图管理</h2>
    
    <el-card class="management-card">
      <!-- 操作按钮 -->
      <template #header>
        <div class="card-header">
          <span>轮播图列表</span>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加轮播图
          </el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-input
          v-model="searchForm.title"
          placeholder="搜索轮播图标题"
          prefix-icon="Search"
          style="width: 300px; margin-right: 10px;"
          @keyup.enter="handleSearch"
        />
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
      
      <!-- 轮播图列表 -->
      <el-table
        :data="carousels"
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
          prop="title"
          label="标题"
          min-width="150"
          sortable="custom"
        />
        <el-table-column
          prop="subtitle"
          label="副标题"
          min-width="200"
          show-overflow-tooltip
        />
        <el-table-column
          prop="image_url"
          label="图片"
          width="100"
        >
          <template #default="scope">
            <el-image
              v-if="scope.row.image_url"
              :src="getFullImageUrl(scope.row.image_url)"
              :initial-index="0"
              fit="cover"
              style="width: 60px; height: 40px; border-radius: 4px;"
              preview-teleported
            />
            <span v-else>无</span>
          </template>
        </el-table-column>

        <el-table-column
          prop="sort_order"
          label="排序"
          width="80"
          sortable="custom"
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
    
    <!-- 添加/编辑轮播图对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加轮播图' : '编辑轮播图'"
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
            placeholder="请输入轮播图标题"
            maxlength="255"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item
          label="副标题"
          prop="subtitle"
        >
          <el-input
            v-model="form.subtitle"
            placeholder="请输入轮播图副标题"
            type="textarea"
            :rows="3"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item
          label="图片"
          prop="image_url"
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
              v-if="form.image_url"
              :src="getFullImageUrl(form.image_url)"
              fit="cover"
              style="width: 120px; height: 80px; border-radius: 4px; cursor: pointer;"
            />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        

        
        <el-form-item
          label="排序"
          prop="sort_order"
        >
          <el-input-number
            v-model="form.sort_order"
            :min="0"
            :max="999"
            placeholder="排序值"
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
    
    <!-- 图片预览 -->
    <el-image-viewer
      v-if="imageViewerVisible"
      :url-list="[imageViewerUrl]"
      :initial-index="0"
      :on-close="handleImageViewerClose"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import {
  Plus, Edit, Delete, Search, Refresh
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from '@/utils/axios'

// 数据
const carousels = ref([])
const loading = ref(false)
const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})
const searchForm = reactive({
  title: '',
  is_active: ''
})
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref()
const form = reactive({
  id: null,
  title: '',
  subtitle: '',
  image_url: '',
  sort_order: 0,
  is_active: true
})
const formRules = reactive({
  title: [
    { required: true, message: '请输入轮播图标题', trigger: 'blur' },
    { min: 1, max: 255, message: '标题长度在 1 到 255 个字符之间', trigger: 'blur' }
  ],
  subtitle: [
    { max: 500, message: '副标题长度不能超过 500 个字符', trigger: 'blur' }
  ],
  image_url: [
    { max: 500, message: '图片URL长度不能超过 500 个字符', trigger: 'blur' }
  ],

  sort_order: [
    { type: 'number', min: 0, max: 999, message: '排序值在 0 到 999 之间', trigger: 'blur' }
  ]
})
const imageViewerVisible = ref(false)
const imageViewerUrl = ref('')

// 上传相关
const uploadUrl = computed(() => {
  return import.meta.env.VITE_API_BASE_URL ? `${import.meta.env.VITE_API_BASE_URL}/utils/upload` : 'http://localhost:8000/api/v1/utils/upload'
})

const token = computed(() => {
  return localStorage.getItem('token') || ''
})

// 计算完整的图片URL
const getFullImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  const baseUrl = import.meta.env.VITE_API_BASE_URL ? import.meta.env.VITE_API_BASE_URL.replace('/api/v1', '') : 'http://localhost:8000'
  return baseUrl + url
}

// 图片上传成功
const handleImageUploadSuccess = (response, file) => {
  if (response.success) {
    form.image_url = response.data.file_url
  }
}

// 上传前验证
const beforeImageUpload = (file) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJpgOrPng) {
    ElMessage.error('只支持JPG和PNG格式的图片')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB')
    return false
  }
  return true
}

// 获取轮播图列表
const getCarousels = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      title: searchForm.title,
      is_active: searchForm.is_active
    }
    const response = await axios.get('/api/v1/learning_materials/carousels', { params })
    if (response.success) {
      carousels.value = response.data.items
      pagination.total = response.data.total
    }
  } catch (error) {
    console.error('获取轮播图列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  getCarousels()
}

// 重置搜索条件
const handleReset = () => {
  searchForm.title = ''
  searchForm.is_active = ''
  pagination.page = 1
  getCarousels()
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
  getCarousels()
}

// 页码改变
const handleCurrentChange = (page) => {
  pagination.page = page
  getCarousels()
}

// 显示添加对话框
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

// 显示编辑对话框
const showEditDialog = (row) => {
  dialogType.value = 'edit'
  // 只复制需要的字段，排除link_url
  form.id = row.id
  form.title = row.title
  form.subtitle = row.subtitle
  form.image_url = row.image_url
  form.sort_order = row.sort_order
  form.is_active = row.is_active
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    
    const url = dialogType.value === 'add'
      ? '/api/v1/learning_materials/carousels'
      : `/api/v1/learning_materials/carousels/${form.id}`
      
    const method = dialogType.value === 'add' ? 'post' : 'put'
    
    const response = await axios[method](url, form)
    
    if (response.success) {
      dialogVisible.value = false
      getCarousels()
    }
  } catch (error) {
    console.error('提交表单失败:', error)
  }
}

// 状态改变
const handleStatusChange = async (row) => {
  try {
    console.log('更新轮播图状态:', row.id, row.is_active)
    const response = await axios.put(
      `/api/v1/learning_materials/carousels/${row.id}`,
      { is_active: row.is_active }
    )
    
    console.log('更新响应:', response)
    
    if (response.success) {
      ElMessage.success('状态更新成功')
      // 更新成功后重新获取轮播图列表
      getCarousels()
    } else {
      ElMessage.error(response.message || '更新失败')
      row.is_active = !row.is_active // 恢复原状态
    }
  } catch (error) {
    console.error('更新状态失败:', error)
    ElMessage.error('网络请求失败')
    row.is_active = !row.is_active // 恢复原状态
  }
}

// 删除
const handleDelete = async (id) => {
  try {
    await axios.delete(`/api/v1/learning_materials/carousels/${id}`)
    getCarousels()
  } catch (error) {
    console.error('删除失败:', error)
  }
}

// 图片预览
const handleImageViewerClose = () => {
  imageViewerVisible.value = false
  imageViewerUrl.value = ''
}

// 初始化
onMounted(() => {
  getCarousels()
})
</script>

<style scoped>
.carousel-management {
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

/* 上传组件样式 */
.avatar-uploader {
  display: flex;
  align-items: center;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color 0.3s;
}

.avatar-uploader .el-upload:hover {
  border-color: #409eff;
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
