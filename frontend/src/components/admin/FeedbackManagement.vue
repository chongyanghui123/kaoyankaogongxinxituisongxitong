<template>
  <div class="feedback-management">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h2 class="title">体验反馈管理</h2>
        </div>
      </template>
      
      <div class="search-filter">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索反馈内容"
          prefix-icon="Search"
          style="width: 300px; margin-bottom: 20px"
          @keyup.enter="handleSearch"
        >
          <template #append>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
          </template>
        </el-input>
        
        <el-select
          v-model="statusFilter"
          placeholder="筛选状态"
          style="width: 150px; margin-right: 10px"
          @change="handleSearch"
        >
          <el-option label="全部" value="" />
          <el-option label="待处理" value="pending" />
          <el-option label="已处理" value="processed" />
        </el-select>
        
        <el-select
          v-model="typeFilter"
          placeholder="筛选类型"
          style="width: 150px"
          @change="handleSearch"
        >
          <el-option label="全部" value="" />
          <el-option label="功能建议" value="1" />
          <el-option label="问题反馈" value="2" />
          <el-option label="其他" value="3" />
        </el-select>
      </div>
      
      <el-table
        :data="feedbacks"
        style="width: 100%"
        border
        stripe
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.type === 1" type="info">功能建议</el-tag>
            <el-tag v-else-if="scope.row.type === 2" type="warning">问题反馈</el-tag>
            <el-tag v-else type="success">其他</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="反馈内容">
          <template #default="scope">
            <div class="content-cell" :title="scope.row.content">
              {{ scope.row.content }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="reply" label="管理员回复" width="200">
          <template #default="scope">
            <div v-if="scope.row.reply" class="reply-content">{{ scope.row.reply }}</div>
            <div v-else class="no-reply">暂无回复</div>
          </template>
        </el-table-column>
        <el-table-column prop="contact" label="联系方式" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.status === 'pending'" type="danger">待处理</el-tag>
            <el-tag v-else type="success">已处理</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" width="180" />
        <el-table-column label="操作" width="280">
          <template #default="scope">
            <el-button
              type="success"
              size="small"
              @click="handleReply(scope.row)"
            >
              {{ scope.row.reply ? '修改回复' : '回复' }}
            </el-button>
            <el-button
              v-if="scope.row.status === 'pending'"
              type="primary"
              size="small"
              @click="handleProcess(scope.row)"
            >
              标记已处理
            </el-button>
            <el-button
              v-else
              type="info"
              size="small"
              @click="handleProcess(scope.row)"
            >
              标记待处理
            </el-button>
            <el-button
              v-if="scope.row.reply"
              type="danger"
              size="small"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
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
    </el-card>
    
    <!-- 回复对话框 -->
    <el-dialog
      v-model="replyDialogVisible"
      :title="currentFeedback?.reply ? '修改回复' : '回复反馈'"
      width="500px"
    >
      <el-form :model="replyForm" label-width="80px">
        <el-form-item label="反馈内容">
          <div class="feedback-content-preview">{{ currentFeedback?.content }}</div>
        </el-form-item>
        <el-form-item label="回复内容">
          <el-input
            v-model="replyForm.reply"
            type="textarea"
            :rows="5"
            placeholder="请输入回复内容"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="replyDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReply">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from '@/utils/axios'

const feedbacks = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchKeyword = ref('')
const statusFilter = ref('')
const typeFilter = ref('')
const replyDialogVisible = ref(false)
const currentFeedback = ref(null)
const replyForm = ref({
  reply: ''
})

const fetchFeedbacks = async () => {
  try {
    const response = await axios.get('/api/v1/feedback/admin', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    let filteredFeedbacks = response.data || []
    
    // 应用搜索和筛选
    if (searchKeyword.value) {
      filteredFeedbacks = filteredFeedbacks.filter(item => 
        item.content.includes(searchKeyword.value)
      )
    }
    
    if (statusFilter.value) {
      filteredFeedbacks = filteredFeedbacks.filter(item => 
        item.status === statusFilter.value
      )
    }
    
    if (typeFilter.value) {
      filteredFeedbacks = filteredFeedbacks.filter(item => 
        item.type.toString() === typeFilter.value
      )
    }
    
    total.value = filteredFeedbacks.length
    
    // 分页
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    feedbacks.value = filteredFeedbacks.slice(start, end)
  } catch (error) {
    console.error('获取反馈列表失败:', error)
    ElMessage.error('获取反馈列表失败')
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchFeedbacks()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchFeedbacks()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  fetchFeedbacks()
}

const handleProcess = async (feedback) => {
  try {
    const newStatus = feedback.status === 'pending' ? 'processed' : 'pending'
    
    await axios.put(`/api/v1/feedback/${feedback.id}/status`, {
      status: newStatus
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    ElMessage.success('状态更新成功')
    fetchFeedbacks()
  } catch (error) {
    console.error('更新状态失败:', error)
    ElMessage.error('更新状态失败')
  }
}

const handleReply = (feedback) => {
  currentFeedback.value = feedback
  replyForm.value.reply = feedback.reply || ''
  replyDialogVisible.value = true
}

const submitReply = async () => {
  if (!replyForm.value.reply.trim()) {
    ElMessage.warning('请输入回复内容')
    return
  }
  
  try {
    await axios.put(`/api/v1/feedback/${currentFeedback.value.id}/reply`, {
      reply: replyForm.value.reply
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    ElMessage.success('回复成功')
    replyDialogVisible.value = false
    fetchFeedbacks()
  } catch (error) {
    console.error('回复失败:', error)
    ElMessage.error('回复失败')
  }
}

const handleDelete = async (feedback) => {
  ElMessageBox.confirm(
    '确定要删除这条反馈吗？删除后将无法恢复。',
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await axios.delete(`/api/v1/feedback/${feedback.id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      ElMessage.success('删除成功')
      fetchFeedbacks()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 用户取消删除
  })
}

onMounted(() => {
  fetchFeedbacks()
})
</script>

<style scoped>
.feedback-management {
  padding: 0 20px;
}

.content-cell {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 400px;
}

.reply-content {
  font-size: 13px;
  color: #606266;
  line-height: 1.5;
  word-break: break-all;
}

.no-reply {
  color: #c0c4cc;
  font-size: 13px;
  text-align: center;
}

.feedback-content-preview {
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  color: #606266;
  line-height: 1.5;
}

.search-filter {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>