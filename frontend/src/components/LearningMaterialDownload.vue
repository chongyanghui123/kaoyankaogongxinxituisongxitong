<template>
  <div class="learning-material-download">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">学习资料下载</h3>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
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
          <el-col :span="8">
            <el-select v-model="typeFilter" placeholder="按类型筛选" clearable @change="getMaterials">
              <el-option label="全部" value="" />
              <el-option label="考研" value="1" />
              <el-option label="考公" value="2" />
            </el-select>
          </el-col>
          <el-col :span="8">
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
        </el-row>
      </div>
      
      <!-- 学习资料列表 -->
      <div class="materials-grid" v-loading="loading">
        <el-card
          v-for="material in materials"
          :key="material.id"
          class="material-card"
          :body-style="{ padding: '0' }"
        >
          <div class="material-card-body">
            <div class="material-cover" v-if="material.cover_image">
              <el-image :src="material.cover_image" fit="cover" />
            </div>
            <div class="material-cover placeholder" v-else>
              <el-icon class="cover-icon"><Picture /></el-icon>
            </div>
            <div class="material-content">
              <h4 class="material-title">{{ material.title }}</h4>
              <p class="material-description">{{ truncateText(material.description, 100) }}</p>
              <div class="material-meta">
                <el-tag :type="material.type === 1 ? 'primary' : 'success'" size="small">{{ material.type === 1 ? '考研' : '考公' }}</el-tag>
                <span class="material-category">{{ material.category_name }}</span>
                <span class="material-subject">{{ material.subject }}</span>
              </div>
              <div class="material-info">
                <span class="material-size">{{ formatFileSize(material.file_size) }}</span>
                <span class="material-downloads">{{ material.download_count }} 次下载</span>
                <el-rate v-model="material.rating" disabled :max="5" :show-score="false" />
              </div>
              <div class="material-actions">
                <el-button type="primary" @click="showMaterialDetail(material)">查看详情</el-button>
                <el-button type="success" @click="downloadMaterial(material.id)">下载</el-button>
              </div>
            </div>
          </div>
        </el-card>
      </div>
      
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
      
      <!-- 下载记录 -->
      <el-card class="content-card" style="margin-top: 20px;">
        <template #header>
          <div class="card-header">
            <h3 class="title">下载记录</h3>
          </div>
        </template>
        <el-table :data="downloads" style="width: 100%" v-loading="downloadsLoading">
          <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
          <el-table-column prop="material_title" label="资料标题" min-width="200" />
          <el-table-column prop="material_type" label="类型" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.material_type === 1 ? 'primary' : 'success'">
                {{ scope.row.material_type === 1 ? '考研' : '考公' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="download_time" label="下载时间" width="180" />
          <el-table-column label="操作" width="120">
            <template #default="scope">
              <el-button type="primary" size="small" @click="downloadMaterial(scope.row.material_id)">重新下载</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 下载记录分页 -->
        <div class="pagination" v-if="!downloadsLoading && downloads.length > 0">
          <el-pagination
            v-model:current-page="downloadsCurrentPage"
            v-model:page-size="downloadsPageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="downloadsTotal"
            @size-change="handleDownloadsSizeChange"
            @current-change="handleDownloadsCurrentChange"
          />
        </div>
      </el-card>
      
      <!-- 资料详情对话框 -->
      <el-dialog
        v-model="showDetailDialog"
        :title="currentMaterial.title || '资料详情'"
        width="800px"
      >
        <div class="material-detail">
          <div class="detail-cover" v-if="currentMaterial.cover_image">
            <el-image :src="currentMaterial.cover_image" fit="cover" />
          </div>
          <div class="detail-info">
            <h3>{{ currentMaterial.title }}</h3>
            <div class="detail-meta">
              <el-tag :type="currentMaterial.type === 1 ? 'primary' : 'success'">
                {{ currentMaterial.type === 1 ? '考研' : '考公' }}
              </el-tag>
              <span class="detail-category">{{ currentMaterial.category_name }}</span>
              <span class="detail-subject">{{ currentMaterial.subject }}</span>
            </div>
            <div class="detail-stats">
              <span class="detail-size">{{ formatFileSize(currentMaterial.file_size) }}</span>
              <span class="detail-downloads">{{ currentMaterial.download_count }} 次下载</span>
              <el-rate v-model="currentMaterial.rating" disabled :max="5" />
            </div>
            <div class="detail-description">
              <h4>资料描述</h4>
              <p>{{ currentMaterial.description }}</p>
            </div>
            <div class="detail-actions">
              <el-button type="primary" @click="downloadMaterial(currentMaterial.id)">下载</el-button>
              <el-button type="success" @click="rateMaterial(currentMaterial.id)">评分</el-button>
              <el-button @click="showCommentDialog = true">评论</el-button>
            </div>
          </div>
          
          <!-- 评论列表 -->
          <div class="comments-section" style="margin-top: 20px;">
            <h4>评论</h4>
            <el-list
              v-for="comment in comments"
              :key="comment.id"
              class="comment-item"
            >
              <el-list-item>
                <template #default>
                  <div class="comment-content">
                    <div class="comment-header">
                      <span class="comment-user">{{ comment.user_name }}</span>
                      <span class="comment-time">{{ comment.created_at }}</span>
                    </div>
                    <div class="comment-text">{{ comment.comment }}</div>
                  </div>
                </template>
              </el-list-item>
            </el-list>
            <div v-if="comments.length === 0" class="no-comments">
              暂无评论
            </div>
          </div>
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showDetailDialog = false">关闭</el-button>
          </span>
        </template>
      </el-dialog>
      
      <!-- 评分对话框 -->
      <el-dialog
        v-model="showRateDialog"
        title="给资料评分"
        width="400px"
      >
        <div class="rate-dialog">
          <el-rate v-model="ratingValue" :max="5" show-score />
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showRateDialog = false">取消</el-button>
            <el-button type="primary" @click="submitRating">提交评分</el-button>
          </span>
        </template>
      </el-dialog>
      
      <!-- 评论对话框 -->
      <el-dialog
        v-model="showCommentDialog"
        title="发表评论"
        width="600px"
      >
        <div class="comment-dialog">
          <el-input
            v-model="commentContent"
            type="textarea"
            placeholder="请输入评论内容"
            :rows="4"
          />
        </div>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="showCommentDialog = false">取消</el-button>
            <el-button type="primary" @click="submitComment">提交评论</el-button>
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
import { Picture } from '@element-plus/icons-vue'

// 资料列表相关
const materials = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')
const typeFilter = ref('')
const categoryFilter = ref('')

// 分类列表
const categories = ref([])

// 下载记录相关
const downloads = ref([])
const downloadsLoading = ref(false)
const downloadsCurrentPage = ref(1)
const downloadsPageSize = ref(10)
const downloadsTotal = ref(0)

// 资料详情相关
const showDetailDialog = ref(false)
const currentMaterial = ref({})
const comments = ref([])

// 评分相关
const showRateDialog = ref(false)
const ratingValue = ref(0)
let currentRatingMaterialId = ref(0)

// 评论相关
const showCommentDialog = ref(false)
const commentContent = ref('')

// 获取资料分类列表
const getCategories = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/learning_materials/categories', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (response.data.success) {
      categories.value = response.data.data
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
    
    const response = await axios.get('/api/v1/learning_materials/materials', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params
    })
    
    if (response.data.success) {
      materials.value = response.data.data.items || []
      total.value = response.data.data.total
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

// 获取下载记录
const getDownloads = async () => {
  try {
    downloadsLoading.value = true
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/learning_materials/downloads', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        page: downloadsCurrentPage.value,
        page_size: downloadsPageSize.value
      }
    })
    
    if (response.data.success) {
      downloads.value = response.data.data.items || []
      downloadsTotal.value = response.data.data.total
    } else {
      downloads.value = []
      downloadsTotal.value = 0
    }
  } catch (error) {
    console.error('获取下载记录失败:', error)
    downloads.value = []
    downloadsTotal.value = 0
  } finally {
    downloadsLoading.value = false
  }
}

