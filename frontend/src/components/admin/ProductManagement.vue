<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">产品管理</h3>
          <el-button type="primary" class="add-user-btn" @click="showAddProductDialog = true">添加产品</el-button>
          <el-button type="danger" class="delete-all-btn" @click="handleDeleteAll">全部删除</el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="productSearchQuery"
              placeholder="搜索产品"
              clearable
              prefix-icon="Search"
              @keyup.enter="getProducts"
            >
              <template #append>
                <el-button type="primary" @click="getProducts">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="8">
            <el-select v-model="productTypeFilter" placeholder="按产品类型筛选" clearable @change="getProducts">
              <el-option label="全部" value="" />
              <el-option label="考研VIP" value="1" />
              <el-option label="考公VIP" value="2" />
              <el-option label="双赛道VIP" value="3" />
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-select v-model="productStatusFilter" placeholder="按状态筛选" clearable @change="getProducts">
              <el-option label="全部" value="" />
              <el-option label="上架" value="1" />
              <el-option label="下架" value="0" />
            </el-select>
          </el-col>
        </el-row>
      </div>
      
      <!-- 产品表格 -->
      <el-table :data="products" style="width: 100%" v-loading="productsLoading">
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="name" label="产品名称" />
        <el-table-column prop="price" label="价格" width="100" />
        <el-table-column prop="original_price" label="原价" width="100" />
        <el-table-column prop="type_text" label="产品类型" width="120">
          <template #default="scope">
            <el-tag
              :type="scope.row.type === 1 ? 'primary' : scope.row.type === 2 ? 'success' : 'warning'"
            >
              {{ scope.row.type_text }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="有效期(天)" width="100" />
        <el-table-column prop="status_text" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="Number(scope.row.status) === 1 ? 'success' : 'danger'">
              {{ scope.row.status_text }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="250">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editProduct(scope.row.id)">编辑</el-button>
            <el-button :type="Number(scope.row.status) == 1 ? 'warning' : 'success'" size="small" @click="toggleProductStatus(scope.row.id, scope.row.status)">{{ Number(scope.row.status) == 1 ? '下架' : '上架' }}</el-button>
            <el-button type="danger" size="small" @click="handleDeleteProduct(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加产品对话框 -->
    <el-dialog
      v-model="showAddProductDialog"
      title="添加产品"
      width="600px"
    >
      <el-form :model="productForm" label-width="100px">
        <el-form-item label="产品名称" required>
          <el-input v-model="productForm.name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="产品描述">
          <el-input v-model="productForm.description" type="textarea" placeholder="请输入产品描述" />
        </el-form-item>
        <el-form-item label="价格" required>
          <el-input v-model="productForm.price" type="number" placeholder="请输入价格" />
        </el-form-item>
        <el-form-item label="原价">
          <el-input v-model="productForm.original_price" type="number" placeholder="请输入原价" />
        </el-form-item>
        <el-form-item label="产品类型" required>
          <el-select v-model="productForm.type" placeholder="请选择产品类型">
            <el-option label="考研VIP" value="1" />
            <el-option label="考公VIP" value="2" />
            <el-option label="双赛道VIP" value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="有效期(天)" required>
          <el-input v-model="productForm.duration" type="number" placeholder="请输入有效期" />
        </el-form-item>
        <el-form-item label="状态" required>
          <el-select v-model="productForm.status" placeholder="请选择状态">
            <el-option label="上架" value="1" />
            <el-option label="下架" value="0" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddProductDialog = false">取消</el-button>
          <el-button type="primary" @click="saveProduct">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑产品对话框 -->
    <el-dialog
      v-model="showEditProductDialog"
      title="编辑产品"
      width="600px"
    >
      <el-form :model="productForm" label-width="100px">
        <el-form-item label="产品名称" required>
          <el-input v-model="productForm.name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="产品描述">
          <el-input v-model="productForm.description" type="textarea" placeholder="请输入产品描述" />
        </el-form-item>
        <el-form-item label="价格" required>
          <el-input v-model="productForm.price" type="number" placeholder="请输入价格" />
        </el-form-item>
        <el-form-item label="原价">
          <el-input v-model="productForm.original_price" type="number" placeholder="请输入原价" />
        </el-form-item>
        <el-form-item label="产品类型" required>
          <el-select v-model="productForm.type" placeholder="请选择产品类型">
            <el-option label="考研VIP" value="1" />
            <el-option label="考公VIP" value="2" />
            <el-option label="双赛道VIP" value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="有效期(天)" required>
          <el-input v-model="productForm.duration" type="number" placeholder="请输入有效期" />
        </el-form-item>
        <el-form-item label="状态" required>
          <el-select v-model="productForm.status" placeholder="请选择状态">
            <el-option label="上架" value="1" />
            <el-option label="下架" value="0" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditProductDialog = false">取消</el-button>
          <el-button type="primary" @click="saveProduct">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

// 产品管理相关
const products = ref([])
const productsLoading = ref(false)
const productSearchQuery = ref('')
const productTypeFilter = ref('')
const productStatusFilter = ref('')
const showAddProductDialog = ref(false)
const showEditProductDialog = ref(false)
const currentProduct = ref(null)
const productForm = reactive({
  name: '',
  description: '',
  price: 0,
  original_price: 0,
  type: 1,
  duration: 30,
  features: [],
  status: 1
})

// 产品管理方法
const getProducts = async () => {
  try {
    productsLoading.value = true
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/admin/products', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        keyword: productSearchQuery.value || undefined,
        type: productTypeFilter.value || undefined,
        status: productStatusFilter.value || undefined
      }
    })
    // 处理产品类型和状态的文本显示
    products.value = response.data.map(product => {
      return {
        ...product,
        type_text: product.type == 1 ? '考研VIP' : product.type == 2 ? '考公VIP' : '双赛道VIP',
        status_text: product.status == 1 ? '上架' : '下架'
      }
    })
  } catch (error) {
    console.error('获取产品列表失败:', error)
    if (error.response) {
      console.error('Error response:', error.response.data)
      console.error('Error status:', error.response.status)
    }
  } finally {
    productsLoading.value = false
  }
}

