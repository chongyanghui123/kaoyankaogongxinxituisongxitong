<template>
  <div class="gift-management">
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span>礼品管理</span>
          <el-button type="primary" @click="handleAdd">添加礼品</el-button>
        </div>
      </template>

      <el-table :data="gifts" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="礼品名称" width="150" />
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="points_required" label="所需积分" width="100" />
        <el-table-column prop="stock" label="库存" width="80" />
        <el-table-column prop="exchanged_count" label="已兑换" width="80" />
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">
              {{ row.is_active ? '上架' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
        class="pagination"
      />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑礼品' : '添加礼品'" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="礼品名称">
          <el-input v-model="form.name" placeholder="请输入礼品名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" rows="3" placeholder="请输入礼品描述" />
        </el-form-item>
        <el-form-item label="礼品图片">
          <el-upload
            class="image-uploader"
            :show-file-list="false"
            :before-upload="beforeImageUpload"
            :http-request="handleImageUpload"
          >
            <img v-if="form.image_url" :src="getImageUrl(form.image_url)" class="image-preview" />
            <el-icon v-else class="image-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="所需积分">
          <el-input-number v-model="form.points_required" :min="1" />
        </el-form-item>
        <el-form-item label="库存">
          <el-input-number v-model="form.stock" :min="0" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="是否上架">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-card class="exchange-card">
      <template #header>
        <span>兑换记录</span>
      </template>

      <el-form :inline="true" class="search-form">
        <el-form-item label="状态">
          <el-select v-model="exchangeSearch.status" placeholder="全部" clearable>
            <el-option label="待处理" :value="0" />
            <el-option label="已发货" :value="1" />
            <el-option label="已完成" :value="2" />
            <el-option label="已取消" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadExchanges">搜索</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="exchanges" v-loading="exchangeLoading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户" width="120" />
        <el-table-column prop="gift_name" label="礼品" width="150" />
        <el-table-column prop="points_used" label="使用积分" width="100" />
        <el-table-column prop="status_name" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status_name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="tracking_number" label="快递单号" width="150" />
        <el-table-column prop="created_at" label="兑换时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleUpdateExchange(row)">处理</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="exchangePagination.page"
        v-model:page-size="exchangePagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        :total="exchangePagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleExchangeSizeChange"
        @current-change="handleExchangePageChange"
        class="pagination"
      />
    </el-card>

    <el-dialog v-model="exchangeDialogVisible" title="处理兑换" width="400px">
      <el-form :model="exchangeForm" label-width="100px">
        <el-form-item label="状态">
          <el-select v-model="exchangeForm.status">
            <el-option label="待处理" :value="0" />
            <el-option label="已发货" :value="1" />
            <el-option label="已完成" :value="2" />
            <el-option label="已取消" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="快递单号">
          <el-input v-model="exchangeForm.tracking_number" placeholder="请输入快递单号" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="exchangeForm.remark" type="textarea" rows="2" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="exchangeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitExchange">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from '@/utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const loading = ref(false)
const exchangeLoading = ref(false)
const gifts = ref([])
const exchanges = ref([])
const dialogVisible = ref(false)
const exchangeDialogVisible = ref(false)
const isEdit = ref(false)
const imageFile = ref(null)

const form = reactive({
  id: null,
  name: '',
  description: '',
  image_url: '',
  points_required: 100,
  stock: 0,
  is_active: true,
  sort_order: 0
})

const exchangeForm = reactive({
  id: null,
  status: 0,
  tracking_number: '',
  remark: ''
})

const exchangeSearch = reactive({
  status: null
})

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

const exchangePagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

const formatTime = (time) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

const getStatusType = (status) => {
  const types = { 0: 'warning', 1: 'primary', 2: 'success', 3: 'info' }
  return types[status] || 'info'
}

const loadGifts = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/admin/gifts', {
      params: {
        page: pagination.page,
        page_size: pagination.page_size
      },
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.data.success) {
      gifts.value = response.data.data.items
      pagination.total = response.data.data.total
    }
  } catch (error) {
    console.error('获取礼品列表失败:', error)
    ElMessage.error('获取礼品列表失败')
  } finally {
    loading.value = false
  }
}

