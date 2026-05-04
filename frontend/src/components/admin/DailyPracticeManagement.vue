<template>
  <div class="daily-practice-management">
    <div class="page-header">
      <h2>每日一练管理</h2>
      <el-button type="primary" @click="showAddDialog">
        <el-icon><Plus /></el-icon>
        添加题目
      </el-button>
    </div>

    <div class="filter-bar">
      <el-select v-model="filterCategory" placeholder="选择分类" clearable @change="loadPractices" style="width: 150px;">
        <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat" />
      </el-select>
      <el-select v-model="filterActive" placeholder="状态" clearable @change="loadPractices" style="width: 120px;">
        <el-option label="启用" :value="true" />
        <el-option label="禁用" :value="false" />
      </el-select>
    </div>

    <el-table :data="practices" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="category" label="分类" width="100">
        <template #default="{ row }">
          <el-tag>{{ row.category }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="question" label="题目" min-width="300">
        <template #default="{ row }">
          <div class="question-cell">{{ row.question }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="answer" label="答案" width="80" />
      <el-table-column prop="difficulty" label="难度" width="100">
        <template #default="{ row }">
          <el-rate v-model="row.difficulty" disabled :max="3" />
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">
            {{ row.is_active ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="showEditDialog(row)">编辑</el-button>
          <el-button type="danger" link @click="deletePractice(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="loadPractices"
        @current-change="loadPractices"
      />
    </div>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑题目' : '添加题目'" width="600px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="分类">
          <el-select v-model="form.category" placeholder="选择分类" allow-create filterable>
            <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat" />
          </el-select>
        </el-form-item>
        <el-form-item label="题目">
          <el-input v-model="form.question" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="选项">
          <div class="options-editor">
            <div v-for="(opt, index) in optionsList" :key="index" class="option-item">
              <el-input v-model="opt.label" placeholder="A/B/C/D" style="width: 60px;" />
              <el-input v-model="opt.text" placeholder="选项内容" style="flex: 1;" />
              <el-button type="danger" link @click="removeOption(index)">删除</el-button>
            </div>
            <el-button type="primary" link @click="addOption">+ 添加选项</el-button>
          </div>
        </el-form-item>
        <el-form-item label="正确答案">
          <el-input v-model="form.answer" placeholder="A/B/C/D" style="width: 100px;" />
        </el-form-item>
        <el-form-item label="解析">
          <el-input v-model="form.analysis" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="难度">
          <el-rate v-model="form.difficulty" :max="3" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.is_active" active-text="启用" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePractice">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from '../../utils/axios'

const practices = ref([])
const categories = ref(['行测', '申论', '考研英语', '考研政治', '考研数学'])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const filterCategory = ref('')
const filterActive = ref(null)

const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)

const form = reactive({
  category: '',
  question: '',
  answer: '',
  analysis: '',
  difficulty: 1,
  is_active: true
})

const optionsList = ref([
  { label: 'A', text: '' },
  { label: 'B', text: '' },
  { label: 'C', text: '' },
  { label: 'D', text: '' }
])

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('zh-CN')
}

const loadPractices = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (filterCategory.value) params.category = filterCategory.value
    if (filterActive.value !== null) params.is_active = filterActive.value

    const res = await axios.get('/api/v1/admin/daily-practices', { params })
    console.log('API响应:', res)
    // axios拦截器已返回response.data，后端数据结构是 { success, code, message, data, total }
    practices.value = res.data || []
    total.value = res.total || 0
  } catch (error) {
    console.error('加载失败:', error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const res = await axios.get('/api/v1/admin/daily-practices/categories')
    if (res.data && res.data.length > 0) {
      categories.value = [...new Set([...categories.value, ...res.data])]
    }
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

const showAddDialog = () => {
  isEdit.value = false
  editId.value = null
  Object.assign(form, {
    category: '',
    question: '',
    answer: '',
    analysis: '',
    difficulty: 1,
    is_active: true
  })
  optionsList.value = [
    { label: 'A', text: '' },
    { label: 'B', text: '' },
    { label: 'C', text: '' },
    { label: 'D', text: '' }
  ]
  dialogVisible.value = true
}

const showEditDialog = (row) => {
  isEdit.value = true
  editId.value = row.id
  Object.assign(form, {
    category: row.category,
    question: row.question,
    answer: row.answer,
    analysis: row.analysis || '',
    difficulty: row.difficulty,
    is_active: row.is_active
  })
  try {
    optionsList.value = JSON.parse(row.options)
  } catch {
    optionsList.value = [
      { label: 'A', text: '' },
      { label: 'B', text: '' },
      { label: 'C', text: '' },
      { label: 'D', text: '' }
    ]
  }
  dialogVisible.value = true
}

const addOption = () => {
  const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
  const nextLabel = labels[optionsList.value.length] || String(optionsList.value.length + 1)
  optionsList.value.push({ label: nextLabel, text: '' })
}

const removeOption = (index) => {
  optionsList.value.splice(index, 1)
}

const savePractice = async () => {
  if (!form.category || !form.question || !form.answer) {
    ElMessage.warning('请填写完整信息')
    return
  }

  const optionsJson = JSON.stringify(optionsList.value.filter(o => o.text))

  try {
    const data = {
      ...form,
      options: optionsJson
    }

    if (isEdit.value) {
      await axios.put(`/api/v1/admin/daily-practices/${editId.value}`, data)
      ElMessage.success('更新成功')
    } else {
      await axios.post('/api/v1/admin/daily-practices', data)
      ElMessage.success('添加成功')
    }

    dialogVisible.value = false
    loadPractices()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '保存失败')
  }
}

const deletePractice = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该题目吗？', '提示', { type: 'warning' })
    await axios.delete(`/api/v1/admin/daily-practices/${row.id}`)
    ElMessage.success('删除成功')
    loadPractices()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadPractices()
  loadCategories()
})
</script>

<style scoped>
.daily-practice-management {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.filter-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.question-cell {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.options-editor {
  width: 100%;
}

.option-item {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
}
</style>
