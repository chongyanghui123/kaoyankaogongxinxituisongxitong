<template>
  <div class="payment-container">
    <el-card class="payment-card">
      <template #header>
        <div class="card-header">
          <h2>订单支付</h2>
          <div class="countdown" v-if="remainingTime > 0">
            <el-alert
              title="支付倒计时"
              type="warning"
              :description="formatCountdown(remainingTime)"
              :closable="false"
            >
            </el-alert>
          </div>
        </div>
      </template>

      <div class="payment-content">
        <!-- 订单信息 -->
        <el-card class="order-info-card" shadow="hover">
          <template #header>
            <span>订单信息</span>
          </template>
          
          <div class="order-details">
            <el-row :gutter="16">
              <el-col :span="12">
                <div class="info-item">
                  <span class="label">订单编号：</span>
                  <span class="value">{{ orderInfo.order_no }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="info-item">
                  <span class="label">创建时间：</span>
                  <span class="value">{{ orderInfo.created_at }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="info-item">
                  <span class="label">支付金额：</span>
                  <span class="value amount">{{ formatAmount(orderInfo.total_amount) }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="info-item">
                  <span class="label">支付方式：</span>
                  <span class="value">{{ getPaymentMethodText(orderInfo.payment_method) }}</span>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="info-item">
                  <span class="label">订单状态：</span>
                  <el-tag :type="getOrderStatusType(orderInfo.payment_status)">{{ getOrderStatusText(orderInfo.payment_status) }}</el-tag>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="info-item">
                  <span class="label">产品名称：</span>
                  <span class="value">{{ orderInfo.product_name }}</span>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-card>

        <!-- 支付方式 -->
        <el-card class="payment-method-card" shadow="hover">
          <template #header>
            <span>选择支付方式</span>
          </template>
          
          <el-radio-group v-model="selectedPaymentMethod" @change="updatePaymentMethod">
            <el-row :gutter="16">
              <el-col :span="8">
                <el-radio :value="1">
                  <div class="payment-option">
                    <el-icon class="payment-icon"><CreditCard /></el-icon>
                    <span>微信支付</span>
                  </div>
                </el-radio>
              </el-col>
              <el-col :span="8">
                <el-radio :value="2">
                  <div class="payment-option">
                    <el-icon class="payment-icon"><Money /></el-icon>
                    <span>支付宝</span>
                  </div>
                </el-radio>
              </el-col>
              <el-col :span="8">
                <el-radio :value="3">
                  <div class="payment-option">
                    <el-icon class="payment-icon"><CreditCard /></el-icon>
                    <span>银行卡</span>
                  </div>
                </el-radio>
              </el-col>
            </el-row>
          </el-radio-group>
        </el-card>

        <!-- 支付二维码 -->
        <el-card class="qr-code-card" shadow="hover" v-if="showQrCode">
          <template #header>
            <span>扫描二维码支付</span>
          </template>
          
          <div class="qr-code-container">
            <div class="qr-code-placeholder">
              <el-empty description="模拟支付二维码"></el-empty>
            </div>
            <div class="qr-code-actions">
              <el-button type="primary" @click="simulatePayment">
                <el-icon><Check /></el-icon>
                模拟支付成功
              </el-button>
              <el-button @click="copyQrCode">
                <el-icon><DocumentCopy /></el-icon>
                复制链接
              </el-button>
            </div>
          </div>
        </el-card>

        <!-- 支付操作 -->
        <div class="payment-actions">
          <el-button type="danger" @click="handleCancel">
            <el-icon><Delete /></el-icon>
            取消支付
          </el-button>
          <el-button type="primary" @click="handlePayment" :loading="isProcessing">
            <el-icon><CreditCard /></el-icon>
            {{ isProcessing ? '支付中...' : '立即支付' }}
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 支付成功对话框 -->
    <el-dialog v-model="showSuccessDialog" title="支付成功" width="500px" :close-on-click-modal="false">
      <div class="success-content">
        <el-empty description="支付成功">
          <template #image>
            <img src="https://element-plus.org/images/empty.svg" style="width: 120px; height: 120px;" alt="success" />
          </template>
          <template #description>
            <div class="success-text">
              <p>您的订单已成功支付</p>
              <p>感谢您的购买！</p>
            </div>
          </template>
        </el-empty>
      </div>
      <template #footer>
        <el-button type="primary" @click="goBack">返回</el-button>
      </template>
    </el-dialog>

    <!-- 支付失败对话框 -->
    <el-dialog v-model="showFailureDialog" title="支付失败" width="500px" :close-on-click-modal="false">
      <div class="failure-content">
        <el-empty description="支付失败">
          <template #image>
            <img src="https://element-plus.org/images/empty.svg" style="width: 120px; height: 120px;" alt="failure" />
          </template>
          <template #description>
            <div class="failure-text">
              <p>{{ failureMessage }}</p>
              <p>请重新尝试支付</p>
            </div>
          </template>
        </el-empty>
      </div>
      <template #footer>
        <el-button @click="showFailureDialog = false">关闭</el-button>
        <el-button type="primary" @click="handleRetry">重新支付</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { Clock, CopyDocument, Check, Refresh, CreditCard, Money, Phone, Delete, DocumentCopy } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const orderId = ref(null)
const productId = ref(route.query.product_id || null)
const paymentMethod = ref(route.query.payment_method || 1)

const orderInfo = reactive({
  order_no: '',
  product_name: '',
  product_id: 0,
  price: 0,
  quantity: 0,
  total_amount: 0,
  payment_method: paymentMethod.value,
  payment_status: 0,
  created_at: '',
  paid_at: '',
  updated_at: '',
  payment_time: '',
  user_id: 0
})

const paymentMethods = [
  { value: 1, label: '微信支付', icon: 'wechat' },
  { value: 2, label: '支付宝', icon: 'alipay' },
  { value: 3, label: '银行卡', icon: 'card' }
]

// 倒计时
const countdown = ref(10 * 60)
const timer = ref(null)

// 状态
const isProcessing = ref(false)
const showSuccessDialog = ref(false)
const showFailureDialog = ref(false)
const showQrCode = ref(false)
const failureMessage = ref('')
const selectedPaymentMethod = ref(paymentMethod.value)
const remainingTime = ref(600) // 10分钟倒计时（秒）
const countdownTimer = ref(null)

// 生成倒计时存储的key - 使用产品ID作为基础，确保页面刷新后能找到
const getCountdownKey = () => {
  return `payment_countdown_${productId.value || 'default'}`
}

// 保存倒计时数据
const saveCountdown = () => {
  if (remainingTime.value > 0) {
    localStorage.setItem(getCountdownKey(), remainingTime.value.toString())
  } else {
    localStorage.removeItem(getCountdownKey())
  }
}

// 加载倒计时数据
const loadCountdown = () => {
  const key = getCountdownKey()
  const savedTime = localStorage.getItem(key)
  if (savedTime) {
    const parsedTime = parseInt(savedTime)
    if (parsedTime > 0) {
      remainingTime.value = parsedTime
    }
  }
}

// 获取订单详情
const getOrderDetail = async (orderId) => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`/api/v1/payments/orders/${orderId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.data && response.data.success) {
      Object.assign(orderInfo, response.data.data)
      selectedPaymentMethod.value = orderInfo.payment_method
    } else {
      ElMessage.error('获取订单详情失败')
      router.push('/')
    }
  } catch (error) {
    console.error('获取订单详情失败:', error)
    ElMessage.error('获取订单详情失败')
    router.push('/')
  }
}

// 更新支付方式
const updatePaymentMethod = async (method) => {
  try {
    const token = localStorage.getItem('token')
    await axios.put(`/api/v1/payments/orders/${orderInfo.id}`, {
      payment_method: method
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    orderInfo.payment_method = method
    ElMessage.success('支付方式已更新')
  } catch (error) {
    console.error('更新支付方式失败:', error)
    ElMessage.error('更新支付方式失败')
  }
}

// 处理支付
const handlePayment = async () => {
  if (remainingTime.value <= 0) {
    ElMessage.error('支付已超时')
    return
  }

  showQrCode.value = true
  ElMessage.info('请在10分钟内完成支付')
}

// 模拟支付
const simulatePayment = async () => {
  try {
    isProcessing.value = true
    
    // 模拟支付请求
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 调用支付API
    const token = localStorage.getItem('token')
    const response = await axios.post(`/api/v1/payments/orders/${orderId.value}/pay`, {
      payment_method: selectedPaymentMethod.value
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.data && response.data.success) {
      orderInfo.payment_status = 1 // 支付成功
      
      // 清除localStorage中的倒计时
      localStorage.removeItem(getCountdownKey())
      
      showSuccessDialog.value = true
      showQrCode.value = false
    } else {
      throw new Error(response.data?.message || '支付失败')
    }
  } catch (error) {
    console.error('支付失败:', error)
    failureMessage.value = error.response?.data?.message || error.message
    showFailureDialog.value = true
    showQrCode.value = false
  } finally {
    isProcessing.value = false
  }
}

// 取消支付
const handleCancel = async () => {
  try {
    await ElMessageBox.confirm('确定要取消支付吗？订单将被取消', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const token = localStorage.getItem('token')
    await axios.put(`/api/v1/payments/orders/${orderId.value}`, {
      payment_status: 2 // 取消支付
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    // 清除localStorage中的倒计时
    localStorage.removeItem(getCountdownKey())
    
    ElMessage.success('支付已取消')
    router.back()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消支付失败:', error)
      ElMessage.error('取消支付失败')
    }
  }
}

// 重新支付
const handleRetry = () => {
  showFailureDialog.value = false
  remainingTime.value = 600 // 重置倒计时
  startCountdown()
}

// 复制支付链接
const copyQrCode = () => {
  ElMessage.success('支付链接已复制到剪贴板')
}

// 返回上一页
const goBack = () => {
  showSuccessDialog.value = false
  router.back()
}

// 格式化金额
const formatAmount = (amount) => {
  return `¥${amount.toFixed(2)}`
}

// 格式化倒计时
const formatCountdown = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 获取支付方式文本
const getPaymentMethodText = (method) => {
  const methods = {
    1: '微信支付',
    2: '支付宝',
    3: '银行卡'
  }
  return methods[method] || '未知支付方式'
}

// 获取订单状态文本
const getOrderStatusText = (status) => {
  const statuses = {
    0: '待支付',
    1: '已支付',
    2: '已取消',
    3: '已退款'
  }
  return statuses[status] || '未知状态'
}

// 获取订单状态类型
const getOrderStatusType = (status) => {
  const types = {
    0: 'warning',
    1: 'success',
    2: 'danger',
    3: 'info'
  }
  return types[status] || 'info'
}

// 启动倒计时
const startCountdown = () => {
  // 清除之前的倒计时
  if (countdownTimer.value) {
    clearInterval(countdownTimer.value)
    countdownTimer.value = null
  }
  
  // 加载保存的倒计时数据
  loadCountdown()
  
  // 启动新的倒计时
  countdownTimer.value = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value--
      // 保存剩余时间到localStorage
      saveCountdown()
    } else {
      clearInterval(countdownTimer.value)
      countdownTimer.value = null
      // 清除localStorage中的倒计时
      localStorage.removeItem(getCountdownKey())
      handleTimeout()
    }
  }, 1000)
}

// 支付超时处理
const handleTimeout = () => {
  ElMessage.error('支付已超时，请重新下单')
  showQrCode.value = false
  // 自动取消订单
  setTimeout(async () => {
    try {
      const token = localStorage.getItem('token')
      await axios.put(`/api/v1/payments/orders/${orderId.value}`, {
        payment_status: 2 // 取消支付
      }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
    } catch (error) {
      console.error('自动取消订单失败:', error)
    }
  }, 1000)
}

// 检查并处理待创建的用户数据
const processPendingUserData = async () => {
  const pendingUserData = localStorage.getItem('pendingUserData')
  
  if (pendingUserData) {
    try {
      const userData = JSON.parse(pendingUserData)
      
      // 任何人都可以创建订单，直接调用注册接口
      const registerResponse = await axios.post('/api/v1/auth/register', userData, {
        headers: {
          'X-Admin-Create': 'false'
        }
      })
      
      if (registerResponse.data && registerResponse.data.success) {
        // 不清除pendingUserData，因为createOrder函数还需要从中获取用户需求信息
        return {
          userCreated: true,
          userId: registerResponse.data.data.user_id,
          username: registerResponse.data.data.username,
          isNewUser: true
        }
      }
    } catch (error) {
      console.error('用户创建失败:', error)
      // 即使用户创建失败，继续执行订单创建，但保留pendingUserData
      return {
        userCreated: false,
        isNewUser: false
      }
    }
  }
  
  return {
    userCreated: false,
    isNewUser: false
  }
}

// 创建新订单
const createOrder = async () => {
  try {
    // 先处理待创建的用户数据
    const processResult = await processPendingUserData()
    
    // 获取token（普通用户可能没有token）
    const token = localStorage.getItem('token')
    
    // 获取用户需求信息
    const pendingUserData = localStorage.getItem('pendingUserData')
    let userRequirements = null
    if (pendingUserData) {
      const userData = JSON.parse(pendingUserData)
      userRequirements = {
        username: userData.username,
        email: userData.email,
        phone: userData.phone,
        real_name: userData.real_name,
        gender: userData.gender,
        birthdate: userData.birthdate,
        kaoyan_requirements: userData.kaoyan_requirements,
        kaogong_requirements: userData.kaogong_requirements
      }
    }
    
    // 准备订单创建数据
    const orderData = {
      product_id: parseInt(productId.value),
      payment_method: parseInt(selectedPaymentMethod.value),
      user_requirements: userRequirements
    }
    
    // 如果是新创建的用户，传递user_id参数
    if (processResult.userCreated && processResult.userId) {
      orderData.user_id = processResult.userId
    }
    
    // 发送订单创建请求，不需要Authorization头
    const response = await axios.post('/api/v1/payments/orders', orderData)
    
    if (response.data && response.data.success) {
      Object.assign(orderInfo, response.data.data)
      const oldOrderId = orderId.value
      orderId.value = response.data.data.id // 更新订单ID
      
      // 订单创建成功后清除pendingUserData
    localStorage.removeItem('pendingUserData')
    
    // 如果之前有临时倒计时数据，迁移到新的订单ID下
    if (oldOrderId === 'temp') {
      const tempKey = `payment_countdown_temp`
      const savedTime = localStorage.getItem(tempKey)
      if (savedTime) {
        const newKey = `payment_countdown_${orderId.value}`
        localStorage.setItem(newKey, savedTime)
        localStorage.removeItem(tempKey)
      }
    }
    } else {
      throw new Error(response.data?.message || '创建订单失败')
    }
  } catch (error) {
    console.error('创建订单失败:', error)
    failureMessage.value = error.response?.data?.message || error.message
    showFailureDialog.value = true
  }
}

// 组件挂载时
onMounted(async () => {
  // 确保产品ID存在
  if (!productId.value) {
    ElMessage.error('缺少产品ID')
    router.push('/')
    return
  }
  
  // 先加载倒计时数据
  loadCountdown()
  
  if (orderId.value) {
    // 如果有订单ID，获取订单详情
    await getOrderDetail(orderId.value)
    startCountdown()
  } else {
    // 先设置临时订单ID
    orderId.value = 'temp'
    startCountdown()
    
    // 然后创建新订单
    await createOrder()
    
    // 订单创建成功后，重新启动倒计时
    startCountdown()
  }
})

// 组件卸载时
onBeforeUnmount(() => {
  if (countdownTimer.value) {
    clearInterval(countdownTimer.value)
  }
})
</script>

<style scoped>
.payment-container {
  min-height: 100vh;
  padding: 20px;
  background-color: #f5f7fa;
}

.payment-card {
  max-width: 900px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.countdown {
  flex: 1;
  margin-left: 20px;
}

.payment-content {
  margin-top: 20px;
}

.order-info-card,
.payment-method-card,
.qr-code-card {
  margin-bottom: 20px;
}

.order-details {
  padding: 10px 0;
}

.info-item {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.label {
  font-weight: bold;
  color: #666;
  width: 80px;
}

.value {
  color: #333;
}

.amount {
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
}

.payment-option {
  display: flex;
  align-items: center;
  padding: 10px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.payment-option:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
}

.payment-icon {
  margin-right: 8px;
  font-size: 20px;
}

.qr-code-container {
  text-align: center;
  padding: 20px;
}

.qr-code-placeholder {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 20px;
}

.qr-code-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.payment-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.success-content,
.failure-content {
  text-align: center;
  padding: 20px;
}

.success-text p,
.failure-text p {
  margin: 5px 0;
}

.payment-icon {
  margin-right: 8px;
  font-size: 20px;
}
</style>
