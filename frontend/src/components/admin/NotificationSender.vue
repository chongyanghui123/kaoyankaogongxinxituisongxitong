<template>
  <div class="notification-sender">
    <!-- 发送通知表单 -->
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <h2>发送通知</h2>
        </div>
      </template>
      
      <el-form :model="notificationForm" ref="notificationFormRef" label-width="120px" :rules="rules">
        <el-form-item label="发送对象" prop="userType">
          <el-radio-group v-model="notificationForm.userType">
            <el-radio :value="1">考研用户</el-radio>
            <el-radio :value="2">考公用户</el-radio>
            <el-radio :value="3">全部用户</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="通知标题" prop="title">
          <el-input v-model="notificationForm.title" placeholder="请输入通知标题" maxlength="50" show-word-limit />
        </el-form-item>
        
        <el-form-item label="通知内容" prop="content">
          <el-input v-model="notificationForm.content" type="textarea" :rows="5" placeholder="请输入通知内容" maxlength="200" show-word-limit />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="sendNotification" :loading="loading">发送通知</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 通知历史记录 -->
    <el-card class="box-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <h2>通知历史记录</h2>
          <el-input 
            v-model="searchQuery" 
            placeholder="搜索通知内容" 
            clearable 
            style="width: 200px;"
            @input="handleSearch"
          >
            <template #prepend>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </template>

      <el-table :data="historyData" v-loading="historyLoading">
        <el-table-column prop="title" label="通知标题" min-width="150" show-overflow-tooltip />
        <el-table-column prop="content" label="通知内容" min-width="300" show-overflow-tooltip />
        <el-table-column prop="send_time" label="发送时间" width="180" />
        <el-table-column prop="receiver_count" label="接收人数" width="120" />
        <el-table-column prop="push_status" label="发送状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.push_status === 1 ? 'success' : 'danger'">
              {{ scope.row.push_status === 1 ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button 
              type="danger" 
              text 
              size="small"
              @click="deleteHistory(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-if="total > 0"
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from '@/utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

const notificationFormRef = ref()

const notificationForm = reactive({
  userType: 3,
  title: '',
  content: ''
})

const loading = ref(false)
const historyLoading = ref(false)

const rules = {
  userType: [
    { required: true, message: '请选择发送对象', trigger: 'change' }
  ],
  title: [
    { required: true, message: '请输入通知标题', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入通知内容', trigger: 'blur' }
  ]
}

// 历史记录相关数据
const historyData = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const searchQuery = ref('')

const sendNotification = async () => {
  try {
    const valid = await notificationFormRef.value.validate()
    if (!valid) return
    
    await ElMessageBox.confirm('确定要发送此通知吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    
    const token = localStorage.getItem('token')
    const response = await axios.post('/api/v1/admin/notification/send', notificationForm, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    if (response.success) {
      ElMessage.success(`成功发送通知给 ${response.data.user_count} 个用户`)
      resetForm()
      // 发送成功后刷新历史记录
      await getHistory()
    } else {
      ElMessage.error(response.message || '发送失败')
    }
  } catch (error) {
    if (error.name !== 'Error' || error.message !== 'cancel') {
      console.error('发送通知失败:', error)
      ElMessage.error(error.response?.data?.message || '发送失败')
    }
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  notificationFormRef.value?.resetFields()
  notificationForm.userType = 3
  notificationForm.title = ''
  notificationForm.content = ''
}

// 获取历史记录
const getHistory = async () => {
  try {
    historyLoading.value = true
    const token = localStorage.getItem('token')
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value
    }
    
    const response = await axios.get('/api/v1/admin/notification/history', {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params
    })
    
    if (response.success) {
      historyData.value = response.data.items
      total.value = response.data.total
    } else {
      ElMessage.error(response.message || '获取历史记录失败')
    }
  } catch (error) {
    console.error('获取历史记录失败:', error)
    ElMessage.error(error.response?.data?.message || '获取历史记录失败')
  } finally {
    historyLoading.value = false
  }
}

// 搜索历史记录
const handleSearch = async () => {
  currentPage.value = 1
  await getHistory()
}

// 处理分页大小变化
const handleSizeChange = async (size) => {
  pageSize.value = size
  currentPage.value = 1
  await getHistory()
}

// 处理页码变化
const handleCurrentChange = async (page) => {
  currentPage.value = page
  await getHistory()
}

// 删除历史记录
const deleteHistory = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这条历史记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const token = localStorage.getItem('token')
    const response = await axios.delete(`/api/v1/admin/notification/history/${row.id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    if (response.success) {
      ElMessage.success('删除成功')
      await getHistory()
    } else {
      ElMessage.error(response.message || '删除失败')
    }
  } catch (error) {
    if (error.name !== 'Error' || error.message !== 'cancel') {
      console.error('删除历史记录失败:', error)
      ElMessage.error(error.response?.data?.message || '删除失败')
    }
  }
}

// 页面加载时获取历史记录
onMounted(async () => {
  await getHistory()
})
</script>

<style scoped>
.notification-sender {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

:deep(.el-card) {
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}
</style>
