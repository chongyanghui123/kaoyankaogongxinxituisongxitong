<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">用户网站管理</h3>
        </div>
      </template>
      
      <!-- 分类筛选 -->
      <div class="search-filter">
        <el-form :inline="true" :model="filterForm" class="demo-form-inline">
          <el-form-item label="用户类型">
            <el-select v-model="filterForm.user_type" placeholder="选择用户类型" style="width: 150px;">
              <el-option label="全部" value="" />
              <el-option label="考研" value="考研" />
              <el-option label="考公" value="考公" />
              <el-option label="双赛道" value="双赛道" />
              <el-option label="未订阅" value="未订阅" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleFilter">筛选</el-button>
            <el-button @click="resetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 按学生分类 -->
      <div class="student-classification">
        <h4>按学生分类</h4>
        <el-table :data="filteredStudentWebsites" style="width: 100%">
          <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="email" label="邮箱" />
          <el-table-column prop="user_type" label="用户类型" width="100" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status ? 'success' : 'danger'">
                {{ scope.row.status ? '活跃' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="websites" label="网站地址" min-width="300">
            <template #default="scope">
              <div v-if="scope.row.websites && scope.row.websites.length > 0">
                <el-button type="primary" size="small" @click="showWebsiteDetails(scope.row.websites)">查看全部</el-button>
              </div>
              <span v-else class="no-websites">无网站地址</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
    
    <!-- 网站详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="网站地址详情"
      width="800px"
    >
      <div v-if="selectedWebsites && selectedWebsites.length > 0">
        <el-table :data="selectedWebsites" style="width: 100%">
          <el-table-column prop="name" label="名称" width="200" />
          <el-table-column prop="url" label="网址">
            <template #default="scope">
              <a :href="scope.row.url" target="_blank">{{ scope.row.url }}</a>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else class="no-websites">无网站地址</div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 用户网站管理相关
const studentWebsites = ref([])
const filteredStudentWebsites = ref([])
const dialogVisible = ref(false)
const selectedWebsites = ref([])
const filterForm = ref({
  user_type: ''
})

// 获取学生网站列表
const getStudentWebsites = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/admin/student-websites', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    studentWebsites.value = response.data
    filteredStudentWebsites.value = response.data
  } catch (error) {
    console.error('获取学生网站列表失败:', error)
  }
}

// 筛选学生网站
const handleFilter = () => {
  let filtered = studentWebsites.value
  
  // 按用户类型筛选
  if (filterForm.value.user_type) {
    filtered = filtered.filter(item => item.user_type === filterForm.value.user_type)
  }
  
  filteredStudentWebsites.value = filtered
}

// 重置筛选
const resetFilter = () => {
  filterForm.value = {
    user_type: ''
  }
  filteredStudentWebsites.value = studentWebsites.value
}

// 显示网站详情
const showWebsiteDetails = (websites) => {
  selectedWebsites.value = websites
  dialogVisible.value = true
}

onMounted(() => {
  getStudentWebsites()
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

.student-classification {
  margin-top: 20px;
}

.student-classification h4 {
  margin-bottom: 10px;
  font-size: 16px;
  font-weight: 500;
}

.website-item {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.website-name {
  display: block;
  font-weight: 500;
  margin-bottom: 5px;
}

.website-url {
  font-size: 12px;
  color: #409eff;
  word-break: break-all;
}

.no-websites {
  color: #909399;
}
</style>