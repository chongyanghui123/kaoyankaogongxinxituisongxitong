<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">学习资料管理</h3>
          <el-button type="primary" @click="showUploadDialog = true">上传资料</el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-input
              v-model="searchQuery"
              placeholder="搜索资料"
              clearable
              prefix-icon="Search"
              @keyup.enter="getMaterials"
            >
              <template #append>
                <el-button type="primary" @click="getMaterials">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="6">
            <el-select v-model="typeFilter" placeholder="按类型筛选" clearable @change="getMaterials">
              <el-option label="全部" value="" />
              <el-option label="考研" value="1" />
              <el-option label="考公" value="2" />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="categoryFilter" placeholder="按分类筛选" clearable @change="getMaterials">
              <el-option label="全部" value="" />
              <el-option
                v-for="category in categories"
                :key="category.id"
                :label="category.name"
                :value="category.id"
              />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="vipFilter" placeholder="按VIP权限筛选" clearable @change="getMaterials">
              <el-option label="全部" value="" />
              <el-option label="VIP专属" value="true" />
              <el-option label="普通资料" value="false" />
            </el-select>
          </el-col>
        </el-row>
      </div>
      
      <!-- 学习资料表格 -->
      <el-table :data="materials" style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column label="封面图片" width="120">
          <template #default="scope">
            <el-image 
              v-if="scope.row.cover_image" 
              :src="apiBaseUrl + scope.row.cover_image" 
              :preview-src-list="[apiBaseUrl + scope.row.cover_image]"
              style="width: 60px; height: 60px;"
              fit="cover"
            />
            <span v-else>无图片</span>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.type === 1 ? 'primary' : 'success'">
              {{ scope.row.type === 1 ? '考研' : '考公' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="category_name" label="分类" width="150" />
        <el-table-column prop="subject" label="科目" width="120" />
        <el-table-column prop="file_size" label="文件大小" width="120">
          <template #default="scope">
            {{ formatFileSize(scope.row.file_size) }}
          </template>
        </el-table-column>
        <el-table-column prop="download_count" label="下载次数" width="100" />
        <el-table-column prop="rating" label="评分" width="100">
          <template #default="scope">
            <span class="rating-number">{{ scope.row.rating.toFixed(1) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="VIP专属" width="90">
          <template #default="scope">
            <el-tag :type="scope.row.is_vip ? 'danger' : 'info'" size="small">
              {{ scope.row.is_vip ? 'VIP' : '普通' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="upload_time" label="上传时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="openEditDialog(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteMaterial(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination" v-if="!loading && materials.length > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
      
      <!-- 上传资料对话框 -->
      <el-dialog
        v-model="showUploadDialog"
        title="上传学习资料"
        width="800px"
      >
        <el-form :model="uploadForm" label-width="100px">
          <el-form-item label="资料标题">
            <el-input v-model="uploadForm.title" placeholder="请输入资料标题" />
          </el-form-item>
          <el-form-item label="资料描述">
            <el-input
              v-model="uploadForm.description"
              type="textarea"
              placeholder="请输入资料描述"
              :rows="3"
            />
          </el-form-item>
          <el-form-item label="资料类型">
            <el-select v-model="uploadForm.type" placeholder="请选择资料类型">
              <el-option label="考研" value="1" />
              <el-option label="考公" value="2" />
            </el-select>
          </el-form-item>
          <el-form-item label="资料分类">
            <el-select v-model="uploadForm.category_id" placeholder="请选择资料分类">
              <el-option
                v-for="category in categories"
                :key="category.id"
                :label="category.name"
                :value="category.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="科目">
            <el-input v-model="uploadForm.subject" placeholder="请输入科目" />
          </el-form-item>
          <el-form-item label="VIP专属">
            <el-switch v-model="uploadForm.is_vip" active-text="仅VIP可见" inactive-text="所有用户可见" />
          </el-form-item>
          <el-form-item label="资料文件">
            <el-upload
              class="upload-demo"
              action=""
              :auto-upload="false"
              :on-change="handleFileChange"
              :file-list="fileList"
              :limit="1"
              accept=".pdf,.doc,.docx,.txt,.zip,.rar"
            >
              <el-button type="primary">选择文件</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  请选择 PDF、Word、TXT 或压缩文件
                </div>
              </template>
            </el-upload>
          </el-form-item>
          <el-form-item label="封面图片">
            <el-upload
              class="upload-demo"
              action=""
              :auto-upload="false"
              :on-change="handleCoverChange"
              :file-list="coverList"
              :limit="1"
              accept=".jpg,.jpeg,.png,.gif"
            >
              <el-button type="primary">选择图片</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  请选择 JPG、PNG 或 GIF 图片
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showUploadDialog = false">取消</el-button>
            <el-button type="primary" @click="uploadMaterial">上传</el-button>
          </span>
        </template>
      </el-dialog>
      
      <!-- 编辑资料对话框 -->
      <el-dialog
        v-model="showEditDialog"
        title="编辑学习资料"
        width="800px"
      >
        <el-form :model="editForm" label-width="100px">
          <el-form-item label="资料标题">
            <el-input v-model="editForm.title" placeholder="请输入资料标题" />
          </el-form-item>
          <el-form-item label="资料描述">
            <el-input
              v-model="editForm.description"
              type="textarea"
              placeholder="请输入资料描述"
              :rows="3"
            />
          </el-form-item>
          <el-form-item label="资料类型">
            <el-select v-model="editForm.type" placeholder="请选择资料类型">
              <el-option label="考研" value="1" />
              <el-option label="考公" value="2" />
            </el-select>
          </el-form-item>
          <el-form-item label="资料分类">
            <el-select v-model="editForm.category_id" placeholder="请选择资料分类">
              <el-option
                v-for="category in categories"
                :key="category.id"
                :label="category.name"
                :value="category.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="科目">
            <el-input v-model="editForm.subject" placeholder="请输入科目" />
          </el-form-item>
          <el-form-item label="VIP专属">
            <el-switch v-model="editForm.is_vip" active-text="仅VIP可见" inactive-text="所有用户可见" />
          </el-form-item>
          <el-form-item label="资料文件">
            <el-upload
              class="upload-demo"
              action=""
              :auto-upload="false"
              :on-change="handleEditFileChange"
              :file-list="editFileList"
              :limit="1"
              accept=".pdf,.doc,.docx,.txt,.zip,.rar"
            >
              <el-button type="primary">选择文件</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  请选择 PDF、Word、TXT 或压缩文件
                </div>
              </template>
            </el-upload>
            <div v-if="editForm.file_url" class="current-file">
              当前文件: {{ editForm.title }}{{ getFileExtension(editForm.file_url) }}
            </div>
          </el-form-item>
          <el-form-item label="封面图片">
            <el-upload
              class="upload-demo"
              action=""
              :auto-upload="false"
              :on-change="handleEditCoverChange"
              :file-list="editCoverList"
              :limit="1"
              accept=".jpg,.jpeg,.png,.gif"
            >
              <el-button type="primary">选择图片</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  请选择 JPG、PNG 或 GIF 图片
                </div>
              </template>
            </el-upload>
            <div v-if="editForm.cover_image" class="current-file">
              当前封面: <el-image :src="apiBaseUrl + editForm.cover_image" :preview-src-list="[apiBaseUrl + editForm.cover_image]" style="width: 100px; height: 100px;" fit="cover" />
            </div>
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showEditDialog = false">取消</el-button>
            <el-button type="primary" @click="updateMaterial">保存</el-button>
          </span>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

// 获取 API 基础 URL
const apiBaseUrl = import.meta.env.VITE_API_URL

// 资料列表相关
const materials = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')
const typeFilter = ref('')
const categoryFilter = ref('')
const vipFilter = ref('')

// 分类列表
const categories = ref([])

// 上传资料相关
const showUploadDialog = ref(false)
const uploadForm = ref({
  title: '',
  description: '',
  type: '',
  category_id: '',
  subject: '',
  is_vip: false
})
const fileList = ref([])
const coverList = ref([])

// 编辑资料相关
const showEditDialog = ref(false)
const editForm = ref({
  id: '',
  title: '',
  description: '',
  type: '',
  category_id: '',
  subject: '',
  is_vip: false,
  file_url: '',
  cover_image: ''
})
const editFileList = ref([])
const editCoverList = ref([])

// 获取资料分类列表
const getCategories = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/learning_materials/categories', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (response.success) {
      categories.value = response.data
    }
  } catch (error) {
    console.error('获取资料分类列表失败:', error)
    ElMessage.error('获取资料分类列表失败')
  }
}

// 获取学习资料列表
const getMaterials = async () => {
  try {
    loading.value = true
    const token = localStorage.getItem('token')
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (searchQuery.value) {
      params.keyword = searchQuery.value
    }
    if (typeFilter.value) {
      params.type = typeFilter.value
    }
    if (categoryFilter.value) {
      params.category_id = categoryFilter.value
    }
    if (vipFilter.value) {
      params.is_vip = vipFilter.value === 'true'
    }
    
    const response = await axios.get('/api/v1/learning_materials/materials', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params
    })
    
    if (response.success) {
      materials.value = response.data.items || []
      total.value = response.data.total
    } else {
      materials.value = []
      total.value = 0
    }
  } catch (error) {
    console.error('获取学习资料列表失败:', error)
    materials.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 处理分页大小变化
const handleSizeChange = (size) => {
  pageSize.value = size
  getMaterials()
}

// 处理当前页码变化
const handleCurrentChange = (current) => {
  currentPage.value = current
  getMaterials()
}

// 处理文件选择
const handleFileChange = (file) => {
  fileList.value = [file]
}

// 处理封面图片选择
const handleCoverChange = (file) => {
  coverList.value = [file]
}

// 上传资料
const uploadMaterial = async () => {
  try {
    if (!uploadForm.value.title) {
      ElMessage.error('请输入资料标题')
      return
    }
    if (!uploadForm.value.description) {
      ElMessage.error('请输入资料描述')
      return
    }
    if (!uploadForm.value.type) {
      ElMessage.error('请选择资料类型')
      return
    }
    if (!uploadForm.value.category_id) {
      ElMessage.error('请选择资料分类')
      return
    }
    if (!uploadForm.value.subject) {
      ElMessage.error('请输入科目')
      return
    }
    if (fileList.value.length === 0) {
      ElMessage.error('请选择资料文件')
      return
    }
    
    const token = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('title', uploadForm.value.title)
    formData.append('description', uploadForm.value.description)
    formData.append('type', uploadForm.value.type)
    formData.append('category_id', uploadForm.value.category_id)
    formData.append('subject', uploadForm.value.subject)
    formData.append('is_vip', uploadForm.value.is_vip ? 'true' : 'false')
    formData.append('file', fileList.value[0].raw)
    if (coverList.value.length > 0) {
      formData.append('cover_image', coverList.value[0].raw)
    }
    
    const response = await axios.post('/api/v1/learning_materials/materials', formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    if (response.success) {
      ElMessage.success('上传资料成功')
      showUploadDialog.value = false
      // 重置表单
      uploadForm.value = {
        title: '',
        description: '',
        type: '',
        category_id: '',
        subject: '',
        is_vip: false
      }
      fileList.value = []
      coverList.value = []
      // 刷新资料列表
      getMaterials()
    } else {
      ElMessage.error('上传资料失败: ' + response.data.message)
    }
  } catch (error) {
    console.error('上传资料失败:', error)
    ElMessage.error('上传资料失败')
  }
}

// 显示编辑对话框
const openEditDialog = (material) => {
  editForm.value = {
    id: material.id,
    title: material.title,
    description: material.description,
    type: material.type,
    category_id: material.category_id,
    subject: material.subject,
    is_vip: material.is_vip || false,
    file_url: material.file_url,
    cover_image: material.cover_image
  }
  editFileList.value = []
  editCoverList.value = []
  showEditDialog.value = true
}

// 处理编辑文件选择
const handleEditFileChange = (file) => {
  editFileList.value = [file]
}

// 处理编辑封面图片选择
const handleEditCoverChange = (file) => {
  editCoverList.value = [file]
}

// 更新资料
const updateMaterial = async () => {
  try {
    if (!editForm.value.title) {
      ElMessage.error('请输入资料标题')
      return
    }
    if (!editForm.value.description) {
      ElMessage.error('请输入资料描述')
      return
    }
    if (!editForm.value.type) {
      ElMessage.error('请选择资料类型')
      return
    }
    if (!editForm.value.category_id) {
      ElMessage.error('请选择资料分类')
      return
    }
    if (!editForm.value.subject) {
      ElMessage.error('请输入科目')
      return
    }
    
    const token = localStorage.getItem('token')
    const formData = new FormData()
    formData.append('title', editForm.value.title)
    formData.append('description', editForm.value.description)
    formData.append('type', editForm.value.type)
    formData.append('category_id', editForm.value.category_id)
    formData.append('subject', editForm.value.subject)
    formData.append('is_vip', editForm.value.is_vip ? 'true' : 'false')
    if (editFileList.value.length > 0) {
      formData.append('file', editFileList.value[0].raw)
    }
    if (editCoverList.value.length > 0) {
      formData.append('cover_image', editCoverList.value[0].raw)
    }
    
    const response = await axios.put(`/api/v1/learning_materials/materials/${editForm.value.id}`, formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    
    if (response.success) {
      ElMessage.success('更新资料成功')
      showEditDialog.value = false
      // 刷新资料列表
      getMaterials()
    } else {
      ElMessage.error('更新资料失败: ' + response.message)
    }
  } catch (error) {
    console.error('更新资料失败:', error)
    ElMessage.error('更新资料失败')
  }
}

// 删除资料
const deleteMaterial = async (id) => {
  try {
    // 确认删除
    const confirmed = await ElMessageBox.confirm('确定要删除该资料吗？此操作不可恢复！', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    if (confirmed) {
      const token = localStorage.getItem('token')
      const response = await axios.delete(`/api/v1/learning_materials/materials/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (response.success) {
        ElMessage.success('删除资料成功')
        // 刷新资料列表
        getMaterials()
      } else {
        ElMessage.error('删除资料失败: ' + response.message)
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除资料失败:', error)
      ElMessage.error('删除资料失败')
    }
  }
}

// 格式化文件大小
const formatFileSize = (size) => {
  if (size < 1024) {
    return size + ' B'
  } else if (size < 1024 * 1024) {
    return (size / 1024).toFixed(2) + ' KB'
  } else {
    return (size / (1024 * 1024)).toFixed(2) + ' MB'
  }
}

// 获取文件扩展名
const getFileExtension = (url) => {
  return url.substring(url.lastIndexOf('.'))
}

onMounted(() => {
  getCategories()
  getMaterials()
})
</script>

<style scoped>
.admin-content {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
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

.current-file {
  margin-top: 10px;
  font-size: 14px;
  color: #666;
}

.dialog-footer {
  text-align: right;
}

.rating-number {
  display: inline-block;
  padding: 4px 8px;
  background-color: #f0f9ff;
  color: #1890ff;
  border-radius: 4px;
  font-weight: 500;
  font-size: 14px;
}
</style>
