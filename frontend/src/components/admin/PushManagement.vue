<template>
  <div class="push-management">
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon total-icon">
            <el-icon><DataAnalysis /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ stats.total_push || 0 }}</div>
            <div class="stat-label">总推送数</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon success-icon">
            <el-icon><Check /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ stats.success_push || 0 }}</div>
            <div class="stat-label">成功推送</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon failed-icon">
            <el-icon><Close /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ stats.failed_push || 0 }}</div>
            <div class="stat-label">失败推送</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon rate-icon">
            <el-icon><TrendCharts /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ stats.success_rate ? stats.success_rate.toFixed(2) + '%' : '0.00%' }}</div>
            <div class="stat-label">成功率</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 推送统计图表 -->
    <div class="chart-grid">
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <h3>推送类型分布</h3>
            <el-button link size="small" @click="refreshData">刷新</el-button>
          </div>
        </template>
        <div class="chart-container">
          <div ref="categoryChart" style="width: 100%; height: 300px;"></div>
        </div>
      </el-card>

      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <h3>推送渠道分布</h3>
            <el-button link size="small" @click="refreshData">刷新</el-button>
          </div>
        </template>
        <div class="chart-container">
          <div ref="channelChart" style="width: 100%; height: 300px;"></div>
        </div>
      </el-card>
    </div>

    <!-- 推送操作 -->
    <el-card class="operation-card">
      <template #header>
        <div class="card-header">
          <h3>推送操作</h3>
        </div>
      </template>

      <!-- 手动触发推送 -->
      <div class="mb-8">
        <h4 class="section-title">手动触发推送</h4>
        <div class="operation-grid">
          <el-button 
            type="primary" 
            @click="triggerPush('kaoyan')"
            class="operation-button primary-button"
          >
            <el-icon class="mr-2"><Document /></el-icon>
            触发考研情报推送
          </el-button>
          <el-button 
            type="success" 
            @click="triggerPush('kaogong')"
            class="operation-button success-button"
          >
            <el-icon class="mr-2"><Paperclip /></el-icon>
            触发考公情报推送
          </el-button>
          <el-button 
            type="warning" 
            @click="triggerPush('expiry')"
            class="operation-button warning-button"
          >
            <el-icon class="mr-2"><AlarmClock /></el-icon>
            触发到期提醒推送
          </el-button>
        </div>
      </div>

      <!-- 自动推送设置 -->
      <div>
        <h4 class="section-title">自动推送设置</h4>
        <el-form :inline="true" class="schedule-form">
          <el-form-item label="推送频率">
            <el-select v-model="pushFrequency" placeholder="选择推送频率" style="width: 200px">
              <el-option value="hourly" label="每小时"></el-option>
              <el-option value="daily" label="每天"></el-option>
              <el-option value="weekly" label="每周"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="推送时间">
            <el-time-picker v-model="pushTime" placeholder="选择推送时间" style="width: 200px"></el-time-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="savePushSettings">
              <el-icon class="mr-2"><Check /></el-icon>
              保存设置
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>

    <!-- 推送历史记录 -->
    <el-card class="history-card">
      <template #header>
        <div class="card-header">
          <h3>推送历史记录</h3>
        </div>
      </template>

      <!-- 筛选条件 -->
      <el-form :inline="true" class="filter-form mb-4">
        <el-form-item label="推送分类">
          <el-select v-model="filter.category" placeholder="所有分类" style="width: 120px" @change="fetchPushHistory">
            <el-option value="" label="所有分类"></el-option>
            <el-option value="1" label="考研"></el-option>
            <el-option value="2" label="考公"></el-option>
            <el-option value="3" label="系统通知"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="推送渠道">
          <el-select v-model="filter.push_type" placeholder="所有渠道" style="width: 120px" @change="fetchPushHistory">
            <el-option value="" label="所有渠道"></el-option>
            <el-option value="1" label="微信"></el-option>
            <el-option value="2" label="企业微信"></el-option>
            <el-option value="3" label="邮件"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="推送状态">
          <el-select v-model="filter.push_status" placeholder="所有状态" style="width: 120px" @change="fetchPushHistory">
            <el-option value="" label="所有状态"></el-option>
            <el-option value="1" label="成功"></el-option>
            <el-option value="0" label="失败"></el-option>
          </el-select>
        </el-form-item>
      </el-form>

      <!-- 历史记录表格 -->
      <el-table :data="pushHistory.items" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column label="用户" width="150">
          <template #default="scope">
            <div class="user-info">
              <div class="user-avatar">
                {{ scope.row.user_info?.username?.charAt(0) || '?' }}
              </div>
              <span>{{ scope.row.user_info?.username || '未知' }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="category_text" label="分类" width="100"></el-table-column>
        <el-table-column prop="push_type_text" label="渠道" width="120"></el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.push_status == 1 ? 'success' : 'danger'">
              {{ scope.row.push_status_text }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="push_content" label="内容">
          <template #default="scope">
            <span :title="scope.row.push_content" class="content-truncate">
              {{ scope.row.push_content }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="push_time" label="推送时间" width="180">
          <template #default="scope">
            {{ formatTime(scope.row.push_time) }}
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="filter.page"
          v-model:page-size="filter.page_size"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pushHistory.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { DataAnalysis, Check, Close, TrendCharts, Document, Paperclip, AlarmClock, Message as MessageIcon, Refresh } from '@element-plus/icons-vue'
import { ElMessage, ElLoading } from 'element-plus'
import * as echarts from 'echarts'

const stats = ref({})
const pushHistory = ref({
  total: 0,
  items: []
})
const filter = ref({
  page: 1,
  page_size: 20,
  category: '',
  push_type: '',
  push_status: ''
})
const pushFrequency = ref('daily')
const pushTime = ref(new Date())
const categoryChart = ref(null)
const channelChart = ref(null)
const loading = ref(false)

async function fetchStats() {
  try {
    const response = await fetch('/api/v1/push/stats', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const data = await response.json()
    if (data.success) {
      stats.value = data.data
      initCharts()
      updateCharts()
    }
  } catch (error) {
    console.error('获取推送统计失败:', error)
    ElMessage.error('获取推送统计失败')
  }
}

async function fetchPushSettings() {
  try {
    const response = await fetch('/api/v1/push/settings', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const data = await response.json()
    if (data.success) {
      pushFrequency.value = data.data.frequency
      // 解析时间字符串为 Date 对象
      if (data.data.time) {
        const timeParts = data.data.time.split(':')
        const now = new Date()
        now.setHours(parseInt(timeParts[0]), parseInt(timeParts[1]), 0, 0)
        pushTime.value = now
      }
    }
  } catch (error) {
    console.error('获取推送设置失败:', error)
  }
}

async function fetchPushHistory() {
  try {
    loading.value = true
    const queryParams = new URLSearchParams()
    queryParams.append('page', filter.value.page)
    queryParams.append('page_size', filter.value.page_size)
    if (filter.value.category) {
      queryParams.append('category', filter.value.category)
    }
    if (filter.value.push_type) {
      queryParams.append('push_type', filter.value.push_type)
    }
    if (filter.value.push_status) {
      queryParams.append('push_status', filter.value.push_status)
    }

    const response = await fetch(`/api/v1/push/history?${queryParams.toString()}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const data = await response.json()
    if (data.success) {
      pushHistory.value = data.data
    }
  } catch (error) {
    console.error('获取推送历史失败:', error)
    ElMessage.error('获取推送历史失败')
  } finally {
    loading.value = false
  }
}

async function triggerPush(type) {
  try {
    const loading = ElLoading.service({ fullscreen: true, text: '推送中...' })
    const response = await fetch(`/api/v1/push/trigger/${type}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    const data = await response.json()
    if (data.success) {
      ElMessage.success(data.message || '推送任务已触发')
      fetchStats()
      fetchPushHistory()
    } else {
      ElMessage.error('触发推送失败: ' + (data.message || '未知错误'))
    }
  } catch (error) {
    console.error('触发推送失败:', error)
    ElMessage.error('触发推送失败: 网络错误')
  } finally {
    ElLoading.service().close()
  }
}

async function savePushSettings() {
  try {
    const loading = ElLoading.service({ fullscreen: true, text: '保存设置中...' })
    const response = await fetch('/api/v1/push/settings', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        frequency: pushFrequency.value,
        time: pushTime.value
      })
    })
    const data = await response.json()
    if (data.success) {
      ElMessage.success('推送设置保存成功')
    } else {
      ElMessage.error('保存设置失败: ' + (data.message || '未知错误'))
    }
  } catch (error) {
    console.error('保存推送设置失败:', error)
    ElMessage.error('保存推送设置失败: 网络错误')
  } finally {
    ElLoading.service().close()
  }
}

function handleSizeChange(val) {
  filter.value.page_size = val
  fetchPushHistory()
}

function handleCurrentChange(val) {
  filter.value.page = val
  fetchPushHistory()
}

function refreshData() {
  fetchStats()
  fetchPushHistory()
}

function formatTime(timeStr) {
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN')
}

function initCharts() {
  // 初始化分类图表
  if (categoryChart.value && !categoryChart.value.chart) {
    categoryChart.value.chart = echarts.init(categoryChart.value)
  }
  
  // 初始化渠道图表
  if (channelChart.value && !channelChart.value.chart) {
    channelChart.value.chart = echarts.init(channelChart.value)
  }
}

function updateCharts() {
  // 更新分类图表
  if (categoryChart.value?.chart && stats.value.category_stats) {
    const categoryOption = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        top: 'middle'
      },
      series: [
        {
          name: '推送类型',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            formatter: '{b}: {c} ({d}%)'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '16',
              fontWeight: 'bold'
            }
          },
          data: stats.value.category_stats.map(item => ({
            value: item.count,
            name: item.category_text
          }))
        }
      ]
    }
    categoryChart.value.chart.setOption(categoryOption)
  }

  // 更新渠道图表
  if (channelChart.value?.chart && stats.value.channel_stats) {
    const channelOption = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: stats.value.channel_stats.map(item => item.push_type_text),
        axisTick: {
          alignWithLabel: true
        }
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '推送数量',
          type: 'bar',
          barWidth: '60%',
          data: stats.value.channel_stats.map(item => item.count),
          itemStyle: {
            color: '#6366f1'
          }
        }
      ]
    }
    channelChart.value.chart.setOption(channelOption)
  }
}

