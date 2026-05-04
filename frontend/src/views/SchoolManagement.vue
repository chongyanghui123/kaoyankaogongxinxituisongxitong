<template>
  <div class="school-management">
    <el-card shadow="hover" class="mb-4">
      <template #header>
        <div class="flex justify-between items-center">
          <h3 class="text-xl font-bold">学校管理</h3>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>
            添加学校
          </el-button>
        </div>
      </template>
      
      <div class="mb-4">
        <el-form :inline="true" :model="searchForm" class="mb-4">
          <el-form-item label="省份">
            <el-select v-model="searchForm.province" placeholder="选择省份" clearable>
              <el-option
                v-for="province in provinces"
                :key="province"
                :label="province"
                :value="province"
              />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="search">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <el-table
        v-loading="loading"
        :data="schools.items"
        style="width: 100%"
        border
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="province" label="省份" width="120" />
        <el-table-column prop="name" label="学校名称" />

        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="openEditDialog(scope.row)"
              style="margin-right: 5px"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="deleteSchool(scope.row.id, scope.row.name)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="flex justify-between mt-4">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="schools.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 添加学校对话框 -->
    <el-dialog
      v-model="addDialogVisible"
      title="添加学校"
      width="500px"
    >
      <el-form :model="addForm" :rules="rules" ref="addFormRef" label-width="100px">
        <el-form-item label="省份" prop="province">
          <el-select v-model="addForm.province" placeholder="选择省份">
            <el-option
              v-for="province in provinces"
              :key="province"
              :label="province"
              :value="province"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="学校名称" prop="name">
          <el-input v-model="addForm.name" placeholder="输入学校名称" />
        </el-form-item>

      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAddForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 编辑学校对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑学校"
      width="500px"
    >
      <el-form :model="editForm" :rules="rules" ref="editFormRef" label-width="100px">
        <el-form-item label="省份" prop="province">
          <el-select v-model="editForm.province" placeholder="选择省份">
            <el-option
              v-for="province in provinces"
              :key="province"
              :label="province"
              :value="province"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="学校名称" prop="name">
          <el-input v-model="editForm.name" placeholder="输入学校名称" />
        </el-form-item>

      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEditForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from '@/utils/axios'

// 搜索表单
const searchForm = reactive({
  province: ''
})

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 20
})

// 加载状态
const loading = ref(false)

// 学校数据
const schools = ref({
  items: [],
  total: 0
})

// 省份列表
const provinces = ref([])

// 添加对话框
const addDialogVisible = ref(false)
const addForm = reactive({
  province: '',
  name: ''
})

// 编辑对话框
const editDialogVisible = ref(false)
const editForm = reactive({
  id: '',
  province: '',
  name: ''
})

// 表单验证规则
const rules = {
  province: [
    { required: true, message: '请选择省份', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入学校名称', trigger: 'blur' }
  ]
}

// 表单引用
const addFormRef = ref(null)
const editFormRef = ref(null)

// 获取省份列表
const getProvinces = async () => {
  try {
    const response = await axios.get('/api/v1/utils/provinces', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    if (response.success) {
      provinces.value = response.data
    }
  } catch (error) {
    console.error('获取省份列表失败:', error)
    ElMessage.error('获取省份列表失败')
  }
}

// 获取学校列表
const getSchools = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/v1/school-management/schools', {
      params: {
        province: searchForm.province,
        skip: (pagination.currentPage - 1) * pagination.pageSize,
        limit: pagination.pageSize
      },
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    if (response.success) {
      schools.value = response.data
    }
  } catch (error) {
    console.error('获取学校列表失败:', error)
    ElMessage.error('获取学校列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const search = () => {
  pagination.currentPage = 1
  getSchools()
}

// 重置搜索
const resetSearch = () => {
  searchForm.province = ''
  pagination.currentPage = 1
  getSchools()
}

// 分页处理
const handleSizeChange = (size) => {
  pagination.pageSize = size
  getSchools()
}

const handleCurrentChange = (current) => {
  pagination.currentPage = current
  getSchools()
}

// 打开添加对话框
const openAddDialog = () => {
  addForm.province = ''
  addForm.name = ''
  addDialogVisible.value = true
}

// 提交添加表单
const submitAddForm = async () => {
  if (!addFormRef.value) return
  await addFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await axios.post('/api/v1/school-management/schools', {
          province: addForm.province,
          name: addForm.name
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (response.success) {
          ElMessage.success('添加学校成功')
          addDialogVisible.value = false
          getSchools()
        } else {
          ElMessage.error(response.message || '添加学校失败')
        }
      } catch (error) {
        console.error('添加学校失败:', error)
        ElMessage.error('添加学校失败')
      }
    }
  })
}

// 打开编辑对话框
const openEditDialog = (row) => {
  editForm.id = row.id
  editForm.province = row.province
  editForm.name = row.name
  editDialogVisible.value = true
}

// 提交编辑表单
const submitEditForm = async () => {
  if (!editFormRef.value) return
  await editFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await axios.put(`/api/v1/school-management/schools/${editForm.id}`, {
          province: editForm.province,
          name: editForm.name
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        })
        if (response.success) {
          ElMessage.success('更新学校成功')
          editDialogVisible.value = false
          getSchools()
        } else {
          ElMessage.error(response.message || '更新学校失败')
        }
      } catch (error) {
        console.error('更新学校失败:', error)
        ElMessage.error('更新学校失败')
      }
    }
  })
}

// 删除学校
const deleteSchool = (id, name) => {
  ElMessageBox.confirm(
    `确定要删除学校「${name}」吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const response = await axios.delete(`/api/v1/school-management/schools/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.success) {
        ElMessage.success('删除学校成功')
        getSchools()
      } else {
        ElMessage.error(response.message || '删除学校失败')
      }
    } catch (error) {
      console.error('删除学校失败:', error)
      ElMessage.error('删除学校失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 初始化
onMounted(() => {
  getProvinces()
  getSchools()
})
</script>

<script>
import { ElMessageBox } from 'element-plus'

export default {
  name: 'SchoolManagement',
  components: {
    ElMessageBox
  }
}
</script>

<style scoped>
.school-management {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 20px;
}

.flex {
  display: flex;
}

.justify-between {
  justify-content: space-between;
}

.items-center {
  align-items: center;
}

.mt-4 {
  margin-top: 20px;
}

.text-xl {
  font-size: 20px;
}

.font-bold {
  font-weight: bold;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
</style>
