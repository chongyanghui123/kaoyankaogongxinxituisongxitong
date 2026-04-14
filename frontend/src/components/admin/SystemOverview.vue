<template>
  <div class="system-overview">
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon user-icon">
            <el-icon><User /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ stats.user_count }}</div>
            <div class="stat-label">用户总数</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon kaoyan-icon">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ stats.kaoyan_count }}</div>
            <div class="stat-label">考研情报</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon kaogong-icon">
            <el-icon><Paperclip /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ stats.kaogong_count }}</div>
            <div class="stat-label">考公情报</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon order-icon">
            <el-icon><ShoppingCart /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ stats.order_count }}</div>
            <div class="stat-label">订单总数</div>
          </div>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon push-icon">
            <el-icon><Message /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-number">{{ stats.push_count }}</div>
            <div class="stat-label">推送总数</div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 用户类型分布 -->
    <el-card class="user-type-card">
      <template #header>
        <div class="card-header">
          <h3>用户类型分布</h3>
          <el-button type="text" size="small" @click="refreshData">刷新</el-button>
        </div>
      </template>
      
      <div class="chart-container">
        <div ref="userTypeChart" style="width: 100%; height: 300px;"></div>
      </div>
    </el-card>


  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { User, Document, Paperclip, ShoppingCart, Message, DataAnalysis } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import * as echarts from 'echarts'

const stats = ref({
  user_count: 0,
  kaoyan_count: 0,
  kaogong_count: 0,
  order_count: 0,
  push_count: 0,
  timestamp: '',
  user_type_distribution: {
    "未订阅": 0,
    "考研": 0,
    "考公": 0,
    "双赛道": 0
  }
})

const userTypeChart = ref(null)
let chartInstance = null

const loading = ref(false)

// 初始化图表
const initChart = () => {
  if (!userTypeChart.value) return
  
  chartInstance = echarts.init(userTypeChart.value)
  
  const option = {
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
        name: '用户类型分布',
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
          formatter: '{b}: {c}人 ({d}%)'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold'
          }
        },
        data: []
      }
    ]
  }
  
  chartInstance.setOption(option)
  
  // 响应式调整
  const handleResize = () => {
    if (chartInstance) {
      chartInstance.resize()
    }
  }
  window.addEventListener('resize', handleResize)
  
  return () => {
    window.removeEventListener('resize', handleResize)
  }
}

// 更新图表数据
const updateChart = () => {
  if (!chartInstance || !stats.value.user_type_distribution) return
  
  const data = [
    { value: stats.value.user_type_distribution["未订阅"] || 0, name: "未订阅" },
    { value: stats.value.user_type_distribution["考研"] || 0, name: "考研" },
    { value: stats.value.user_type_distribution["考公"] || 0, name: "考公" },
    { value: stats.value.user_type_distribution["双赛道"] || 0, name: "双赛道" }
  ]
  
  const option = chartInstance.getOption()
  option.series[0].data = data
  chartInstance.setOption(option)
}

// 清理图表
const destroyChart = () => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
}

const fetchStats = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/v1/admin/stats', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    if (response.data.success) {
      stats.value = response.data.data
    } else {
      stats.value = response.data
    }
    
    // 更新图表数据
    if (stats.value.user_type_distribution) {
      updateChart()
    }
    

  } catch (error) {
    console.error('获取统计数据失败:', error)
    // 显示错误信息
    ElMessage.error('获取统计数据失败，请检查网络连接')
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  fetchStats()
}

onMounted(async () => {
  // 等待 DOM 渲染完成
  await fetchStats()
  
  // 初始化图表
  setTimeout(() => {
    initChart()
    updateChart()
  }, 100)
})

onUnmounted(() => {
  destroyChart()
})
</script>

<style scoped>
.system-overview {
  padding: 20px;
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

.user-icon {
  background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
}

.kaoyan-icon {
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
}

.kaogong-icon {
  background: linear-gradient(135deg, #fa8c16 0%, #d46b08 100%);
}

.order-icon {
  background: linear-gradient(135deg, #722ed1 0%, #531dab 100%);
}

.push-icon {
  background: linear-gradient(135deg, #eb2f96 0%, #c41d7f 100%);
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

.chart-placeholder {
  text-align: center;
  color: #909399;
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.user-type-card {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