// 处理下载记录分页大小变化
const handleDownloadsSizeChange = (size) => {
  downloadsPageSize.value = size
  getDownloads()
}

// 处理下载记录当前页码变化
const handleDownloadsCurrentChange = (current) => {
  downloadsCurrentPage.value = current
  getDownloads()
}

// 显示资料详情
const showMaterialDetail = async (material) => {
  try {
    currentMaterial.value = material
    // 获取评论
    const token = localStorage.getItem('token')
    const response = await axios.get(`/api/v1/learning_materials/materials/${material.id}/comments`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        page: 1,
        page_size: 100
      }
    })
    
    if (response.data.success) {
      comments.value = response.data.data.items || []
    } else {
      comments.value = []
    }
    showDetailDialog.value = true
  } catch (error) {
    console.error('获取资料详情失败:', error)
    ElMessage.error('获取资料详情失败')
  }
}

// 下载资料
const downloadMaterial = async (materialId) => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`/api/v1/learning_materials/materials/${materialId}/download`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      responseType: 'blob'
    })
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    // 获取资料标题作为文件名
    const material = materials.value.find(m => m.id === materialId) || downloads.value.find(d => d.material_id === materialId)
    const filename = material ? material.material_title || material.title : `资料${materialId}`
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success('下载资料成功')
    // 刷新下载记录
    getDownloads()
  } catch (error) {
    console.error('下载资料失败:', error)
    ElMessage.error('下载资料失败')
  }
}