onMounted(() => {
  fetchStats()
  fetchPushHistory()
  fetchPushSettings()
})

onBeforeUnmount(() => {
  if (categoryChart.value?.chart) {
    categoryChart.value.chart.dispose()
  }
  if (channelChart.value?.chart) {
    channelChart.value.chart.dispose()
  }
})
</script>

<style scoped>
.push-management {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  height: 100%;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
}

.total-icon {
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
}

.success-icon {
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
}

.failed-icon {
  background: linear-gradient(135deg, #ff4d4f 0%, #cf1322 100%);
}

.rate-icon {
  background: linear-gradient(135deg, #722ed1 0%, #531dab 100%);
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.operation-card {
  margin-bottom: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}

.operation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.operation-button {
  padding: 16px;
  font-size: 14px;
  font-weight: 500;
}

.test-form {
  margin-top: 16px;
}

.history-card {
  margin-bottom: 20px;
}

.filter-form {
  margin-bottom: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
}

.content-truncate {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .push-management {
    padding: 16px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-grid {
    grid-template-columns: 1fr;
  }
  
  .operation-grid {
    grid-template-columns: 1fr;
  }
  
  .test-form {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .test-form .el-form-item {
    margin-bottom: 12px;
  }
  
  .filter-form {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-form .el-form-item {
    margin-bottom: 12px;
  }
  
  .pagination-container {
    justify-content: center;
  }
}
</style>
