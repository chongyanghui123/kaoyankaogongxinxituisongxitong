<template>
  <div class="user">
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
          <el-dropdown>
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
        <el-row :gutter="20">
          <!-- 左侧菜单 -->
          <el-col :span="6">
            <el-card class="user-menu">
              <el-menu
                :default-active="activeMenu"
                class="el-menu-vertical-demo"
                @select="handleMenuSelect"
              >
                <el-menu-item index="profile">
                  <el-icon><User /></el-icon>
                  <span>个人资料</span>
                </el-menu-item>
                <el-menu-item index="subscription">
                  <el-icon><Ticket /></el-icon>
                  <span>会员订阅</span>
                </el-menu-item>
                <el-menu-item index="requirements">
                  <el-icon><Setting /></el-icon>
                  <span>需求配置</span>
                </el-menu-item>
                <el-menu-item index="keywords">
                  <el-icon><Search /></el-icon>
                  <span>关键词设置</span>
                </el-menu-item>
                <el-menu-item index="favorites">
                  <el-icon><Collection /></el-icon>
                  <span>我的收藏</span>
                </el-menu-item>
                <el-menu-item index="read">
                  <el-icon><Document /></el-icon>
                  <span>阅读历史</span>
                </el-menu-item>
                <el-menu-item index="materials">
                  <el-icon><Download /></el-icon>
                  <span>学习资料</span>
                </el-menu-item>
              </el-menu>
            </el-card>
          </el-col>

          <!-- 右侧内容 -->
          <el-col :span="18">
            <!-- 个人资料 -->
            <div v-if="activeMenu === 'profile'" class="user-content">
              <el-card class="content-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><User /></el-icon>
                    <span>个人资料</span>
                  </div>
                </template>
                <el-form :model="userForm" :rules="rules" ref="userFormRef" label-width="100px">
                  <el-form-item label="用户名" prop="username">
                    <el-input v-model="userForm.username" placeholder="请输入用户名" />
                  </el-form-item>
                  <el-form-item label="邮箱" prop="email">
                    <el-input v-model="userForm.email" placeholder="请输入邮箱" disabled />
                  </el-form-item>
                  <el-form-item label="手机号" prop="phone">
                    <el-input v-model="userForm.phone" placeholder="请输入手机号" />
                  </el-form-item>
                  <el-form-item label="修改密码" prop="password">
                    <el-input v-model="userForm.password" type="password" placeholder="请输入新密码" show-password />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="updateProfile">保存修改</el-button>
                  </el-form-item>
                </el-form>
              </el-card>
            </div>

            <!-- 会员订阅 -->
            <div v-if="activeMenu === 'subscription'" class="user-content">
              <el-card class="content-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Ticket /></el-icon>
                    <span>会员订阅</span>
                  </div>
                </template>
                <div v-if="subscription" class="subscription-info">
                  <p>当前会员类型: <el-tag type="success">{{ subscription.type }}</el-tag></p>
                  <p>开始时间: {{ formatDate(subscription.start_date) }}</p>
                  <p>结束时间: {{ formatDate(subscription.end_date) }}</p>
                  <p v-if="subscription.is_active">状态: <el-tag type="success">已激活</el-tag></p>
                  <p v-else>状态: <el-tag type="danger">已过期</el-tag></p>
                  <el-button type="primary" @click="renewSubscription">续费</el-button>
                </div>
                <div v-else class="no-subscription">
                  <p>您当前未订阅会员</p>
                  <el-button type="primary" @click="buySubscription">立即购买</el-button>
                </div>
                
                <div class="products">
                  <h3>会员套餐</h3>
                  <el-row :gutter="20">
                    <el-col :span="8" v-for="product in products" :key="product.id">
                      <el-card shadow="hover" class="product-card">
                        <h4>{{ product.name }}</h4>
                        <p class="price">¥{{ product.price }}</p>
                        <p class="description">{{ product.description }}</p>
                        <el-button type="primary" @click="selectProduct(product.id)">{{ product.status == 1 ? '立即购买' : '已下架' }}</el-button>
                      </el-card>
                    </el-col>
                  </el-row>
                </div>
              </el-card>
            </div>

            <!-- 订阅配置 -->
            <div v-if="activeMenu === 'subscription'" class="user-content">
              <el-card class="content-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Ticket /></el-icon>
                    <span>会员订阅</span>
                  </div>
                </template>
                <div v-if="subscription" class="subscription-info">
                  <p>当前会员类型: <el-tag type="success">{{ subscription.type }}</el-tag></p>
                  <p>开始时间: {{ formatDate(subscription.start_date) }}</p>
                  <p>结束时间: {{ formatDate(subscription.end_date) }}</p>
                  <p v-if="subscription.is_active">状态: <el-tag type="success">已激活</el-tag></p>
                  <p v-else>状态: <el-tag type="danger">已过期</el-tag></p>
                  <el-button type="primary" @click="renewSubscription">续费</el-button>
                </div>
                <div v-else class="no-subscription">
                  <p>您当前未订阅会员</p>
                  <el-button type="primary" @click="buySubscription">立即购买</el-button>
                </div>
                
                <div class="products">
                  <h3>会员套餐</h3>
                  <el-row :gutter="20">
                    <el-col :span="8" v-for="product in products" :key="product.id">
                      <el-card shadow="hover" class="product-card">
                        <h4>{{ product.name }}</h4>
                        <p class="price">¥{{ product.price }}</p>
                        <p class="description">{{ product.description }}</p>
                        <el-button type="primary" @click="selectProduct(product.id)">{{ product.status == 1 ? '立即购买' : '已下架' }}</el-button>
                      </el-card>
                    </el-col>
                  </el-row>
                </div>
              </el-card>
            </div>

            <!-- 需求配置 -->
            <div v-if="activeMenu === 'requirements'" class="user-content">
              <el-card class="content-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Setting /></el-icon>
                    <span>需求配置</span>
                  </div>
                </template>
                <el-tabs v-model="activeRequirementTab">
                  <!-- 考研需求 -->
                  <el-tab-pane label="考研需求" name="kaoyan">
                    <el-form :model="kaoyanRequirement" label-width="100px">
                      <el-form-item label="关注省份">
                        <el-select v-model="kaoyanRequirement.provinces" multiple placeholder="选择省份">
                          <el-option label="北京" value="北京" />
                          <el-option label="上海" value="上海" />
                          <el-option label="广东" value="广东" />
                          <el-option label="江苏" value="江苏" />
                          <el-option label="浙江" value="浙江" />
                          <el-option label="湖北" value="湖北" />
                          <el-option label="湖南" value="湖南" />
                          <el-option label="四川" value="四川" />
                          <el-option label="山东" value="山东" />
                          <el-option label="河南" value="河南" />
                        </el-select>
                      </el-form-item>
                      <el-form-item label="关注学校">
                        <el-input v-model="kaoyanRequirement.schools" type="textarea" placeholder="请输入关注的学校，多个学校用逗号分隔" />
                      </el-form-item>
                      <el-form-item label="关注专业">
                        <el-input v-model="kaoyanRequirement.majors" type="textarea" placeholder="请输入关注的专业，多个专业用逗号分隔" />
                      </el-form-item>
                      <el-form-item label="关注类型">
                        <el-checkbox-group v-model="kaoyanRequirement.types">
                          <el-checkbox label="招生简章" />
                          <el-checkbox label="分数线" />
                          <el-checkbox label="复试信息" />
                          <el-checkbox label="调剂信息" />
                          <el-checkbox label="专业目录" />
                        </el-checkbox-group>
                      </el-form-item>
                      <el-form-item>
                        <el-button type="primary" @click="saveKaoyanRequirement">保存配置</el-button>
                      </el-form-item>
                    </el-form>
                  </el-tab-pane>
                  <!-- 考公需求 -->
                  <el-tab-pane label="考公需求" name="kaogong">
                    <el-form :model="kaogongRequirement" label-width="100px">
                      <el-form-item label="关注省份">
                        <el-select v-model="kaogongRequirement.provinces" multiple placeholder="选择省份">
                          <el-option label="北京" value="北京" />
                          <el-option label="上海" value="上海" />
                          <el-option label="广东" value="广东" />
                          <el-option label="江苏" value="江苏" />
                          <el-option label="浙江" value="浙江" />
                          <el-option label="湖北" value="湖北" />
                          <el-option label="湖南" value="湖南" />
                          <el-option label="四川" value="四川" />
                          <el-option label="山东" value="山东" />
                          <el-option label="河南" value="河南" />
                        </el-select>
                      </el-form-item>
                      <el-form-item label="关注职位类型">
                        <el-checkbox-group v-model="kaogongRequirement.positionTypes">
                          <el-checkbox label="公务员" />
                          <el-checkbox label="事业单位" />
                          <el-checkbox label="选调生" />
                          <el-checkbox label="三支一扶" />
                          <el-checkbox label="军队文职" />
                        </el-checkbox-group>
                      </el-form-item>
                      <el-form-item label="关注专业">
                        <el-input v-model="kaogongRequirement.majors" type="textarea" placeholder="请输入关注的专业，多个专业用逗号分隔" />
                      </el-form-item>
                      <el-form-item label="学历要求">
                        <el-checkbox-group v-model="kaogongRequirement.educationLevels">
                          <el-checkbox label="本科" />
                          <el-checkbox label="硕士" />
                          <el-checkbox label="博士" />
                          <el-checkbox label="专科" />
                        </el-checkbox-group>
                      </el-form-item>
                      <el-form-item>
                        <el-button type="primary" @click="saveKaogongRequirement">保存配置</el-button>
                      </el-form-item>
                    </el-form>
                  </el-tab-pane>
                  <!-- 推送设置 -->
                  <el-tab-pane label="推送设置" name="push">
                    <el-form :model="pushSettings" label-width="100px">
                      <el-form-item label="推送频率">
                        <el-select v-model="pushSettings.frequency" placeholder="选择推送频率">
                          <el-option label="每小时" value="hourly" />
                          <el-option label="每天" value="daily" />
                          <el-option label="每周" value="weekly" />
                        </el-select>
                      </el-form-item>
                      <el-form-item label="推送时间">
                        <el-time-picker
                          v-model="pushSettings.time"
                          format="HH:mm"
                          placeholder="选择推送时间"
                          style="width: 100%"
                        />
                      </el-form-item>
                      <el-form-item>
                        <el-button type="primary" @click="savePushSettings">保存设置</el-button>
                      </el-form-item>
                    </el-form>
                  </el-tab-pane>
                </el-tabs>
              </el-card>
            </div>

            <!-- 关键词设置 -->
            <div v-if="activeMenu === 'keywords'" class="user-content">
              <el-card class="content-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Search /></el-icon>
                    <span>关键词设置</span>
                  </div>
                </template>
                <el-form :model="keywordForm" :rules="keywordRules" ref="keywordFormRef" label-width="100px">
                  <el-form-item label="关键词" prop="keyword">
                    <el-input v-model="keywordForm.keyword" placeholder="请输入关键词" />
                  </el-form-item>
                  <el-form-item label="分类" prop="category">
                    <el-select v-model="keywordForm.category" placeholder="选择分类">
                      <el-option label="考研" value="kaoyan" />
                      <el-option label="考公" value="kaogong" />
                    </el-select>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="addKeyword">添加关键词</el-button>
                  </el-form-item>
                </el-form>
                
                <el-table :data="keywords" style="width: 100%">
                  <el-table-column prop="keyword" label="关键词" width="180" />
                  <el-table-column prop="category" label="分类" width="120" />
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button type="danger" size="small" @click="deleteKeyword(scope.row.id)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </div>

            <!-- 我的收藏 -->
            <div v-if="activeMenu === 'favorites'" class="user-content">
              <el-card class="content-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Collection /></el-icon>
                    <span>我的收藏</span>
                  </div>
                </template>
                <el-table :data="favorites" style="width: 100%">
                  <el-table-column prop="title" label="标题" />
                  <el-table-column prop="info_type" label="类型" width="100" />
                  <el-table-column prop="created_at" label="收藏时间" width="180" />
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button type="primary" size="small" @click="viewFavorite(scope.row.info_id, scope.row.info_type)">查看</el-button>
                      <el-button type="danger" size="small" @click="removeFavorite(scope.row.id)">取消收藏</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </div>

            <!-- 阅读历史 -->
            <div v-if="activeMenu === 'read'" class="user-content">
              <el-card class="content-card">
                <template #header>
                  <div class="card-header">
                    <el-icon><Document /></el-icon>
                    <span>阅读历史</span>
                  </div>
                </template>
                <el-table :data="readHistory" style="width: 100%">
                  <el-table-column prop="title" label="标题" />
                  <el-table-column prop="info_type" label="类型" width="100" />
                  <el-table-column prop="read_at" label="阅读时间" width="180" />
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button type="primary" size="small" @click="viewReadInfo(scope.row.info_id, scope.row.info_type)">查看</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </div>

            <!-- 学习资料 -->
            <div v-if="activeMenu === 'materials'" class="user-content">
              <learning-material-download />
            </div>
          </el-col>
        </el-row>
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Ticket, Search, Collection, Document, ArrowDown, Setting, Download } from '@element-plus/icons-vue'
import axios from 'axios'
import LearningMaterialDownload from '../components/LearningMaterialDownload.vue'

