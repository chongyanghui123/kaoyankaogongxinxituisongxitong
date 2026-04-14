<template>
  <div class="home">
    <!-- 顶部导航栏 -->
    <el-header height="60px" class="header">
      <div class="container">
        <div class="logo">
          <h1>双赛道情报通</h1>
        </div>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          @select="handleSelect"
          background-color="#001529"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/kaoyan">考研情报</el-menu-item>
          <el-menu-item index="/kaogong">考公情报</el-menu-item>
          <el-menu-item v-if="!isLoggedIn" index="/login">登录</el-menu-item>
          <el-menu-item v-if="!isLoggedIn" index="/register">注册</el-menu-item>
          <el-dropdown v-else>
            <span class="el-dropdown-link">
              {{ userInfo.username }} <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="navigateTo('/user')">个人中心</el-dropdown-item>
                <el-dropdown-item v-if="userInfo.is_admin" @click="navigateTo('/admin')">管理后台</el-dropdown-item>
                <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-menu>
      </div>
    </el-header>

    <!-- 主要内容 -->
    <el-main class="main">
      <div class="container">
        <!-- 轮播图 -->
        <el-carousel :interval="5000" type="card" height="400px" class="carousel">
          <el-carousel-item v-for="item in carouselItems" :key="item.id">
            <div class="carousel-item">
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
            </div>
          </el-carousel-item>
        </el-carousel>

        <!-- 功能模块 -->
        <div class="features">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-card shadow="hover" class="feature-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Document /></el-icon>
                    <span>考研情报</span>
                  </div>
                </template>
                <div class="feature-content">
                  <p>7×24小时自动抓取考研相关信息，包括招生简章、分数线、复试信息等</p>
                  <el-button type="primary" @click="navigateTo('/kaoyan')">查看详情</el-button>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card shadow="hover" class="feature-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Position /></el-icon>
                    <span>考公情报</span>
                  </div>
                </template>
                <div class="feature-content">
                  <p>7×24小时自动抓取考公相关信息，包括招考公告、职位表、报名信息等</p>
                  <el-button type="primary" @click="navigateTo('/kaogong')">查看详情</el-button>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card shadow="hover" class="feature-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Bell /></el-icon>
                    <span>精准推送</span>
                  </div>
                </template>
                <div class="feature-content">
                  <p>根据用户设置的关键词和兴趣，智能推送相关信息，让您第一时间获取重要资讯</p>
                  <el-button type="primary" @click="navigateTo('/user')">设置推送</el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>

        <!-- 最新情报 -->
        <div class="latest-info">
          <h2 class="section-title">最新情报</h2>
          <el-row :gutter="20">
            <el-col :span="12">
              <h3>考研最新情报</h3>
              <el-list>
                <el-list-item v-for="item in kaoyanLatest" :key="item.id">
                  <template #title>
                    <a :href="'#/kaoyan/' + item.id">{{ item.title }}</a>
                  </template>
                  <template #extra>
                    <span class="time">{{ formatDate(item.publish_date) }}</span>
                  </template>
                </el-list-item>
              </el-list>
            </el-col>
            <el-col :span="12">
              <h3>考公最新情报</h3>
              <el-list>
                <el-list-item v-for="item in kaogongLatest" :key="item.id">
                  <template #title>
                    <a :href="'#/kaogong/' + item.id">{{ item.title }}</a>
                  </template>
                  <template #extra>
                    <span class="time">{{ formatDate(item.publish_date) }}</span>
                  </template>
                </el-list-item>
              </el-list>
            </el-col>
          </el-row>
        </div>
      </div>
    </el-main>

    <!-- 底部 -->
    <el-footer height="120px" class="footer">
      <div class="container">
        <p>© 2026 双赛道情报通 版权所有</p>
        <p>7×24小时自动抓取、分类、推送考研+考公官方关键信息的情报平台</p>
      </div>
    </el-footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Document, Position, Bell, ArrowDown } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const activeIndex = ref('/')
const isLoggedIn = ref(false)
const userInfo = ref({})
const carouselItems = ref([
  { id: 1, title: '考研情报监控', description: '实时监控考研相关信息，第一时间获取重要资讯' },
  { id: 2, title: '考公情报监控', description: '实时监控考公相关信息，不错过任何招考机会' },
  { id: 3, title: '智能精准推送', description: '根据您的兴趣和需求，智能推送相关信息' }
])
const kaoyanLatest = ref([])
const kaogongLatest = ref([])

// 处理菜单选择
const handleSelect = (key) => {
  navigateTo(key)
}

// 导航到指定路径
const navigateTo = (path) => {
  router.push(path)
}

// 退出登录
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('userInfo')
  isLoggedIn.value = false
  userInfo.value = {}
  router.push('/')
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

// 获取最新情报
const getLatestInfo = async () => {
  try {
    // 模拟数据，实际应该调用API
    kaoyanLatest.value = [
      { id: 1, title: '2026年全国硕士研究生招生考试公告', publish_date: '2026-09-24' },
      { id: 2, title: '2026年考研国家线公布', publish_date: '2026-03-15' },
      { id: 3, title: '2026年考研复试调剂指南', publish_date: '2026-03-20' }
    ]
    kaogongLatest.value = [
      { id: 1, title: '2026年国家公务员招考公告', publish_date: '2026-10-14' },
      { id: 2, title: '2026年国考职位表发布', publish_date: '2026-10-15' },
      { id: 3, title: '2026年国考报名指南', publish_date: '2026-10-16' }
    ]
  } catch (error) {
    console.error('获取最新情报失败:', error)
  }
}

// 检查登录状态
const checkLoginStatus = () => {
  const token = localStorage.getItem('token')
  const userInfoStr = localStorage.getItem('userInfo')
  if (token && userInfoStr) {
    isLoggedIn.value = true
    userInfo.value = JSON.parse(userInfoStr)
  }
}

onMounted(() => {
  checkLoginStatus()
  getLatestInfo()
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #001529;
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo h1 {
  color: #fff;
  margin: 0;
  font-size: 24px;
  line-height: 60px;
}

.header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.main {
  flex: 1;
  padding: 40px 0;
}

.carousel {
  margin-bottom: 40px;
}

.carousel-item {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
}

.carousel-item h3 {
  font-size: 24px;
  margin-bottom: 20px;
}

.carousel-item p {
  font-size: 16px;
  color: #666;
}

.features {
  margin-bottom: 40px;
}

.feature-card {
  height: 200px;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.card-header el-icon {
  margin-right: 8px;
}

.feature-content {
  height: calc(100% - 40px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.feature-content p {
  margin-bottom: 20px;
  color: #666;
}

.latest-info {
  margin-bottom: 40px;
}

.section-title {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
}

.latest-info h3 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #333;
}

.time {
  color: #999;
  font-size: 14px;
}

.footer {
  background-color: #f0f2f5;
  padding: 30px 0;
  text-align: center;
  color: #666;
}

.footer p {
  margin: 5px 0;
}
</style>
