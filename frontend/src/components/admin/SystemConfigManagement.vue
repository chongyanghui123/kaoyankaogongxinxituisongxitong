<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">系统配置</h3>
          <el-button type="primary" class="add-user-btn" @click="showAddConfigDialog = true">添加配置</el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="configSearchQuery"
              placeholder="搜索配置键"
              clearable
              prefix-icon="Search"
              @keyup.enter="getSystemConfigs"
            >
              <template #append>
                <el-button type="primary" @click="getSystemConfigs">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="8">
            <el-select v-model="configTypeFilter" placeholder="按配置类型筛选" clearable @change="getSystemConfigs">
              <el-option label="全部" value="" />
              <el-option label="字符串" value="0" />
              <el-option label="数字" value="1" />
              <el-option label="布尔值" value="2" />
              <el-option label="JSON" value="3" />
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-select v-model="configStatusFilter" placeholder="按状态筛选" clearable @change="getSystemConfigs">
              <el-option label="全部" value="" />
              <el-option label="启用" value="1" />
              <el-option label="禁用" value="0" />
            </el-select>
          </el-col>
        </el-row>
      </div>
      
      <!-- 系统配置表格 -->
      <el-table :data="systemConfigs" style="width: 100%" v-loading="configsLoading">
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="config_key" label="配置键" />
        <el-table-column prop="config_value" label="配置值" />
        <el-table-column prop="config_type_text" label="配置类型" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.config_type === 0 ? 'info' : scope.row.config_type === 1 ? 'primary' : scope.row.config_type === 2 ? 'success' : 'warning'">
              {{ scope.row.config_type_text }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="配置描述" />
        <el-table-column prop="is_system_text" label="系统配置" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_system ? 'danger' : 'info'">
              {{ scope.row.is_system_text }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status_text" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
              {{ scope.row.status_text }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="80">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editConfig(scope.row.id)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加系统配置对话框 -->
    <el-dialog
      v-model="showAddConfigDialog"
      title="添加系统配置"
      width="600px"
    >
      <el-form :model="configForm" label-width="100px">
        <el-form-item label="配置键" required>
          <el-input v-model="configForm.key" placeholder="请输入配置键" />
        </el-form-item>
        <el-form-item label="配置值" required>
          <el-input v-model="configForm.value" type="textarea" placeholder="请输入配置值" />
        </el-form-item>
        <el-form-item label="配置描述">
          <el-input v-model="configForm.description" type="textarea" placeholder="请输入配置描述" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="configForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddConfigDialog = false">取消</el-button>
          <el-button type="primary" @click="saveConfig">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑系统配置对话框 -->
    <el-dialog
      v-model="showEditConfigDialog"
      title="编辑系统配置"
      width="600px"
    >
      <el-form :model="configForm" label-width="100px">
        <el-form-item label="配置键" required>
          <el-input v-model="configForm.key" placeholder="请输入配置键" />
        </el-form-item>
        <el-form-item label="配置值" required>
          <el-input v-model="configForm.value" type="textarea" placeholder="请输入配置值" />
        </el-form-item>
        <el-form-item label="配置描述">
          <el-input v-model="configForm.description" type="textarea" placeholder="请输入配置描述" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="configForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditConfigDialog = false">取消</el-button>
          <el-button type="primary" @click="saveConfig">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 系统配置相关
const systemConfigs = ref([])
const configsLoading = ref(false)
const configSearchQuery = ref('')
const configTypeFilter = ref('')
const configStatusFilter = ref('')
const showAddConfigDialog = ref(false)
const showEditConfigDialog = ref(false)
const currentConfig = ref(null)
const configForm = reactive({
  key: '',
  value: '',
  description: '',
  is_active: true
})

// 系统配置方法
const getSystemConfigs = async () => {
  try {
    configsLoading.value = true
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/admin/configs', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        is_active: configStatusFilter.value === '1' ? true : configStatusFilter.value === '0' ? false : undefined
      }
    })
    // 处理配置类型和状态的文本显示
    systemConfigs.value = response.data.map(config => ({
      ...config,
      config_key: config.key,
      config_value: config.value,
      config_type: config.key.includes('json') ? 3 : typeof config.value === 'number' ? 1 : typeof config.value === 'boolean' ? 2 : 0,
      config_type_text: config.key.includes('json') ? 'JSON' : typeof config.value === 'number' ? '数字' : typeof config.value === 'boolean' ? '布尔值' : '字符串',
      is_system: false,
      is_system_text: '否',
      status: config.is_active ? 1 : 0,
      status_text: config.is_active ? '启用' : '禁用'
    }))
  } catch (error) {
    console.error('获取系统配置失败:', error)
  } finally {
    configsLoading.value = false
  }
}

const editConfig = async (configId) => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`/api/v1/admin/configs/${configId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    currentConfig.value = response.data
    // 填充表单数据
    configForm.key = currentConfig.value.key
    configForm.value = currentConfig.value.value
    configForm.description = currentConfig.value.description
    configForm.is_active = currentConfig.value.is_active
    
    showEditConfigDialog.value = true
  } catch (error) {
    console.error('获取系统配置信息失败:', error)
    ElMessage.error('获取系统配置信息失败，请稍后重试')
  }
}

const saveConfig = async () => {
  try {
    const token = localStorage.getItem('token')
    let response
    
    if (currentConfig.value) {
      // 更新系统配置
      response = await axios.put(`/api/v1/admin/configs/${currentConfig.value.id}`, configForm, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      ElMessage.success('系统配置更新成功')
      showEditConfigDialog.value = false
    } else {
      // 创建系统配置
      response = await axios.post('/api/v1/admin/configs', configForm, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      ElMessage.success('系统配置创建成功')
      showAddConfigDialog.value = false
    }
    
    // 刷新系统配置列表
    getSystemConfigs()
  } catch (error) {
    console.error('保存系统配置失败:', error)
    ElMessage.error('保存系统配置失败，请稍后重试')
  }
}

const deleteConfig = async (configId) => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`/api/v1/admin/configs/${configId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    ElMessage.success('系统配置删除成功')
    // 刷新系统配置列表
    getSystemConfigs()
  } catch (error) {
    console.error('删除系统配置失败:', error)
    ElMessage.error('删除系统配置失败，请稍后重试')
  }
}

onMounted(() => {
  getSystemConfigs()
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