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

    <!-- 图表区域 -->
    <div class="charts-row">
      <!-- 用户增长趋势图 -->
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <h3>📈 用户增长趋势（近7天）</h3>
            <el-button link size="small" @click="refreshData">刷新</el-button>
          </div>
        </template>
        <div ref="userGrowthChart" style="width: 100%; height: 280px;"></div>
      </el-card>

      <!-- VIP用户分布 -->
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <h3>👑 VIP用户分布</h3>
          </div>
        </template>
        <div ref="vipChart" style="width: 100%; height: 280px;"></div>
      </el-card>
    </div>

    <div class="charts-row">
      <!-- 积分分布图 -->
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <h3>💎 积分分布</h3>
          </div>
        </template>
        <div ref="pointsChart" style="width: 100%; height: 280px;"></div>
      </el-card>

      <!-- 用户类型分布 -->
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <h3>👥 用户类型分布</h3>
          </div>
        </template>
        <div ref="userTypeChart" style="width: 100%; height: 280px;"></div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { User, Document, Paperclip, ShoppingCart, Message } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from '@/utils/axios'
import * as echarts from 'echarts'

const stats = ref({
  user_count: 0,
  kaoyan_count: 0,
  kaogong_count: 0,
  order_count: 0,
  push_count: 0,
  timestamp: '',
  user_type_distribution: { "考研": 0, "考公": 0, "双赛道": 0 },
  points_distribution: { "0分": 0, "1-50分": 0, "51-100分": 0, "101-200分": 0, "201-500分": 0, "500分以上": 0 },
  vip_distribution: { "普通用户": 0, "考研VIP": 0, "考公VIP": 0, "双赛道VIP": 0 },
  user_growth_trend: []
})

const userGrowthChart = ref(null)
const vipChart = ref(null)
const pointsChart = ref(null)
const userTypeChart = ref(null)

let userGrowthChartInstance = null
let vipChartInstance = null
let pointsChartInstance = null
let userTypeChartInstance = null

const loading = ref(false)

const initUserGrowthChart = () => {
  if (!userGrowthChart.value) return
  userGrowthChartInstance = echarts.init(userGrowthChart.value)
  const option = {
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', boundaryGap: false, data: [] },
    yAxis: { type: 'value' },
    series: [{
      name: '新增用户',
      type: 'line',
      smooth: true,
      areaStyle: { color: 'rgba(24, 144, 255, 0.2)' },
      lineStyle: { color: '#1890ff', width: 2 },
      itemStyle: { color: '#1890ff' },
      data: []
    }]
  }
  userGrowthChartInstance.setOption(option)
}

const initVipChart = () => {
  if (!vipChart.value) return
  vipChartInstance = echarts.init(vipChart.value)
  const option = {
    tooltip: { trigger: 'item', formatter: '{b}: {c}人 ({d}%)' },
    legend: { orient: 'vertical', left: 'left', top: 'middle' },
    series: [{
      name: 'VIP分布',
      type: 'pie',
      radius: ['35%', '65%'],
      center: ['60%', '50%'],
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: true, formatter: '{b}\n{c}人' },
      data: []
    }]
  }
  vipChartInstance.setOption(option)
}

const initPointsChart = () => {
  if (!pointsChart.value) return
  pointsChartInstance = echarts.init(pointsChart.value)
  const option = {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: [] },
    yAxis: { type: 'value' },
    series: [{
      name: '用户数',
      type: 'bar',
      barWidth: '50%',
      itemStyle: {
        borderRadius: [4, 4, 0, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#36cfc9' },
          { offset: 1, color: '#13c2c2' }
        ])
      },
      data: []
    }]
  }
  pointsChartInstance.setOption(option)
}

const initUserTypeChart = () => {
  if (!userTypeChart.value) return
  userTypeChartInstance = echarts.init(userTypeChart.value)
  const option = {
    tooltip: { trigger: 'item', formatter: '{b}: {c}人 ({d}%)' },
    legend: { orient: 'vertical', left: 'left', top: 'middle' },
    series: [{
      name: '用户类型',
      type: 'pie',
      radius: ['35%', '65%'],
      center: ['60%', '50%'],
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: true, formatter: '{b}\n{c}人' },
      data: []
    }]
  }
  userTypeChartInstance.setOption(option)
}

const updateCharts = () => {
  // 用户增长趋势
  if (userGrowthChartInstance && stats.value.user_growth_trend) {
    const dates = stats.value.user_growth_trend.map(item => item.date)
    const counts = stats.value.user_growth_trend.map(item => item.count)
    userGrowthChartInstance.setOption({
      xAxis: { data: dates },
      series: [{ data: counts }]
    })
  }

  // VIP分布
  if (vipChartInstance && stats.value.vip_distribution) {
    const data = Object.entries(stats.value.vip_distribution).map(([name, value]) => ({ name, value }))
    vipChartInstance.setOption({ series: [{ data }] })
  }

  // 积分分布
  if (pointsChartInstance && stats.value.points_distribution) {
    const categories = Object.keys(stats.value.points_distribution)
    const values = Object.values(stats.value.points_distribution)
    pointsChartInstance.setOption({
      xAxis: { data: categories },
      series: [{ data: values }]
    })
  }

  // 用户类型分布
  if (userTypeChartInstance && stats.value.user_type_distribution) {
    const data = Object.entries(stats.value.user_type_distribution).map(([name, value]) => ({ name, value }))
    userTypeChartInstance.setOption({ series: [{ data }] })
  }
}

const destroyCharts = () => {
  userGrowthChartInstance?.dispose()
  vipChartInstance?.dispose()
  pointsChartInstance?.dispose()
  userTypeChartInstance?.dispose()
}

const fetchStats = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/v1/admin/stats', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    
    stats.value = response
    updateCharts()
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  fetchStats()
}

const handleResize = () => {
  userGrowthChartInstance?.resize()
  vipChartInstance?.resize()
  pointsChartInstance?.resize()
  userTypeChartInstance?.resize()
}

onMounted(async () => {
  await fetchStats()
  setTimeout(() => {
    initUserGrowthChart()
    initVipChart()
    initPointsChart()
    initUserTypeChart()
    updateCharts()
  }, 100)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  destroyCharts()
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.system-overview {
  padding: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
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
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  color: white;
}

.user-icon { background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%); }
.kaoyan-icon { background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%); }
.kaogong-icon { background: linear-gradient(135deg, #fa8c16 0%, #d46b08 100%); }
.order-icon { background: linear-gradient(135deg, #722ed1 0%, #531dab 100%); }
.push-icon { background: linear-gradient(135deg, #eb2f96 0%, #c41d7f 100%); }

.stat-info { flex: 1; }
.stat-number { font-size: 24px; font-weight: bold; color: #303133; margin-bottom: 4px; }
.stat-label { font-size: 14px; color: #606266; }

.charts-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

@media (max-width: 1200px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
}
</style>
