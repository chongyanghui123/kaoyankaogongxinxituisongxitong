<template>
  <div class="student-form-container">
    <div class="form-card">
      <h2 class="form-title">考公学生信息录入</h2>
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="120px">
        <!-- 基本信息 -->
        <el-card class="form-section" header="基本信息" shadow="hover">
          <el-form-item label="姓名" prop="real_name">
            <el-input v-model="formData.real_name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="formData.email" placeholder="请输入邮箱" />
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="formData.phone" placeholder="请输入手机号" />
          </el-form-item>
          <el-form-item label="性别">
            <el-radio-group v-model="formData.gender">
              <el-radio label="男">男</el-radio>
              <el-radio label="女">女</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="出生日期">
            <el-date-picker
              v-model="formData.birthdate"
              type="date"
              placeholder="选择日期"
              style="width: 100%"
            />
          </el-form-item>
        </el-card>

        <!-- 考公需求 -->
        <el-card class="form-section" header="考公需求" shadow="hover">
          <el-form-item label="关注省份">
            <el-select
              v-model="formData.kaogong.provinces"
              multiple
              placeholder="请选择关注省份"
              style="width: 100%"
            >
              <el-option
                v-for="province in provinces"
                :key="province"
                :label="province"
                :value="province"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="岗位类别">
            <el-select
              v-model="formData.kaogong.position_types"
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
            <el-input v-model="formData.kaogong.majors" placeholder="请输入专业，多个专业用逗号分隔" />
          </el-form-item>
          <el-form-item label="学历要求">
            <el-select
              v-model="formData.kaogong.education"
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
            <el-radio-group v-model="formData.kaogong.is_fresh_graduate">
              <el-radio label="是">是</el-radio>
              <el-radio label="否">否</el-radio>
              <el-radio label="不限">不限</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="关键词">
            <el-input v-model="formData.kaogong.keywords" placeholder="请输入关键词，多个关键词用逗号分隔" />
          </el-form-item>
        </el-card>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <el-button type="primary" @click="submitForm">提交信息</el-button>
          <el-button @click="resetForm">重置</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

// 表单数据
const formData = reactive({
  real_name: '',
  email: '',
  phone: '',
  gender: '男',
  birthdate: null,
  kaogong: {
    provinces: [],
    position_types: [],
    majors: '',
    education: '不限',
    is_fresh_graduate: '不限',
    keywords: ''
  }
})

// 表单验证规则
const rules = {
  real_name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

// 表单引用
const formRef = ref(null)

// 省份列表
const provinces = [
  '北京', '天津', '河北', '山西', '内蒙古',
  '辽宁', '吉林', '黑龙江', '上海', '江苏',
  '浙江', '安徽', '福建', '江西', '山东',
  '河南', '湖北', '湖南', '广东', '广西',
  '海南', '重庆', '四川', '贵州', '云南',
  '西藏', '陕西', '甘肃', '青海', '宁夏',
  '新疆'
]

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        // 准备提交数据
        const submitData = {
          username: formData.real_name,
          email: formData.email,
          password: '123456a', // 默认密码，包含字母和数字
          phone: formData.phone,
          real_name: formData.real_name,
          gender: formData.gender,
          birthdate: formData.birthdate ? formData.birthdate.toISOString().split('T')[0] : null,
          kaoyan_requirements: null,
          kaogong_requirements: {
            provinces: formData.kaogong.provinces,
            position_types: formData.kaogong.position_types,
            majors: formData.kaogong.majors,
            education: formData.kaogong.education,
            is_fresh_graduate: formData.kaogong.is_fresh_graduate,
            keywords: formData.kaogong.keywords
          }
        }

        // 调用API创建用户
        const response = await axios.post('/api/v1/auth/register', submitData)
        
        if (response.data && (response.data.code === 200 || response.data.code === 201)) {
          ElMessage.success('学生信息录入成功！')
          resetForm()
        } else {
          ElMessage.error('录入失败：' + (response.data.message || '未知错误'))
        }
      } catch (error) {
        console.error('录入失败', error)
        ElMessage.error('录入失败：' + (error.response?.data?.message || '网络错误'))
      }
    } else {

      ElMessage.error('请检查表单填写是否正确')
    }
  })
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  // 重置需求数据
  formData.kaogong = {
    provinces: [],
    position_types: [],
    majors: '',
    education: '不限',
    is_fresh_graduate: '不限',
    keywords: ''
  }
}


</script>

<style scoped>
.student-form-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.form-card {
  width: 100%;
  max-width: 800px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.form-title {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: 600;
}

.form-section {
  margin-bottom: 20px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.el-form-item {
  margin-bottom: 15px;
}
</style>