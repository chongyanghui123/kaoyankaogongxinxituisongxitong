<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">评论管理</h3>
          <el-button type="primary" class="export-btn" @click="exportComments">导出评论</el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索评论内容或用户名"
              clearable
              prefix-icon="Search"
              @keyup.enter="getComments"
            >
              <template #append>
                <el-button type="primary" @click="getComments">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="6">
            <el-select v-model="typeFilter" placeholder="按类型筛选" clearable @change="getComments">
              <el-option label="全部类型" value="" />
              <el-option label="考研" value="1" />
              <el-option label="考公" value="2" />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="dateFilter" placeholder="按时间筛选" clearable @change="getComments">
              <el-option label="全部时间" value="" />
              <el-option label="今天" value="today" />
              <el-option label="本周" value="week" />
              <el-option label="本月" value="month" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-button type="success" @click="resetFilters">重置</el-button>
          </el-col>
        </el-row>
      </div>
      
      <!-- 评论表格 -->
      <el-table :data="comments" style="width: 100%" :default-sort="{ prop: 'created_at', order: 'descending' }">
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="user_name" label="用户名" min-width="100" show-overflow-tooltip />
        <el-table-column prop="material_title" label="资料标题" min-width="150" show-overflow-tooltip />
        <el-table-column prop="comment" label="评论内容" min-width="200" show-overflow-tooltip />
        <el-table-column prop="created_at" label="评论时间" min-width="160" align="center" />
        <el-table-column prop="material_type" label="类型" width="80" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.material_type === 1 ? 'primary' : 'success'">
              {{ scope.row.material_type === 1 ? '考研' : '考公' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="depth" label="层级" width="80" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.depth > 0" type="warning">
              {{ scope.row.depth }}级回复
            </el-tag>
            <el-tag v-else type="info">
              一级评论
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template #default="scope">
            <el-button 
              size="small" 
              type="primary" 
              @click="viewComment(scope.row)"
              style="margin-right: 5px"
            >
              <el-icon><View /></el-icon>
              查看
            </el-button>
            <el-button 
              size="small" 
              type="danger" 
              @click="deleteComment(scope.row.id)"
            >
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 评论详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="评论详情"
      width="60%"
      :before-close="handleDetailClose"
    >
      <div v-if="currentComment" class="comment-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="评论用户">{{ currentComment.user_name }}</el-descriptions-item>
          <el-descriptions-item label="评论资料">{{ currentComment.material_title }}</el-descriptions-item>
          <el-descriptions-item label="评论内容">{{ currentComment.comment }}</el-descriptions-item>
          <el-descriptions-item label="评论时间">{{ currentComment.created_at }}</el-descriptions-item>
          <el-descriptions-item label="评论类型">
            <el-tag :type="currentComment.material_type === 1 ? 'primary' : 'success'">
              {{ currentComment.material_type === 1 ? '考研' : '考公' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item v-if="currentComment.parent_comment" label="父评论内容">{{ currentComment.parent_comment }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDetailDialog = false">关闭</el-button>
          <el-button type="danger" @click="deleteCurrentComment">删除评论</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { View, Delete } from '@element-plus/icons-vue'

const comments = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchQuery = ref('')
const typeFilter = ref('')
const dateFilter = ref('')
const showDetailDialog = ref(false)
const currentComment = ref(null)

// 获取评论列表
const getComments = async () => {
  try {
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
    if (dateFilter.value) {
      params.date = dateFilter.value
    }
    
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/learning_materials/comments', {
      params,
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.data.success) {
      comments.value = response.data.data.items
      total.value = response.data.data.total
    } else {
      ElMessage.error('获取评论失败')
    }
  } catch (error) {
    console.error('获取评论失败:', error)
    ElMessage.error('获取评论失败')
  }
}

// 查看评论详情
const viewComment = (comment) => {
  currentComment.value = comment
  showDetailDialog.value = true
}

// 删除评论
const deleteComment = async (commentId) => {
  try {
    await ElMessageBox.confirm('确定要删除这条评论吗？删除后无法恢复。', '删除确认', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const token = localStorage.getItem('token')
    await axios.delete(`/api/v1/learning_materials/comments/${commentId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    ElMessage.success('删除成功')
    getComments()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除评论失败:', error)
      ElMessage.error('删除评论失败')
    }
  }
}

// 删除当前查看的评论
const deleteCurrentComment = async () => {
  if (!currentComment.value) return
  await deleteComment(currentComment.value.id)
  showDetailDialog.value = false
  currentComment.value = null
}

// 重置筛选条件
const resetFilters = () => {
  searchQuery.value = ''
  typeFilter.value = ''
  dateFilter.value = ''
  currentPage.value = 1
  getComments()
}

// 导出评论
const exportComments = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/learning_materials/comments/export', {
      responseType: 'blob',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `comments_${new Date().toISOString().split('T')[0]}.csv`)
    document.body.appendChild(link)
    link.click()
    
    // 清理
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出评论失败:', error)
    ElMessage.error('导出评论失败')
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  getComments()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  getComments()
}

// 关闭详情对话框
const handleDetailClose = () => {
  showDetailDialog.value = false
  currentComment.value = null
}

onMounted(() => {
  getComments()
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
  font-weight: bold;
  color: #333;
}

.search-filter {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.comment-detail {
  padding: 10px 0;
}
</style>
