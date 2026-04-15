<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">支付管理</h3>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="orderSearchQuery"
              placeholder="搜索订单号"
              clearable
              prefix-icon="Search"
              @keyup.enter="getOrders"
            >
              <template #append>
                <el-button type="primary" @click="getOrders">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="8">
            <el-select v-model="orderStatusFilter" placeholder="按订单状态筛选" clearable @change="getOrders">
              <el-option label="全部" value="" />
              <el-option label="待支付" value="pending" />
              <el-option label="已完成" value="completed" />
              <el-option label="已取消" value="cancelled" />
              <el-option label="已失败" value="failed" />
            </el-select>
          </el-col>
          <el-col :span="8">
            <div class="flex justify-between items-center">
              <el-input
                v-model="userIdFilter"
                placeholder="按用户ID搜索"
                clearable
                prefix-icon="User"
                @keyup.enter="getOrders"
                style="width: 70%"
              >
                <template #append>
                  <el-button type="primary" @click="getOrders">搜索</el-button>
                </template>
              </el-input>
              <el-button type="danger" @click="confirmDeleteAll">全部删除</el-button>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <!-- 订单表格 -->
      <el-table :data="orders" style="width: 100%" v-loading="ordersLoading">
        <el-table-column type="index" label="序号" width="100" :index="(index) => index + 1" />
        <el-table-column prop="order_no" label="订单号" width="200" />
        <el-table-column prop="user_name" label="用户" width="150" />
        <el-table-column prop="product_name" label="产品" width="150" />
        <el-table-column prop="amount" label="订单金额" width="120">
          <template #default="scope">
            {{ scope.row.amount.toFixed(2) }} 元
          </template>
        </el-table-column>
        <el-table-column prop="status" label="订单状态" width="120">
          <template #default="scope">
            <el-tag
              :type="getOrderStatusType(scope.row.status)"
            >
              {{ getOrderStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="payment_method" label="支付方式" width="120" />

        <el-table-column prop="paid_at" label="支付时间" width="180" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="300">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewOrderDetail(scope.row)">查看详情</el-button>
            <el-button type="warning" size="small" @click="updateOrderStatus(scope.row)">更新状态</el-button>
            <el-button type="danger" size="small" @click="confirmDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
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
    </el-card>

    <!-- 订单详情对话框 -->
    <el-dialog
      v-model="showOrderDetailDialog"
      title="订单详情"
      width="800px"
    >
      <el-form :model="currentOrder" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="订单ID">
              {{ currentOrder.id }}
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="用户">
              {{ currentOrder.user_name || `用户${currentOrder.user_id}` }}
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="产品">
              {{ currentOrder.product_name }}
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="订单金额">
              {{ currentOrder.amount ? currentOrder.amount.toFixed(2) : '0.00' }} 元
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="订单状态">
              <el-tag
                :type="getOrderStatusType(currentOrder.status)"
              >
                {{ getOrderStatusText(currentOrder.status) }}
              </el-tag>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="支付方式">
              {{ currentOrder.payment_method || '未选择' }}
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="支付时间">
              {{ currentOrder.paid_at || '未支付' }}
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="创建时间">
              {{ currentOrder.created_at }}
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="更新时间">
              {{ currentOrder.updated_at }}
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showOrderDetailDialog = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 更新订单状态对话框 -->
    <el-dialog
      v-model="showUpdateStatusDialog"
      title="更新订单状态"
      width="400px"
    >
      <el-form :model="statusForm" label-width="100px">
        <el-form-item label="订单状态" required>
          <el-select v-model="statusForm.status" placeholder="请选择新状态">
            <el-option label="待支付" value="pending" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
            <el-option label="已失败" value="failed" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="statusForm.remark" type="textarea" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showUpdateStatusDialog = false">取消</el-button>
          <el-button type="primary" @click="saveOrderStatus">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

// 订单管理相关
const orders = ref([])
const ordersLoading = ref(false)
const orderSearchQuery = ref('')
const orderStatusFilter = ref('')
const userIdFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const showOrderDetailDialog = ref(false)
const showUpdateStatusDialog = ref(false)
const currentOrder = ref(null)
const statusForm = reactive({
  status: '',
  remark: ''
})

// 状态映射：前端字符串 -> 后端整数
const statusMap = {
  'pending': 0,
  'completed': 1,
  'cancelled': 2,
  'failed': 3
}

// 反向状态映射：后端整数 -> 前端字符串
const reverseStatusMap = {
  0: 'pending',
  1: 'completed',
  2: 'cancelled',
  3: 'failed'
}

// 支付方式映射：后端整数 -> 前端文本
const paymentMethodMap = {
  1: '微信支付',
  2: '支付宝'
}

// 用户信息映射
const usersMap = ref({})

// 产品信息映射
const productsMap = ref({})

// 获取订单列表
const getOrders = async () => {
  try {
    ordersLoading.value = true
    const token = localStorage.getItem('token')
    
    // 构建参数
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }
    
    // 添加关键词搜索（订单号、用户名、邮箱）
    if (orderSearchQuery.value) {
      params.keyword = orderSearchQuery.value
    }
    
    // 添加状态筛选
    if (orderStatusFilter.value) {
      params.payment_status = statusMap[orderStatusFilter.value]
    }
    
    // 添加用户ID筛选
    if (userIdFilter.value) {
      const userId = parseInt(userIdFilter.value)
      if (!isNaN(userId)) {
        params.user_id = userId
      }
    }
    
    const response = await axios.get('/api/v1/admin/orders', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params
    })
    
    // 转换订单数据结构
    orders.value = response.data.data.map(order => ({
      ...order,
      amount: order.total_amount, // 前端使用amount，后端返回total_amount
      status: reverseStatusMap[order.payment_status], // 转换状态为前端格式
      payment_method: paymentMethodMap[order.payment_method] || '未知', // 转换支付方式为文本
      paid_at: order.payment_time, // 前端使用paid_at，后端返回payment_time
      user_name: order.username || `用户${order.user_id}`,
      product_name: order.product_name || `产品${order.product_id}`
    }))
    
    // 加载用户和产品信息
    await loadUsersAndProducts(response.data.data)
    
    // 更新订单数据中的用户和产品名称
    orders.value = orders.value.map(order => ({
      ...order,
      user_name: usersMap.value[order.user_id] || `用户${order.user_id}`,
      product_name: order.product_name || `产品${order.product_id}`
    }))
    
    // 从API返回的total字段获取总数
    total.value = response.data.total
  } catch (error) {
    console.error('获取订单列表失败:', error)
    if (error.response) {
      console.error('Error response:', error.response.data)
      console.error('Error status:', error.response.status)
    }
  } finally {
    ordersLoading.value = false
  }
}

