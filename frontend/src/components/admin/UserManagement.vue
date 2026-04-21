<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">用户管理</h3>
          <el-button type="primary" class="add-user-btn" @click="showAddUserDialog = true">添加用户</el-button>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索用户"
              clearable
              prefix-icon="Search"
              @keyup.enter="getUsers"
            >
              <template #append>
                <el-button type="primary" @click="getUsers">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="8">
            <el-select v-model="userTypeFilter" placeholder="按用户类型筛选" clearable @change="getUsers">
              <el-option label="全部" value="" />
              <el-option label="考研" value="考研" />
              <el-option label="考公" value="考公" />
              <el-option label="双赛道" value="双赛道" />
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-select v-model="userStatusFilter" placeholder="按状态筛选" clearable @change="getUsers">
              <el-option label="全部" value="" />
              <el-option label="活跃" value="true" />
              <el-option label="禁用" value="false" />
            </el-select>
          </el-col>
        </el-row>
      </div>
      
      <!-- 用户表格 -->
      <el-table :data="users" style="width: 100%">
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column label="用户类型">
          <template #default="scope">
            {{ scope.row.is_admin ? '' : scope.row.user_type }}
          </template>
        </el-table-column>
        <el-table-column prop="is_admin" label="管理员" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_admin ? 'danger' : 'info'">
              {{ scope.row.is_admin ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_vip" label="VIP" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.is_vip ? 'warning' : 'info'">
              {{ scope.row.is_vip ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="服务到期时间" width="180">
          <template #default="scope">
            {{ scope.row.vip_end_time ? new Date(scope.row.vip_end_time).toLocaleString() : '无' }}
          </template>
        </el-table-column>
        <el-table-column label="服务开始时间" width="180">
          <template #default="scope">
            {{ scope.row.vip_start_time ? new Date(scope.row.vip_start_time).toLocaleString() : '无' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
              {{ scope.row.is_active ? '活跃' : '到期' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editUser(scope.row.id)">编辑</el-button>
            <el-button type="info" size="small" @click="viewUserRequirements(scope.row.id)">查看需求</el-button>
            <el-button type="danger" size="small" @click="deleteUser(scope.row.id)" v-if="!scope.row.is_admin">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加用户对话框 -->
    <el-dialog
      v-model="showAddUserDialog"
      title="添加用户"
      width="600px"
    >
      <el-form :model="userForm" :rules="userFormRules" ref="userFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username" required>
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email" required>
          <el-input v-model="userForm.email" type="email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone" required>
          <el-input v-model="userForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="密码" prop="password" required>
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="用户类型" prop="user_type" required>
          <el-select v-model="userForm.user_type" placeholder="请选择用户类型">
            <el-option label="考研" value="考研" />
            <el-option label="考公" value="考公" />
            <el-option label="双赛道" value="双赛道" />
          </el-select>
        </el-form-item>
        <el-form-item label="管理员">
          <el-switch v-model="userForm.is_admin" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddUserDialog = false">取消</el-button>
          <el-button type="primary" @click="saveUser">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑用户对话框 -->
    <el-dialog
      v-model="showEditUserDialog"
      title="编辑用户"
      width="600px"
    >
      <el-form :model="userForm" :rules="userFormRules" ref="userFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username" required>
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email" required>
          <el-input v-model="userForm.email" type="email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone" required>
          <el-input v-model="userForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码（留空则不修改）" />
        </el-form-item>
        <el-form-item label="用户类型" prop="user_type" required>
          <el-select v-model="userForm.user_type" placeholder="请选择用户类型">
            <el-option label="考研" value="考研" />
            <el-option label="考公" value="考公" />
            <el-option label="双赛道" value="双赛道" />
          </el-select>
        </el-form-item>
        <el-form-item label="管理员">
          <el-switch v-model="userForm.is_admin" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditUserDialog = false">取消</el-button>
          <el-button type="primary" @click="saveUser">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 查看用户需求对话框 -->
    <el-dialog
      v-model="userRequirementsDialogVisible"
      :title="`用户需求 - ${currentUser?.username || ''}`"
      width="800px"
    >
      <el-tabs v-model="userRequirementsActiveTab">
        <el-tab-pane v-if="currentUser?.user_type !== '考公'" label="考研需求" name="kaoyan">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="关注省份">
              <el-tag v-for="province in (currentUserRequirements?.kaoyan?.provinces || [])" :key="province" class="mr-2 mb-2">
                {{ province }}
              </el-tag>
              <span v-if="!currentUserRequirements?.kaoyan?.provinces || currentUserRequirements?.kaoyan?.provinces.length === 0">无</span>
            </el-descriptions-item>
            <el-descriptions-item label="关注学校">
              {{ currentUserRequirements?.kaoyan?.schools || '无' }}
            </el-descriptions-item>
            <el-descriptions-item label="关注专业">
              {{ currentUserRequirements?.kaoyan?.majors || '无' }}
            </el-descriptions-item>
            <el-descriptions-item label="关注类型">
              <el-tag v-for="type in (currentUserRequirements?.kaoyan?.types || [])" :key="type" class="mr-2 mb-2">
                {{ type }}
              </el-tag>
              <span v-if="!currentUserRequirements?.kaoyan?.types || currentUserRequirements?.kaoyan?.types.length === 0">无</span>
            </el-descriptions-item>
            <el-descriptions-item label="关键词">
              {{ Array.isArray(currentUserRequirements?.kaoyan?.keywords) ? currentUserRequirements.kaoyan.keywords.join(', ') : (currentUserRequirements?.kaoyan?.keywords || '无') }}
            </el-descriptions-item>
          </el-descriptions>
        </el-tab-pane>
        <el-tab-pane v-if="currentUser?.user_type !== '考研'" label="考公需求" name="kaogong">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="关注省份">
              <el-tag v-for="province in (currentUserRequirements?.kaogong?.provinces || [])" :key="province" class="mr-2 mb-2">
                {{ province }}
              </el-tag>
              <span v-if="!currentUserRequirements?.kaogong?.provinces || currentUserRequirements?.kaogong?.provinces.length === 0">无</span>
            </el-descriptions-item>
            <el-descriptions-item label="关注专业">
              {{ currentUserRequirements?.kaogong?.majors || '无' }}
            </el-descriptions-item>
            <el-descriptions-item label="岗位类别">
              <el-tag v-for="type in (currentUserRequirements?.kaogong?.position_types || [])" :key="type" class="mr-2 mb-2">
                {{ type }}
              </el-tag>
              <span v-if="!currentUserRequirements?.kaogong?.position_types || currentUserRequirements?.kaogong?.position_types.length === 0">无</span>
            </el-descriptions-item>
            <el-descriptions-item label="关键词">
              {{ Array.isArray(currentUserRequirements?.kaogong?.keywords) ? currentUserRequirements.kaogong.keywords.join(', ') : (currentUserRequirements?.kaogong?.keywords || '无') }}
            </el-descriptions-item>
          </el-descriptions>
        </el-tab-pane>
        <el-tab-pane label="推送设置" name="push">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="推送频率">
              {{ 
                currentUserRequirements?.push?.frequency === 'hourly' ? '每小时' : 
                currentUserRequirements?.push?.frequency === 'daily' ? '每天' : 
                currentUserRequirements?.push?.frequency === 'weekly' ? '每周' : 
                '无'
              }}
            </el-descriptions-item>
            <el-descriptions-item label="推送时间">
              {{ currentUserRequirements?.push?.time || '无' }}
            </el-descriptions-item>
          </el-descriptions>
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="userRequirementsDialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="openEditUserRequirements">编辑</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑用户需求对话框 -->
    <el-dialog
      v-model="editUserRequirementsDialogVisible"
      :title="`编辑用户需求 - ${currentUser?.username || ''}`"
      width="800px"
    >
      <el-tabs v-model="editUserRequirementsActiveTab">
        <el-tab-pane v-if="currentUser?.user_type !== '考公'" label="考研需求" name="kaoyan">
          <el-form :model="editUserRequirementsForm.kaoyan" label-width="120px">
            <el-form-item label="关注省份">
              <el-select
                v-model="editUserRequirementsForm.kaoyan.provinces"
                multiple
                placeholder="请选择关注省份"
                style="width: 100%"
              >
                <el-option
                  v-for="province in editProvinces"
                  :key="province"
                  :label="province"
                  :value="province"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="关注学校">
              <el-input v-model="editUserRequirementsForm.kaoyan.schools" placeholder="请输入关注学校，多个学校用逗号分隔" />
            </el-form-item>
            <el-form-item label="关注专业">
              <el-input v-model="editUserRequirementsForm.kaoyan.majors" placeholder="请输入关注专业，多个专业用逗号分隔" />
            </el-form-item>
            <el-form-item label="关注类型">
              <el-select
                v-model="editUserRequirementsForm.kaoyan.types"
                multiple
                placeholder="请选择关注类型"
                style="width: 100%"
              >
                <el-option label="招生简章" value="招生简章" />
                <el-option label="考试大纲" value="考试大纲" />
                <el-option label="成绩查询" value="成绩查询" />
                <el-option label="复试通知" value="复试通知" />
                <el-option label="录取通知" value="录取通知" />
              </el-select>
            </el-form-item>
            <el-form-item label="关键词">
              <el-input v-model="editUserRequirementsForm.kaoyan.keywords" placeholder="请输入关键词，多个关键词用逗号分隔" />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane v-if="currentUser?.user_type !== '考研'" label="考公需求" name="kaogong">
          <el-form :model="editUserRequirementsForm.kaogong" label-width="120px">
            <el-form-item label="关注省份">
              <el-select
                v-model="editUserRequirementsForm.kaogong.provinces"
                multiple
                placeholder="请选择关注省份"
                style="width: 100%"
              >
                <el-option
                  v-for="province in editProvinces"
                  :key="province"
                  :label="province"
                  :value="province"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="岗位类别">
              <el-select
                v-model="editUserRequirementsForm.kaogong.position_types"
                multiple
                placeholder="请选择岗位类别"
                style="width: 100%"
              >
                <el-option label="公务员" value="公务员" />
                <el-option label="事业单位" value="事业单位" />
                <el-option label="教师" value="教师" />
                <el-option label="医疗" value="医疗" />
              </el-select>
            </el-form-item>
            <el-form-item label="专业">
              <el-input v-model="editUserRequirementsForm.kaogong.majors" placeholder="请输入专业，多个专业用逗号分隔" />
            </el-form-item>
            <el-form-item label="学历要求">
              <el-select
                v-model="editUserRequirementsForm.kaogong.education"
                placeholder="请选择学历要求"
                style="width: 100%"
              >
                <el-option label="不限" value="不限" />
                <el-option label="本科" value="本科" />
                <el-option label="硕士" value="硕士" />
                <el-option label="博士" value="博士" />
              </el-select>
            </el-form-item>
            <el-form-item label="是否应届生">
              <el-radio-group v-model="editUserRequirementsForm.kaogong.is_fresh_graduate">
                <el-radio value="是">是</el-radio>
                <el-radio value="否">否</el-radio>
                <el-radio value="不限">不限</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="关键词">
              <el-input v-model="editUserRequirementsForm.kaogong.keywords" placeholder="请输入关键词，多个关键词用逗号分隔" />
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="推送设置" name="push">
          <el-form :model="editUserRequirementsForm.push" label-width="120px">
            <el-form-item label="推送频率">
              <el-select
                v-model="editUserRequirementsForm.push.frequency"
                placeholder="请选择推送频率"
                style="width: 100%"
              >
                <el-option label="每小时" value="hourly" />
                <el-option label="每天" value="daily" />
                <el-option label="每周" value="weekly" />
              </el-select>
            </el-form-item>
            <el-form-item label="推送时间">
              <el-time-picker
                v-model="editUserRequirementsForm.push.time"
                format="HH:mm"
                value-format="HH:mm"
                placeholder="选择推送时间"
                style="width: 100%"
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editUserRequirementsDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveUserRequirements">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElSwitch, ElDialog, ElButton, ElTable, ElTableColumn, ElTag, ElTabs, ElTabPane, ElDescriptions, ElDescriptionsItem, ElSelectV2, ElRadio, ElRadioGroup, ElMessageBox } from 'element-plus'

// 用户管理相关
const users = ref([])
const searchQuery = ref('')
const userTypeFilter = ref('')
const userStatusFilter = ref('')
const showAddUserDialog = ref(false)
const showEditUserDialog = ref(false)
const currentUser = ref(null)
const userForm = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
  is_admin: false,
  user_type: '考研'
})

// 表单引用
const userFormRef = ref(null)

// 表单验证规则
const userFormRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在3-20之间', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' },
    {
      validator: async (rule, value, callback) => {
        if (!value) {
          callback()
          return
        }
        
        try {
          const token = localStorage.getItem('token')
          const response = await axios.get('/api/v1/admin/users', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          })
          
          const existingUser = response.data.find(user => 
            user.phone === value && user.id !== currentUser.value?.id
          )
          
          if (existingUser) {
            callback(new Error('手机号已被其他用户使用'))
          } else {
            callback()
          }
        } catch (error) {
          console.error('验证手机号失败:', error)
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  user_type: [
    { required: true, message: '请选择用户类型', trigger: 'change' }
  ]
})

// 用户需求查看相关
const userRequirementsDialogVisible = ref(false)
const currentUserRequirements = ref(null)
const userRequirementsActiveTab = ref('kaoyan')

// 编辑用户需求相关
const editUserRequirementsDialogVisible = ref(false)
const editUserRequirementsActiveTab = ref('kaoyan')
const editProvinces = ref([
  '北京', '天津', '河北', '山西', '内蒙古',
  '辽宁', '吉林', '黑龙江', '上海', '江苏',
  '浙江', '安徽', '福建', '江西', '山东',
  '河南', '湖北', '湖南', '广东', '广西',
  '海南', '重庆', '四川', '贵州', '云南',
  '西藏', '陕西', '甘肃', '青海', '宁夏',
  '新疆'
])
const editUserRequirementsForm = reactive({
  kaoyan: {
    provinces: [],
    schools: '',
    majors: '',
    types: [],
    keywords: ''
  },
  kaogong: {
    provinces: [],
    position_types: [],
    majors: '',
    education: '不限',
    is_fresh_graduate: '不限',
    keywords: ''
  },
  push: {
    frequency: 'daily',
    time: null
  }
})

// 获取用户列表
const getUsers = async () => {
  try {
    const token = localStorage.getItem('token')
    const params = {
      keyword: searchQuery.value
    }
    if (userTypeFilter.value) {
      params.user_type = userTypeFilter.value
    }
    if (userStatusFilter.value) {
      params.is_active = userStatusFilter.value === 'true'
    }
    
    const response = await axios.get('/api/v1/admin/users', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params
    })
    // 将管理员用户放在最顶端
    users.value = response.data.sort((a, b) => {
      if (a.is_admin && !b.is_admin) return -1
      if (!a.is_admin && b.is_admin) return 1
      return 0
    })
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

// 编辑用户
const editUser = async (userId) => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`/api/v1/admin/users/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    currentUser.value = response.data
    // 填充表单数据
    userForm.username = currentUser.value.username
    userForm.email = currentUser.value.email
    userForm.phone = currentUser.value.phone
    userForm.is_admin = currentUser.value.is_admin
    userForm.user_type = currentUser.value.user_type
    
    showEditUserDialog.value = true
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败，请稍后重试')
  }
}

// 保存用户
const saveUser = async () => {
  try {
    // 验证表单
    if (!userFormRef.value) return
    
    await userFormRef.value.validate(async (valid, fields) => {
      if (valid) {
        const token = localStorage.getItem('token')
        let response
        
        if (currentUser.value) {
          // 更新用户 - 不提交密码字段
          const updateData = { ...userForm }
          delete updateData.password
          response = await axios.put(`/api/v1/admin/users/${currentUser.value.id}`, updateData, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          })
          ElMessage.success('用户更新成功')
          showEditUserDialog.value = false
        } else {
          // 创建用户 - 根据user_type设置kaoyan_requirements和kaogong_requirements
          const registerData = { ...userForm }
          
          // 根据user_type设置kaoyan_requirements和kaogong_requirements
          if (registerData.user_type === '考研') {
            registerData.kaoyan_requirements = {}
          } else if (registerData.user_type === '考公') {
            registerData.kaogong_requirements = {}
          } else if (registerData.user_type === '双赛道') {
            registerData.kaoyan_requirements = {}
            registerData.kaogong_requirements = {}
          }
          
          response = await axios.post('/api/v1/auth/register', registerData, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'X-Admin-Create': 'true'
            }
          })
          ElMessage.success('用户创建成功')
          showAddUserDialog.value = false
        }
        
        // 刷新用户列表
        getUsers()
      } else {

        ElMessage.error('请检查表单填写是否正确')
      }
    })
  } catch (error) {
    console.error('保存用户失败:', error)
    ElMessage.error('保存用户失败，请稍后重试')
  }
}

// 删除用户
const deleteUser = async (userId) => {
  try {
    // 显示确认对话框
    await ElMessageBox.confirm(
      '确定要删除该用户吗？此操作不可恢复。',
      '删除用户',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 用户确认删除
    const token = localStorage.getItem('token')
    await axios.delete(`/api/v1/admin/users/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    ElMessage.success('用户删除成功')
    // 刷新用户列表
    getUsers()
  } catch (error) {
    // 如果用户取消删除，不显示错误信息
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
      ElMessage.error('删除用户失败，请稍后重试')
    }
  }
}

// 查看用户需求
const viewUserRequirements = async (userId) => {

  // 找到用户
  const user = users.value.find(u => u.id === userId)
  if (!user) {
    console.error('找不到用户，userId:', userId)
    return
  }
  
  currentUser.value = user

  
  try {
    // 调用API获取用户需求（添加时间戳防止缓存）
    const token = localStorage.getItem('token')


    const response = await axios.get(`/api/v1/admin/users/${userId}/requirements?timestamp=${Date.now()}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    


    // 确保response.data是一个对象
    if (!response.data) {
      response.data = {}
    }
    // 确保push属性存在
    if (!response.data.push) {
      response.data.push = {}
    }
    // 直接设置currentUserRequirements.value
    currentUserRequirements.value = response.data




    
    // 不要根据用户类型设置默认标签页，保留之前的设置
    // 这样在saveUserRequirements函数中设置的标签页就不会被覆盖
    
    // 直接显示对话框
    userRequirementsDialogVisible.value = true
  } catch (error) {
    console.error('获取用户需求失败:', error)
    console.error('错误详情:', error.response?.data)
    ElMessage.error('获取用户需求失败，请稍后重试')
  }
}

// 打开编辑用户需求对话框
const openEditUserRequirements = () => {
  // 重置编辑表单
  editUserRequirementsForm.kaoyan = {
    provinces: [],
    schools: '',
    majors: '',
    types: [],
    keywords: ''
  }
  editUserRequirementsForm.kaogong = {
    provinces: [],
    position_types: [],
    majors: '',
    education: '不限',
    is_fresh_graduate: '不限',
    keywords: ''
  }
  editUserRequirementsForm.push = {
    frequency: 'daily',
    time: null
  }
  
  // 直接复制当前需求数据到编辑表单，不做任何转换
  if (currentUserRequirements.value) {
    if (currentUserRequirements.value.kaoyan) {
      editUserRequirementsForm.kaoyan = { ...currentUserRequirements.value.kaoyan }
    }
    if (currentUserRequirements.value.kaogong) {
      editUserRequirementsForm.kaogong = { ...currentUserRequirements.value.kaogong }
    }
    if (currentUserRequirements.value.push) {
      editUserRequirementsForm.push = { ...currentUserRequirements.value.push }
    }
  }
  
  // 根据用户类型设置默认标签页
  if (currentUser.value?.user_type === '考研') {
    editUserRequirementsActiveTab.value = 'kaoyan'
  } else if (currentUser.value?.user_type === '考公') {
    editUserRequirementsActiveTab.value = 'kaogong'
  } else {
    editUserRequirementsActiveTab.value = 'kaoyan'
  }
  
  // 显示编辑对话框
  editUserRequirementsDialogVisible.value = true
}

// 保存用户需求
const saveUserRequirements = async () => {
  try {
    const token = localStorage.getItem('token')
    
    // 准备发送给后端的数据
    const data = { ...editUserRequirementsForm }
    
    // 确保push.time不为null
    if (!data.push.time) {
      data.push.time = ''
    }
    
    // 时间选择器已经使用value-format="HH:mm"，不需要再格式化
    



    
    await axios.put(`/api/v1/admin/users/${currentUser.value.id}/requirements`, data, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    ElMessage.success('用户需求更新成功')
    editUserRequirementsDialogVisible.value = false
    
    // 保存当前用户ID
    const userId = currentUser.value.id
    // 等待对话框关闭后再重新获取数据并打开查看对话框
    setTimeout(async () => {
      // 设置标签页为推送设置
      userRequirementsActiveTab.value = 'push'
      // 重新获取用户需求并显示更新后的数据
      await viewUserRequirements(userId)
    }, 300)
  } catch (error) {
    console.error('保存用户需求失败:', error)
    console.error('错误详情:', error.response?.data)
    ElMessage.error('保存用户需求失败，请稍后重试')
  }
}

onMounted(() => {
  getUsers()
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

.mr-2 {
  margin-right: 8px;
}

.mb-2 {
  margin-bottom: 8px;
}
</style>