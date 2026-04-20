<template>
  <div class="admin">
    <div class="admin-container">
      <!-- 左侧导航栏 -->
      <el-aside width="200px" class="aside">
        <div class="logo">
          <h1>双赛道情报通</h1>
        </div>
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="vertical"
          @select="handleSelect"
          background-color="#ffffff"
          text-color="#333333"
          active-text-color="#1890ff"
          :default-openeds="['/admin']"
        >
          <el-menu-item index="/admin/overview">
            <el-icon><DataAnalysis /></el-icon>
            <span>系统概览</span>
          </el-menu-item>
          <el-menu-item index="/admin">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/kaoyan">
            <el-icon><Document /></el-icon>
            <span>考研情报管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/kaogong">
            <el-icon><Paperclip /></el-icon>
            <span>考公情报管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/crawlers">
            <el-icon><Refresh /></el-icon>
            <span>爬虫管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/products">
            <el-icon><ShoppingCart /></el-icon>
            <span>产品管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/payments">
            <el-icon><CreditCard /></el-icon>
            <span>支付管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/system">
            <el-icon><Setting /></el-icon>
            <span>系统配置</span>
          </el-menu-item>
          <el-menu-item index="/admin/push">
            <el-icon><Message /></el-icon>
            <span>推送管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/materials">
            <el-icon><Download /></el-icon>
            <span>学习资料管理</span>
          </el-menu-item>

          <el-dropdown>
            <span class="el-dropdown-link user-dropdown">
              {{ userInfo.username }}
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-menu>
      </el-aside>

      <!-- 主要内容 -->
      <el-main class="main">
        <div class="container">
          <!-- 用户管理 -->
          <UserManagement v-if="activeIndex === '/admin'" />
          
          <!-- 爬虫管理 -->
          <CrawlerManagement v-if="activeIndex === '/admin/crawlers'" />
          
          <!-- 考研情报管理 -->
          <KaoyanInfoManagement v-if="activeIndex === '/admin/kaoyan'" />
          
          <!-- 考公情报管理 -->
          <KaogongInfoManagement v-if="activeIndex === '/admin/kaogong'" />
          
          <!-- 产品管理 -->
          <ProductManagement v-if="activeIndex === '/admin/products'" />
          
          <!-- 支付管理 -->
          <PaymentManagement v-if="activeIndex === '/admin/payments'" />
          
          <!-- 系统配置 -->
          <SystemConfigManagement v-if="activeIndex === '/admin/system'" />
          
          <!-- 系统概览 -->
          <div v-if="activeIndex === '/admin/overview'" class="admin-content">
            <SystemOverview />
          </div>
          
          <!-- 推送管理 -->
          <PushManagement v-if="activeIndex === '/admin/push'" />
          
          <!-- 学习资料管理 -->
          <LearningMaterialManagement v-if="activeIndex === '/admin/materials'" />
          

        </div>
      </el-main>
    </div>

    <!-- 底部 -->
    <el-footer height="60px" class="footer">
      <div class="container">
        <p>© 2026 双赛道情报通 版权所有</p>
      </div>
    </el-footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowDown, Search, User, Refresh, ShoppingCart, Setting, Document, DataAnalysis, Paperclip, CreditCard, Message, Bell, Download } from '@element-plus/icons-vue'
import axios from 'axios'

// 导入模块化组件
import UserManagement from '../components/admin/UserManagement.vue'
import CrawlerManagement from '../components/admin/CrawlerManagement.vue'
import KaoyanInfoManagement from '../components/admin/KaoyanInfoManagement.vue'
import KaogongInfoManagement from '../components/admin/KaogongInfoManagement.vue'
import ProductManagement from '../components/admin/ProductManagement.vue'
import PaymentManagement from '../components/admin/PaymentManagement.vue'
import SystemConfigManagement from '../components/admin/SystemConfigManagement.vue'
import SystemOverview from '../components/admin/SystemOverview.vue'
import PushManagement from '../components/admin/PushManagement.vue'
import LearningMaterialManagement from '../components/admin/LearningMaterialManagement.vue'


// const router = useRouter()
// 从本地存储中读取保存的活跃标签页，默认为用户管理
const savedTab = localStorage.getItem('activeAdminTab')
const activeIndex = ref(savedTab || '/admin')
const userInfo = ref({})

// 处理菜单选择
const handleSelect = (key) => {
  activeIndex.value = key
  // 保存到本地存储
  localStorage.setItem('activeAdminTab', key)
}

// 导航到指定路径
const navigateTo = (path) => {
  // 对于外部页面（如个人中心），仍然使用路由跳转
  window.location.href = path
}

// 退出登录
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('userInfo')
  window.location.href = '/login'
}

// 获取用户信息
const getUserInfo = async () => {
  try {
    try {
      const userInfoStr = localStorage.getItem('userInfo')
      userInfo.value = userInfoStr && userInfoStr !== 'undefined' && userInfoStr !== 'null' 
        ? JSON.parse(userInfoStr) 
        : {}
    } catch (error) {
      console.error('解析用户信息失败:', error)
      userInfo.value = {}
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

onMounted(() => {
  getUserInfo()
  // 从本地存储中读取保存的活跃标签页
  const savedTab = localStorage.getItem('activeAdminTab')
  if (savedTab) {
    activeIndex.value = savedTab
  }
})
</script>

<style scoped>
.admin {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.admin-container {
  display: flex;
  flex: 1;
  min-height: 0;
}

.aside {
  background-color: #ffffff;
  height: 100%;
  position: sticky;
  top: 0;
  overflow-y: auto;
  border-right: 1px solid #e8e8e8;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
}

.logo {
  padding: 0 20px;
  border-bottom: 1px solid #e8e8e8;
}

.logo h1 {
  color: #1890ff;
  margin: 0;
  font-size: 18px;
  line-height: 60px;
  font-weight: bold;
}

.el-menu-demo {
  height: calc(100% - 60px);
  border-right: none;
}

.el-menu-item {
  height: 48px;
  line-height: 48px;
  margin: 0 12px;
  border-radius: 4px;
  margin-bottom: 4px;
}

.el-menu-item:hover {
  background-color: #f0f2f5 !important;
}

.el-menu-item.is-active {
  background-color: #e6f7ff !important;
}

.user-dropdown {
  display: block;
  padding: 12px 20px;
  color: #333;
  cursor: pointer;
  margin-top: 20px;
  border-top: 1px solid #e8e8e8;
}

.user-dropdown:hover {
  background-color: #f0f2f5;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.main {
  flex: 1;
  padding: 40px 0;
  overflow-y: auto;
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
  font-weight: bold;
  color: #333;
}

.subtitle {
  margin: 30px 0 20px 0;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.add-user-btn {
  margin-left: auto;
}

.search-filter {
  margin-bottom: 30px;
}

.province-tag,
.type-tag,
.keyword-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.student-crawlers {
  margin-top: 30px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.footer {
  background-color: #f0f2f5;
  padding: 0;
  text-align: center;
  color: #666;
  line-height: 60px;
}

.footer p {
  margin: 0;
}

.info-content {
  padding: 40px;
  text-align: center;
  color: #666;
  font-size: 16px;
}
</style>