const router = useRouter()
const activeIndex = ref('/user')
const activeMenu = ref('profile')
const userInfo = ref({})

// 个人资料
const userForm = reactive({
  username: '',
  email: '',
  phone: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在3-50之间', trigger: 'blur' }
  ],
  phone: [
    { required: false, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' }
  ],
  password: [
    { required: false, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

// 关键词设置
const keywordForm = reactive({
  keyword: '',
  category: ''
})

const keywordRules = {
  keyword: [
    { required: true, message: '请输入关键词', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'blur' }
  ]
}

// 数据
const subscription = ref(null)
const products = ref([])
const keywords = ref([])
const favorites = ref([])
const readHistory = ref([])

// 需求配置
const activeRequirementTab = ref('kaoyan')
const kaoyanRequirement = reactive({
  provinces: [],
  schools: '',
  majors: '',
  types: []
})
const kaogongRequirement = reactive({
  provinces: [],
  positionTypes: [],
  majors: '',
  educationLevels: []
})

// 推送设置
const pushSettings = reactive({
  frequency: 'daily',
  time: null
})

// 处理菜单选择
const handleSelect = (key) => {
  navigateTo(key)
}

// 处理左侧菜单选择
const handleMenuSelect = (key) => {
  activeMenu.value = key
}

// 导航到指定路径
const navigateTo = (path) => {
  router.push(path)
}

// 退出登录
const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('userInfo')
  router.push('/login')
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString()
}

// 更新个人资料
const updateProfile = async () => {
  // 实际应该调用API
  ElMessage.success('个人资料更新成功')
}

// 续费订阅
const renewSubscription = () => {
  // 实际应该调用API
  ElMessage.success('续费成功')
}

// 购买订阅
const buySubscription = () => {
  // 实际应该调用API
  ElMessage.success('购买成功')
}

// 选择产品
const selectProduct = (productId) => {
  // 实际应该调用API
  ElMessage.success('产品选择成功')
}

// 添加关键词
const addKeyword = async () => {
  // 实际应该调用API
  keywords.value.push({
    id: keywords.value.length + 1,
    keyword: keywordForm.keyword,
    category: keywordForm.category
  })
  keywordForm.keyword = ''
  keywordForm.category = ''
  ElMessage.success('关键词添加成功')
}

// 删除关键词
const deleteKeyword = (id) => {
  // 实际应该调用API
  keywords.value = keywords.value.filter(item => item.id !== id)
  ElMessage.success('关键词删除成功')
}

// 查看收藏
const viewFavorite = (infoId, infoType) => {
  // 实际应该跳转到详情页

}

// 取消收藏
const removeFavorite = (id) => {
  // 实际应该调用API
  favorites.value = favorites.value.filter(item => item.id !== id)
  ElMessage.success('取消收藏成功')
}

// 查看阅读历史
const viewReadInfo = (infoId, infoType) => {
  // 实际应该跳转到详情页

}

// 保存考研需求
const saveKaoyanRequirement = async () => {
  // 实际应该调用API

  ElMessage.success('考研需求保存成功')
}

// 保存考公需求
const saveKaogongRequirement = async () => {
  // 实际应该调用API

  ElMessage.success('考公需求保存成功')
}

// 保存推送设置
const savePushSettings = async () => {
  try {
    // 格式化时间
    let timeStr = null
    if (pushSettings.time) {
      const hours = pushSettings.time.getHours().toString().padStart(2, '0')
      const minutes = pushSettings.time.getMinutes().toString().padStart(2, '0')
      timeStr = `${hours}:${minutes}`
    }
    
    const response = await axios.put('/api/v1/users/push-settings', {
      frequency: pushSettings.frequency,
      time: timeStr
    })
    
    if (response.data.success) {
      ElMessage.success('推送设置保存成功')
    } else {
      ElMessage.error(response.data.message || '保存失败')
    }
  } catch (error) {
    console.error('保存推送设置失败:', error)
    console.error('错误详情:', error.response ? error.response.data : error.message)
    ElMessage.error('保存失败，请稍后重试')
  }
}

// 获取用户信息
const getUserInfo = async () => {
  try {
    // 模拟数据，实际应该调用API
    try {
      const userInfoStr = localStorage.getItem('userInfo')
      userInfo.value = userInfoStr && userInfoStr !== 'undefined' && userInfoStr !== 'null' 
        ? JSON.parse(userInfoStr) 
        : {}
    } catch (error) {
      console.error('解析用户信息失败:', error)
      userInfo.value = {}
    }
    userForm.username = userInfo.value.username || ''
    userForm.email = userInfo.value.email || ''
    userForm.phone = userInfo.value.phone || ''
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 获取订阅信息
const getSubscription = async () => {
  try {
    // 模拟数据，实际应该调用API
    subscription.value = {
      type: '高级会员',
      start_date: '2026-01-01',
      end_date: '2026-12-31',
      is_active: true
    }
  } catch (error) {
    console.error('获取订阅信息失败:', error)
  }
}

// 获取产品列表
const getProducts = async () => {
  try {
    // 模拟数据，实际应该调用API
    products.value = [
      {
        id: 1,
        name: '月度会员',
        price: 19.9,
        description: '月会员，享受所有高级功能',
        is_active: true
      },
      {
        id: 2,
        name: '季度会员',
        price: 49.9,
        description: '季会员，享受所有高级功能',
        is_active: true
      },
      {
        id: 3,
        name: '年度会员',
        price: 149.9,
        description: '年会员，享受所有高级功能',
        is_active: true
      }
    ]
  } catch (error) {
    console.error('获取产品列表失败:', error)
  }
}

// 获取关键词列表
const getKeywords = async () => {
  try {
    // 模拟数据，实际应该调用API
    keywords.value = [
      { id: 1, keyword: '考研国家线', category: 'kaoyan' },
      { id: 2, keyword: '公务员考试', category: 'kaogong' }
    ]
  } catch (error) {
    console.error('获取关键词列表失败:', error)
  }
}

// 获取收藏列表
const getFavorites = async () => {
  try {
    // 模拟数据，实际应该调用API
    favorites.value = [
      {
        id: 1,
        info_id: 1,
        info_type: 'kaoyan',
        title: '2026年全国硕士研究生招生考试公告',
        created_at: '2026-10-01 10:00:00'
      },
      {
        id: 2,
        info_id: 1,
        info_type: 'kaogong',
        title: '2026年国家公务员招考公告',
        created_at: '2026-10-15 15:00:00'
      }
    ]
  } catch (error) {
    console.error('获取收藏列表失败:', error)
  }
}

// 获取阅读历史
const getReadHistory = async () => {
  try {
    // 模拟数据，实际应该调用API
    readHistory.value = [
      {
        id: 1,
        info_id: 1,
        info_type: 'kaoyan',
        title: '2026年全国硕士研究生招生考试公告',
        read_at: '2026-10-01 10:30:00'
      },
      {
        id: 2,
        info_id: 2,
        info_type: 'kaoyan',
        title: '2026年考研国家线公布',
        read_at: '2026-10-02 14:00:00'
      },
      {
        id: 3,
        info_id: 1,
        info_type: 'kaogong',
        title: '2026年国家公务员招考公告',
        read_at: '2026-10-15 15:30:00'
      }
    ]
  } catch (error) {
    console.error('获取阅读历史失败:', error)
  }
}

// 获取推送设置
const getPushSettings = async () => {
  try {
    const response = await axios.get('/api/v1/users/push-settings')
    if (response.data.success) {
      const settings = response.data.data
      pushSettings.frequency = settings.frequency || 'daily'
      if (settings.time) {
        // 转换时间格式
        const [hours, minutes] = settings.time.split(':')
        pushSettings.time = new Date()
        pushSettings.time.setHours(parseInt(hours))
        pushSettings.time.setMinutes(parseInt(minutes))
      }
    }
  } catch (error) {
    console.error('获取推送设置失败:', error)
  }
}

onMounted(() => {
  getUserInfo()
  getSubscription()
  getProducts()
  getKeywords()
  getFavorites()
  getReadHistory()
  getPushSettings()
})
</script>

<style scoped>
.user {
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

.user-menu {
  height: fit-content;
}

.content-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}

.card-header el-icon {
  margin-right: 8px;
}

.subscription-info {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.subscription-info p {
  margin: 10px 0;
}

.no-subscription {
  margin-bottom: 30px;
  padding: 40px;
  text-align: center;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.products {
  margin-top: 30px;
}

.products h3 {
  margin-bottom: 20px;
}

.product-card {
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-card h4 {
  margin-bottom: 10px;
}

.product-card .price {
  font-size: 20px;
  font-weight: bold;
  color: #f56c6c;
  margin-bottom: 10px;
}

.product-card .description {
  margin-bottom: 20px;
  color: #666;
  flex: 1;
}

.user-content {
  min-height: 600px;
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
