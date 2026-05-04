<template>
  <div class="sign-in-management">
    <el-card class="stats-card">
      <template #header>
        <span>签到统计</span>
      </template>
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value">{{ stats.today_count || 0 }}</div>
            <div class="stat-label">今日签到</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value">{{ stats.yesterday_count || 0 }}</div>
            <div class="stat-label">昨日签到</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total_count || 0 }}</div>
            <div class="stat-label">累计签到</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total_points || 0 }}</div>
            <div class="stat-label">总积分</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>签到记录</span>
        </div>
      </template>
      
      <el-form :inline="true" class="search-form">
        <el-form-item label="用户ID">
          <el-input v-model="searchForm.user_id" placeholder="请输入用户ID" clearable />
        </el-form-item>
        <el-form-item label="签到日期">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="records" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="user_id" label="用户ID" width="100" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="sign_date" label="签到日期" width="150" />
        <el-table-column prop="points_earned" label="获得积分" width="100">
          <template #default="{ row }">
            <el-tag type="success">+{{ row.points_earned }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="continuous_days" label="连续签到天数" width="120" />
        <el-table-column prop="created_at" label="签到时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
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
        @current-change="handlePageChange"
        class="pagination"
      />
    </el-card>

    <el-card class="points-card">
      <template #header>
        <span>积分记录</span>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="用户ID">
          <el-input v-model="pointsSearchForm.user_id" placeholder="请输入用户ID" clearable />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="pointsSearchForm.type" placeholder="全部" clearable>
            <el-option label="签到" :value="1" />
            <el-option label="兑换" :value="2" />
            <el-option label="系统赠送" :value="3" />
            <el-option label="消费" :value="4" />
            <el-option label="其他" :value="5" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handlePointsSearch">搜索</el-button>
          <el-button @click="handlePointsReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="pointsRecords" v-loading="pointsLoading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="user_id" label="用户ID" width="100" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="points" label="积分变动" width="120">
          <template #default="{ row }">
            <el-tag :type="row.points > 0 ? 'success' : 'danger'">
              {{ row.points > 0 ? '+' : '' }}{{ row.points }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="balance" label="变动后余额" width="120" />
        <el-table-column prop="type_name" label="类型" width="100" />
        <el-table-column prop="description" label="描述" min-width="200" />
        <el-table-column prop="created_at" label="时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pointsPagination.page"
        v-model:page-size="pointsPagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        :total="pointsPagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handlePointsSizeChange"
        @current-change="handlePointsPageChange"
        class="pagination"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from '@/utils/axios'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const pointsLoading = ref(false)
const records = ref([])
const pointsRecords = ref([])
const dateRange = ref([])

const stats = ref({
  today_count: 0,
  yesterday_count: 0,
  total_count: 0,
  total_points: 0
})

const searchForm = reactive({
  user_id: '',
  start_date: '',
  end_date: ''
})

const pointsSearchForm = reactive({
  user_id: '',
  type: ''
})

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

const pointsPagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

const loadStats = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/admin/sign-in/stats', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (response.success) {
      stats.value = response.data
    }
  } catch (error) {
    console.error('获取签到统计失败:', error)
  }
}

const loadRecords = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const params = {
      page: pagination.page,
      page_size: pagination.page_size
    }
    
    if (searchForm.user_id) {
      params.user_id = searchForm.user_id
    }
    if (dateRange.value && dateRange.value.length === 2) {
      params.start_date = dateRange.value[0]
      params.end_date = dateRange.value[1]
    }

    const response = await axios.get('/api/v1/admin/sign-in/records', {
      params,
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.success) {
      records.value = response.data.items
      pagination.total = response.data.total
    }
  } catch (error) {
    console.error('获取签到记录失败:', error)
    ElMessage.error('获取签到记录失败')
  } finally {
    loading.value = false
  }
}

const loadPointsRecords = async () => {
  pointsLoading.value = true
  try {
    const token = localStorage.getItem('token')
    const params = {
      page: pointsPagination.page,
      page_size: pointsPagination.page_size
    }
    
    if (pointsSearchForm.user_id) {
      params.user_id = pointsSearchForm.user_id
    }
    if (pointsSearchForm.type) {
      params.type = pointsSearchForm.type
    }

    const response = await axios.get('/api/v1/admin/points/records', {
      params,
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.success) {
      pointsRecords.value = response.data.items
      pointsPagination.total = response.data.total
    }
  } catch (error) {
    console.error('获取积分记录失败:', error)
    ElMessage.error('获取积分记录失败')
  } finally {
    pointsLoading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadRecords()
}

const handleReset = () => {
  searchForm.user_id = ''
  dateRange.value = []
  pagination.page = 1
  loadRecords()
}

const handlePointsSearch = () => {
  pointsPagination.page = 1
  loadPointsRecords()
}

const handlePointsReset = () => {
  pointsSearchForm.user_id = ''
  pointsSearchForm.type = ''
  pointsPagination.page = 1
  loadPointsRecords()
}

const handleSizeChange = () => {
  pagination.page = 1
  loadRecords()
}

const handlePageChange = () => {
  loadRecords()
}

const handlePointsSizeChange = () => {
  pointsPagination.page = 1
  loadPointsRecords()
}

const handlePointsPageChange = () => {
  loadPointsRecords()
}

onMounted(() => {
  loadStats()
  loadRecords()
  loadPointsRecords()
})
</script>

<style scoped>
.sign-in-management {
  padding: 20px;
}

.stats-card {
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #409eff;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}

.table-card, .points-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