// 评分资料
const rateMaterial = (materialId) => {
  currentRatingMaterialId.value = materialId
  ratingValue.value = 0
  showRateDialog.value = true
}

// 提交评分
const submitRating = async () => {
  try {
    if (ratingValue.value === 0) {
      ElMessage.error('请选择评分')
      return
    }
    
    const token = localStorage.getItem('token')
    const response = await axios.post(`/api/v1/learning_materials/materials/${currentRatingMaterialId.value}/rating`, {
      rating: ratingValue.value
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.data.success) {
      ElMessage.success('评分成功')
      showRateDialog.value = false
      // 刷新资料列表
      getMaterials()
    } else {
      ElMessage.error('评分失败: ' + response.data.message)
    }
  } catch (error) {
    console.error('评分失败:', error)
    ElMessage.error('评分失败')
  }
}

// 提交评论
const submitComment = async () => {
  try {
    if (!commentContent.value) {
      ElMessage.error('请输入评论内容')
      return
    }
    
    const token = localStorage.getItem('token')
    const response = await axios.post(`/api/v1/learning_materials/materials/${currentMaterial.value.id}/comment`, {
      comment: commentContent.value
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.data.success) {
      ElMessage.success('评论成功')
      showCommentDialog.value = false
      commentContent.value = ''
      // 刷新评论列表
      const commentResponse = await axios.get(`/api/v1/learning_materials/materials/${currentMaterial.value.id}/comments`, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        params: {
          page: 1,
          page_size: 100
        }
      })
      
      if (commentResponse.data.success) {
        comments.value = commentResponse.data.data.items || []
      }
    } else {
      ElMessage.error('评论失败: ' + response.data.message)
    }
  } catch (error) {
    console.error('评论失败:', error)
    ElMessage.error('评论失败')
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

// 截断文本
const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) {
    return text
  }
  return text.substring(0, maxLength) + '...'
}

onMounted(() => {
  getCategories()
  getMaterials()
  getDownloads()
})
</script>

<style scoped>
.learning-material-download {
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

.materials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.material-card {
  height: 100%;
}

.material-card-body {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.material-cover {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.material-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.material-cover.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  height: 200px;
}

.cover-icon {
  font-size: 48px;
  color: #999;
}

.material-content {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.material-title {
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: 500;
}

.material-description {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

.material-meta {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.material-category {
  font-size: 14px;
  color: #666;
}

.material-subject {
  font-size: 14px;
  color: #666;
}

.material-info {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 14px;
  color: #666;
}

.material-actions {
  margin-top: auto;
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.material-detail {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-cover {
  width: 100%;
  height: 300px;
  overflow: hidden;
  margin-bottom: 20px;
}

.detail-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.detail-category {
  font-size: 14px;
  color: #666;
}

.detail-subject {
  font-size: 14px;
  color: #666;
}

.detail-stats {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 14px;
  color: #666;
}

.detail-description {
  margin-top: 10px;
}

.detail-description h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: 500;
}

.detail-description p {
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
  color: #333;
}

.detail-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.comments-section {
  margin-top: 30px;
}

.comments-section h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 500;
}

.comment-item {
  border-bottom: 1px solid #f0f0f0;
  padding: 10px 0;
}

.comment-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-user {
  font-size: 14px;
  font-weight: 500;
}

.comment-time {
  font-size: 12px;
  color: #999;
}

.comment-text {
  font-size: 14px;
  line-height: 1.4;
  color: #333;
}

.no-comments {
  text-align: center;
  color: #999;
  padding: 20px 0;
}

.rate-dialog {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.comment-dialog {
  padding: 10px 0;
}

.dialog-footer {
  text-align: right;
}
</style>
