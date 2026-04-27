<template>
  <div class="exam-countdown">
    <div class="countdown-card" v-for="schedule in activeSchedules" :key="schedule.id">
      <div class="card-header">
        <h3>{{ schedule.name }}</h3>
        <el-tag :type="schedule.exam_type === 1 ? 'success' : 'primary'">
          {{ schedule.exam_type === 1 ? '考研' : '考公' }}
        </el-tag>
      </div>
      
      <div class="countdown-content" v-if="schedule.countdown">
        <div class="countdown-timer">
          <div class="time-item">
            <span class="time-value">{{ schedule.countdown.days }}</span>
            <span class="time-label">天</span>
          </div>
          <div class="time-item">
            <span class="time-value">{{ schedule.countdown.hours }}</span>
            <span class="time-label">时</span>
          </div>
          <div class="time-item">
            <span class="time-value">{{ schedule.countdown.minutes }}</span>
            <span class="time-label">分</span>
          </div>
          <div class="time-item">
            <span class="time-value">{{ schedule.countdown.seconds }}</span>
            <span class="time-label">秒</span>
          </div>
        </div>
        
        <div class="exam-info">
          <p class="exam-date">
            <el-icon><Calendar /></el-icon>
            {{ formatDate(schedule.exam_date) }}
          </p>
          <p class="exam-description" v-if="schedule.description">
            {{ schedule.description }}
          </p>
        </div>
      </div>
      
      <div class="countdown-content" v-else>
        <div class="exam-completed">
          <el-icon class="completed-icon"><Check /></el-icon>
          <p>考试已结束</p>
        </div>
        <p class="exam-date">{{ formatDate(schedule.exam_date) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Calendar, Check } from '@element-plus/icons-vue'
import axios from '@/utils/axios'

const activeSchedules = ref([])
let timer = null

// 格式化日期
const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    weekday: 'short'
  })
}

// 获取考试日程
const getExamSchedules = async () => {
  try {
    const response = await axios.get('/api/v1/learning_materials/exam-schedules/active')
    if (response.data.success) {
      activeSchedules.value = response.data.data
    }
  } catch (error) {
    console.error('获取考试日程失败:', error)
  }
}

// 计算倒计时
const calculateCountdown = () => {
  const now = new Date()
  activeSchedules.value.forEach(schedule => {
    const examDate = new Date(schedule.exam_date)
    if (examDate > now) {
      const delta = examDate - now
      const days = Math.floor(delta / (1000 * 60 * 60 * 24))
      const hours = Math.floor((delta % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      const minutes = Math.floor((delta % (1000 * 60 * 60)) / (1000 * 60))
      const seconds = Math.floor((delta % (1000 * 60)) / 1000)
      
      schedule.countdown = { days, hours, minutes, seconds }
    } else {
      schedule.countdown = null
    }
  })
}

// 启动定时器
const startTimer = () => {
  calculateCountdown()
  timer = setInterval(() => {
    calculateCountdown()
  }, 1000)
}

// 停止定时器
const stopTimer = () => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

onMounted(() => {
  getExamSchedules()
  startTimer()
})

onUnmounted(() => {
  stopTimer()
})
</script>

<style scoped>
.exam-countdown {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.countdown-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: all 0.3s ease;
}

.countdown-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.countdown-timer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.time-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.time-value {
  font-size: 32px;
  font-weight: 700;
  color: #409eff;
  line-height: 1;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.time-label {
  font-size: 14px;
  color: #999;
  margin-top: 5px;
}

.exam-info {
  text-align: center;
}

.exam-date {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}

.exam-date el-icon {
  margin-right: 5px;
}

.exam-description {
  color: #999;
  font-size: 13px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.exam-completed {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: #67c23a;
}

.completed-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.exam-completed p {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .exam-countdown {
    grid-template-columns: 1fr;
  }
  
  .countdown-card {
    padding: 15px;
  }
  
  .time-value {
    font-size: 24px;
  }
  
  .time-label {
    font-size: 12px;
  }
  
  .countdown-timer {
    gap: 10px;
  }
}
</style>
