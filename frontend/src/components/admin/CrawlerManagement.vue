<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">爬虫管理</h3>
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
        <el-table :data="filteredStudentCrawlers" style="width: 100%">
          <el-table-column prop="user_id" label="用户ID" width="80" />
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
          <el-table-column prop="crawlers" label="爬虫网址" min-width="300">
            <template #default="scope">
              <div v-if="scope.row.crawlers && scope.row.crawlers.length > 0">
                <el-button type="primary" size="small" @click="showCrawlerDetails(scope.row.crawlers)">查看全部</el-button>
              </div>
              <span v-else class="no-crawlers">无爬虫网址</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
    
    <!-- 爬虫详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="爬虫网址详情"
      width="800px"
    >
      <div v-if="selectedCrawlers && selectedCrawlers.length > 0">
        <el-table :data="selectedCrawlers" style="width: 100%">
          <el-table-column prop="name" label="名称" width="200" />
          <el-table-column prop="url" label="网址">
            <template #default="scope">
              <a :href="scope.row.url" target="_blank">{{ scope.row.url }}</a>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else class="no-crawlers">无爬虫网址</div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 爬虫管理相关
const studentCrawlers = ref([])
const filteredStudentCrawlers = ref([])
const dialogVisible = ref(false)
const selectedCrawlers = ref([])
const filterForm = ref({
  user_type: ''
})

// 获取学生爬虫列表
const getStudentCrawlers = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/admin/student-crawlers', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    studentCrawlers.value = response.data
    filteredStudentCrawlers.value = response.data
  } catch (error) {
    console.error('获取学生爬虫列表失败:', error)
  }
}

// 筛选学生爬虫
const handleFilter = () => {
  let filtered = studentCrawlers.value
  
  // 按用户类型筛选
  if (filterForm.value.user_type) {
    filtered = filtered.filter(item => item.user_type === filterForm.value.user_type)
  }
  
  filteredStudentCrawlers.value = filtered
}

// 重置筛选
const resetFilter = () => {
  filterForm.value = {
    user_type: ''
  }
  filteredStudentCrawlers.value = studentCrawlers.value
}

// 显示爬虫详情
const showCrawlerDetails = (crawlers) => {
  selectedCrawlers.value = crawlers
  dialogVisible.value = true
}

onMounted(() => {
  getStudentCrawlers()
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

.crawler-item {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.crawler-name {
  display: block;
  font-weight: 500;
  margin-bottom: 5px;
}

.crawler-url {
  font-size: 12px;
  color: #409eff;
  word-break: break-all;
}

.no-crawlers {
  color: #909399;
}
</style>