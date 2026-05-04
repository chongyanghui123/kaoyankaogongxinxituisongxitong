<template>
  <div class="kaoyan">
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
        <!-- 搜索和筛选 -->
        <div class="search-filter">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-input
                v-model="searchKeyword"
                placeholder="搜索考研情报"
                clearable
                prefix-icon="Search"
                @keyup.enter="searchInfo"
              >
                <template #append>
                  <el-button type="primary" @click="searchInfo">搜索</el-button>
                </template>
              </el-input>
            </el-col>
            <el-col :span="12">
              <el-row :gutter="10">
                <el-col :span="8">
                  <el-select v-model="filterProvince" placeholder="选择省份" clearable>
                    <el-option v-for="province in provinces" :key="province" :label="province" :value="province" />
                  </el-select>
                </el-col>
                <el-col :span="8">
                  <el-select v-model="filterCategory" placeholder="选择分类" clearable>
                    <el-option v-for="category in categories" :key="category" :label="category" :value="category" />
                  </el-select>
                </el-col>
                <el-col :span="8">
                  <el-select v-model="sortBy" placeholder="排序方式">
                    <el-option label="发布时间" value="publish_date" />
                    <el-option label="阅读量" value="read_count" />
                    <el-option label="点赞量" value="like_count" />
                  </el-select>
                </el-col>
              </el-row>
            </el-col>
          </el-row>
        </div>

        <!-- 情报列表 -->
        <div class="info-list">
          <el-skeleton v-if="loading" :rows="10" animated />
          <el-card v-else v-for="item in kaoyanInfoList" :key="item.id" class="info-card">
            <template #header>
              <div class="card-header">
                <h3 class="title">{{ item.title }}</h3>
                <span class="category">{{ item.category_text }}</span>
              </div>
            </template>
            <div class="card-content">
              <p class="content">{{ item.content ? item.content.substring(0, 200) + '...' : '暂无内容' }}</p>
              <div class="meta">
                <span class="source">{{ item.source }}</span>
                <span class="province">{{ item.province || '全国' }}</span>
                <span class="school">{{ item.school || '全部' }}</span>
                <span class="date">{{ formatDate(item.publish_time) }}</span>
              </div>
              <div class="actions">
                <el-button type="primary" size="small" @click="viewDetail(item.id)">查看详情</el-button>
                <el-button size="small" @click="likeInfo(item.id)">
                  <el-icon><Star /></el-icon> {{ item.like_count }}
                </el-button>
                <el-button size="small" @click="favoriteInfo(item.id)">
                  <el-icon><Collection /></el-icon> {{ item.is_favorite ? '已收藏' : '收藏' }}
                </el-button>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 分页 -->
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
      </div>
    </el-main>

    <!-- 底部 -->
    <el-footer height="120px" class="footer">
      <div class="container">
        <p>© 2026 双赛道情报通 版权所有</p>
        <p>7×24小时自动抓取、分类、推送考研+考公官方关键信息的情报平台</p>
      </div>
    </el-footer>

    <!-- 移动端底部导航 -->
    <MobileTabBar />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowDown, Search, Star, Collection } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from '@/utils/axios'
import MobileTabBar from '@/components/MobileTabBar.vue'

const router = useRouter()
const activeIndex = ref('/kaoyan')
const isLoggedIn = ref(false)
const userInfo = ref({})

// 搜索和筛选
const searchKeyword = ref('')
const filterProvince = ref('')
const filterCategory = ref('')
const sortBy = ref('publish_date')

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 数据
const kaoyanInfoList = ref([])
const provinces = ref(['全国', '北京', '上海', '广东', '江苏', '浙江', '山东', '河南', '四川', '湖北'])
const categories = ref(['政策通知', '招生简章', '分数线', '复试信息', '调剂信息', '报名信息', '准考证', '成绩查询'])

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

// 搜索情报
const searchInfo = () => {
  currentPage.value = 1
  getKaoyanInfo()
}

// 查看详情
const viewDetail = (id) => {
  // 实际应该跳转到详情页

}



// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  getKaoyanInfo()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getKaoyanInfo()
}

// 加载状态
const loading = ref(false)

// 获取考研情报（目前未开发，返回空数据）
const getKaoyanInfo = async () => {
  try {
    loading.value = true
    // 目前未开发，直接返回空数据
    kaoyanInfoList.value = []
    total.value = 0
  } catch (error) {

    kaoyanInfoList.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 获取省份列表（目前未开发，返回默认数据）
const getProvinces = async () => {
  try {
    // 目前未开发，使用默认数据
  } catch (error) {

  }
}

// 点赞情报
const likeInfo = async (id) => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      ElMessage.warning('请先登录')
      return
    }
    
    const response = await axios.post(`/api/v1/kaoyan/info/like/${id}`, {}, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.success) {
      ElMessage.success('点赞成功')
      const item = kaoyanInfoList.value.find(item => item.id === id)
      if (item) {
        item.like_count = response.data.like_count
      }
    } else {
      ElMessage.error('点赞失败')
    }
  } catch (error) {
    console.error('点赞失败:', error)
    ElMessage.error('点赞失败，请稍后重试')
  }
}

// 收藏情报
const favoriteInfo = async (id) => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      ElMessage.warning('请先登录')
      return
    }
    
    // 这里应该调用收藏API，暂时使用模拟数据
    ElMessage.success('收藏成功')
  } catch (error) {
    console.error('收藏失败:', error)
    ElMessage.error('收藏失败，请稍后重试')
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
  getProvinces()
  getKaoyanInfo()
})
</script>

<style scoped>
.kaoyan {
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

.search-filter {
  margin-bottom: 30px;
}

.info-list {
  margin-bottom: 30px;
}

.info-card {
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
  font-weight: bold;
  color: #333;
}

.category {
  background-color: #f0f2f5;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
  color: #666;
}

.card-content {
  margin-top: 15px;
}

.content {
  margin-bottom: 15px;
  color: #666;
  line-height: 1.5;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 15px;
  font-size: 14px;
  color: #999;
}

.actions {
  display: flex;
  gap: 10px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
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