const loadExchanges = async () => {
  exchangeLoading.value = true
  try {
    const token = localStorage.getItem('token')
    const params = {
      page: exchangePagination.page,
      page_size: exchangePagination.page_size
    }
    if (exchangeSearch.status !== null) {
      params.status = exchangeSearch.status
    }

    const response = await axios.get('/api/v1/admin/exchanges', {
      params,
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.data.success) {
      exchanges.value = response.data.data.items
      exchangePagination.total = response.data.data.total
    }
  } catch (error) {
    console.error('获取兑换记录失败:', error)
    ElMessage.error('获取兑换记录失败')
  } finally {
    exchangeLoading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  imageFile.value = null
  Object.assign(form, {
    id: null,
    name: '',
    description: '',
    image_url: '',
    points_required: 100,
    stock: 0,
    is_active: true,
    sort_order: 0
  })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  imageFile.value = null
  Object.assign(form, row)
  dialogVisible.value = true
}

const beforeImageUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

const handleImageUpload = (options) => {
  imageFile.value = options.file
  const reader = new FileReader()
  reader.onload = (e) => {
    form.image_url = e.target.result
  }
  reader.readAsDataURL(options.file)
}

const getImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('data:') || url.startsWith('http')) return url
  return `http://localhost:8000${url}`
}

const handleSubmit = async () => {
  try {
    const token = localStorage.getItem('token')
    const url = isEdit.value ? `/api/v1/admin/gifts/${form.id}` : '/api/v1/admin/gifts'
    const method = isEdit.value ? 'put' : 'post'

    const formData = new FormData()
    formData.append('name', form.name)
    formData.append('description', form.description || '')
    formData.append('points_required', form.points_required)
    formData.append('stock', form.stock)
    formData.append('is_active', form.is_active)
    formData.append('sort_order', form.sort_order)
    
    if (imageFile.value) {
      formData.append('image', imageFile.value)
    }

    const response = await axios[method](url, formData, {
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })

    if (response.data.success) {
      ElMessage.success(isEdit.value ? '更新成功' : '添加成功')
      dialogVisible.value = false
      loadGifts()
    } else {
      ElMessage.error(response.data.message || '操作失败')
    }
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该礼品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const token = localStorage.getItem('token')
    const response = await axios.delete(`/api/v1/admin/gifts/${row.id}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.data.success) {
      ElMessage.success('删除成功')
      loadGifts()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleUpdateExchange = (row) => {
  Object.assign(exchangeForm, {
    id: row.id,
    status: row.status,
    tracking_number: row.tracking_number || '',
    remark: row.remark || ''
  })
  exchangeDialogVisible.value = true
}

const handleSubmitExchange = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.put(`/api/v1/admin/exchanges/${exchangeForm.id}`, exchangeForm, {
      headers: { 'Authorization': `Bearer ${token}` }
    })

    if (response.data.success) {
      ElMessage.success('更新成功')
      exchangeDialogVisible.value = false
      loadExchanges()
    }
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error('更新失败')
  }
}

const handleSizeChange = () => {
  pagination.page = 1
  loadGifts()
}

const handlePageChange = () => {
  loadGifts()
}

const handleExchangeSizeChange = () => {
  exchangePagination.page = 1
  loadExchanges()
}

const handleExchangePageChange = () => {
  loadExchanges()
}

onMounted(() => {
  loadGifts()
  loadExchanges()
})
</script>

<style scoped>
.gift-management {
  padding: 20px;
}

.table-card, .exchange-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.image-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 120px;
  height: 120px;
}

.image-uploader:hover {
  border-color: #409eff;
}

.image-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-preview {
  width: 120px;
  height: 120px;
  display: block;
  object-fit: cover;
}
</style>