const editProduct = async (productId) => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`/api/v1/admin/products/${productId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    currentProduct.value = response.data
    // 填充表单数据
    productForm.name = currentProduct.value.name
    productForm.description = currentProduct.value.description
    productForm.price = currentProduct.value.price
    productForm.original_price = currentProduct.value.original_price
    productForm.type = currentProduct.value.type
    productForm.duration = currentProduct.value.duration
    productForm.features = currentProduct.value.features || []
    productForm.status = currentProduct.value.status
    
    showEditProductDialog.value = true
  } catch (error) {
    console.error('获取产品信息失败:', error)
    ElMessage.error('获取产品信息失败，请稍后重试')
  }
}

const saveProduct = async () => {
  try {
    const token = localStorage.getItem('token')
    let response
    
    if (currentProduct.value) {
      // 更新产品
      response = await axios.put(`/api/v1/admin/products/${currentProduct.value.id}`, productForm, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      ElMessage.success('产品更新成功')
      showEditProductDialog.value = false
    } else {
      // 创建产品
      response = await axios.post('/api/v1/admin/products', productForm, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      ElMessage.success('产品创建成功')
      showAddProductDialog.value = false
    }
    
    // 刷新产品列表
    getProducts()
  } catch (error) {
    console.error('保存产品失败:', error)
    ElMessage.error('保存产品失败，请稍后重试')
  }
}

const handleDeleteProduct = async (productId) => {
  try {
    await ElMessageBox.confirm('确定要删除该产品吗？', '提示', {
      type: 'warning',
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    
    const token = localStorage.getItem('token')
    await axios.delete(`/api/v1/admin/products/${productId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    ElMessage.success('产品删除成功')
    // 刷新产品列表
    getProducts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除产品失败:', error)
      ElMessage.error('删除产品失败，请稍后重试')
    }
  }
}

const handleDeleteAll = async () => {
  try {
    await ElMessageBox.confirm('确定要删除所有产品吗？此操作不可恢复！', '警告', {
      type: 'danger',
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    
    const token = localStorage.getItem('token')
    await axios.delete('/api/v1/admin/products', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    ElMessage.success('所有产品删除成功')
    // 刷新产品列表
    getProducts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除所有产品失败:', error)
      ElMessage.error('删除所有产品失败，请稍后重试')
    }
  }
}

// 切换产品上下架状态
const toggleProductStatus = async (productId, currentStatus) => {
  try {
    const token = localStorage.getItem('token')
    // 计算新状态：1 -> 0, 0 -> 1
    const newStatus = currentStatus == 1 ? 0 : 1
    
    const response = await axios.put(`/api/v1/admin/products/${productId}`, {
      status: newStatus
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    ElMessage.success(`产品已${newStatus == 1 ? '上架' : '下架'}`)
    // 刷新产品列表
    getProducts()
  } catch (error) {
    console.error('切换产品状态失败:', error)
    ElMessage.error('切换产品状态失败，请稍后重试')
  }
}

onMounted(() => {
  getProducts()
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