// 查看订单详情
const viewOrderDetail = (order) => {
  currentOrder.value = order
  showOrderDetailDialog.value = true
}

// 更新订单状态
const updateOrderStatus = (order) => {
  currentOrder.value = order
  statusForm.status = order.status
  statusForm.remark = ''
  showUpdateStatusDialog.value = true
}

// 保存订单状态
const saveOrderStatus = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.put(`/api/v1/payments/admin/orders/${currentOrder.value.id}`, {
      payment_status: statusMap[statusForm.status]
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    ElMessage.success('订单状态更新成功')
    showUpdateStatusDialog.value = false
    getOrders()
  } catch (error) {
    console.error('更新订单状态失败:', error)
    ElMessage.error('更新订单状态失败，请稍后重试')
  }
}

// 确认删除订单
const confirmDelete = (order) => {
  ElMessageBox.confirm(
    `确定要删除订单 ${order.id} 吗？`,
    '删除订单',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    await deleteOrder(order.id)
  }).catch(() => {
    // 取消删除
  })
}

// 删除订单
const deleteOrder = async (orderId) => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`/api/v1/payments/admin/orders/${orderId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    ElMessage.success('订单删除成功')
    getOrders()
  } catch (error) {
    console.error('删除订单失败:', error)
    ElMessage.error('删除订单失败，请稍后重试')
  }
}

// 确认全部删除
const confirmDeleteAll = () => {
  ElMessageBox.confirm(
    '确定要删除所有订单吗？此操作不可恢复！',
    '删除所有订单',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'danger'
    }
  ).then(async () => {
    await deleteAllOrders()
  }).catch(() => {
    // 取消删除
  })
}

// 删除所有订单
const deleteAllOrders = async () => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete('/api/v1/payments/admin/orders', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    ElMessage.success('所有订单删除成功')
    getOrders()
  } catch (error) {
    console.error('删除所有订单失败:', error)
    ElMessage.error('删除所有订单失败，请稍后重试')
  }
}

// 获取用户信息
const getUserInfo = async (userId) => {
  if (usersMap.value[userId]) {
    return usersMap.value[userId]
  }
  
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`/api/v1/users/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.data && response.data.success) {
      const userInfo = response.data.data
      usersMap.value[userId] = userInfo.username || `用户${userId}`
      return usersMap.value[userId]
    }
  } catch (error) {
    console.error(`获取用户 ${userId} 信息失败:`, error)
  }
  
  usersMap.value[userId] = `用户${userId}`
  return usersMap.value[userId]
}

// 获取产品信息
const getProductInfo = async (productId) => {
  if (productsMap.value[productId]) {
    return productsMap.value[productId]
  }
  
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`/api/v1/payments/products/${productId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.data) {
      productsMap.value[productId] = response.data.name || `产品${productId}`
      return productsMap.value[productId]
    }
  } catch (error) {
    console.error(`获取产品 ${productId} 信息失败:`, error)
  }
  
  productsMap.value[productId] = `产品${productId}`
  return productsMap.value[productId]
}

// 加载用户和产品信息
const loadUsersAndProducts = async (orders) => {
  const userIds = [...new Set(orders.map(order => order.user_id))]
  const productIds = [...new Set(orders.map(order => order.product_id))]
  
  // 并行获取用户信息
  await Promise.all(userIds.map(getUserInfo))
  
  // 并行获取产品信息
  await Promise.all(productIds.map(getProductInfo))
}

// 订单状态类型映射
const getOrderStatusType = (status) => {
  const statusMap = {
    'pending': 'warning',
    'completed': 'success',
    'cancelled': 'danger',
    'failed': 'danger'
  }
  return statusMap[status] || 'info'
}

// 订单状态文本映射
const getOrderStatusText = (status) => {
  const statusMap = {
    'pending': '待支付',
    'completed': '已完成',
    'cancelled': '已取消',
    'failed': '已失败'
  }
  return statusMap[status] || '未知状态'
}

// 分页事件处理
const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  getOrders()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  getOrders()
}

onMounted(() => {
  getOrders()
})
</script>

<style scoped>
.admin-content {
  padding: 20px;
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
  font-weight: 500;
}

.search-filter {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
