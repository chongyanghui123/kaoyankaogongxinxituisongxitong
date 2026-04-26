<template>
  <div class="student-form-container">
    <div class="form-card">
      <h2 class="form-title">考研学生信息录入</h2>
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
          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="formData.gender">
              <el-radio value="男">男</el-radio>
              <el-radio value="女">女</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="出生日期" prop="birthdate">
            <el-date-picker
              v-model="formData.birthdate"
              type="date"
              placeholder="选择日期"
              style="width: 100%"
            />
          </el-form-item>
        </el-card>

        <!-- 考研需求 -->
        <el-card class="form-section" header="考研需求" shadow="hover">
          <el-form-item label="关注省份" prop="kaoyan.provinces">
            <el-select
              v-model="formData.kaoyan.provinces"
              multiple
              placeholder="请选择关注省份"
              style="width: 100%"
              @change="handleProvinceChange"
            >
              <el-option
                v-for="province in provinces"
                :key="province"
                :label="province"
                :value="province"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="关注学校" prop="kaoyan.schools">
            <el-select
              v-model="formData.kaoyan.schools"
              multiple
              placeholder="请选择关注学校"
              style="width: 100%"
            >
              <el-option
                v-for="school in schools"
                :key="school"
                :label="school"
                :value="school"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="关注专业" prop="kaoyan.majors">
            <el-input v-model="formData.kaoyan.majors" placeholder="请输入关注专业，多个专业用逗号分隔" />
          </el-form-item>
          <el-form-item label="关注类型" prop="kaoyan.types">
            <el-select
              v-model="formData.kaoyan.types"
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
          <el-form-item label="关键词" prop="kaoyan.keywords">
            <el-input v-model="formData.kaoyan.keywords" placeholder="请输入关键词，多个关键词用逗号分隔" />
          </el-form-item>
        </el-card>

        <!-- 产品选择 -->
        <el-card class="form-section" header="产品选择" shadow="hover">
          <el-form-item label="选择产品" required>
            <el-radio-group v-model="selectedProductId" @change="handleProductChange">
              <el-radio-button
                v-for="product in products"
                :key="product.id"
                :value="product.id"
              >
                <span>{{ product.name }} - ¥{{ product.price }}</span>
              </el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="产品详情">
            <div v-if="selectedProduct" class="product-details">
              <p><strong>产品描述：</strong>{{ selectedProduct.description }}</p>
              <p><strong>价格：</strong>¥{{ selectedProduct.price }}</p>
              <p><strong>时长：</strong>{{ selectedProduct.duration }}天</p>
              <p><strong>类型：</strong>{{ getProductTypeText(selectedProduct.type) }}</p>
            </div>
            <div v-else class="product-details">
              <p>请选择一个产品</p>
            </div>
          </el-form-item>
        </el-card>

        <!-- 支付方式 -->
        <el-card class="form-section" header="支付方式" shadow="hover">
          <el-form-item label="支付方式" prop="paymentMethod" required>
            <el-radio-group v-model="formData.paymentMethod">
              <el-radio value="1">微信支付</el-radio>
              <el-radio value="2">支付宝</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-card>

        <!-- 提交按钮 -->
        <div class="form-actions">
          <el-button type="primary" @click="handlePayment">立即支付</el-button>
          <el-button @click="resetForm">重置</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

// 提交状态
const hasSubmitted = ref(false)
const isProcessing = ref(false)

// 产品相关
const products = ref([])
const productsLoading = ref(false)
const selectedProductId = ref(null)
const selectedProduct = ref(null)

// 获取产品列表
const getProducts = async () => {
  try {
    productsLoading.value = true
    const response = await axios.get('/api/v1/payments/products')
    // 筛选考研相关产品（type=1或type=3）
    products.value = response.data.filter(product => 
      product.type === 1 || product.type === 3
    )
    // 默认选择第一个产品
    if (products.value.length > 0) {
      selectedProductId.value = products.value[0].id
      selectedProduct.value = products.value[0]
    }
  } catch (error) {
    console.error('获取产品列表失败:', error)
    ElMessage.error('获取产品列表失败，请稍后重试')
  } finally {
    productsLoading.value = false
  }
}

// 产品选择变化
const handleProductChange = (productId) => {
  selectedProduct.value = products.value.find(product => product.id === productId)
}

// 获取产品类型文本
const getProductTypeText = (type) => {
  const typeMap = {
    1: '考研VIP',
    2: '考公VIP',
    3: '双赛道VIP'
  }
  return typeMap[type] || '未知类型'
}

// 表单数据
const formData = reactive({
  real_name: '',
  email: '',
  phone: '',
  gender: '男',
  birthdate: null,
  paymentMethod: '1', // 添加支付方式字段到formData中
  kaoyan: {
    provinces: [],
    schools: [],
    majors: '',
    types: [],
    keywords: ''
  }
})

// 学校列表
const schools = ref([])

// 省份列表
const provinces = ref([])

// 加载状态
const loading = ref(false)

// 获取省份列表
const getProvinces = async () => {
  try {
    const response = await axios.get('/api/v1/utils/provinces')
    if (response.data && response.data.success) {
      provinces.value = response.data.data
    }
  } catch (error) {
    console.error('获取省份列表失败', error)
    // 失败时使用默认省份列表（数据库中实际存在的省份）
    provinces.value = [
      '上海', '云南', '内蒙古', '北京', '吉林',
      '四川', '天津', '宁夏', '安徽', '山东',
      '山西', '广东', '广西', '新疆', '江苏',
      '江西', '河北', '河南', '浙江', '海南',
      '湖北', '湖南', '甘肃', '福建', '西藏',
      '贵州', '辽宁', '重庆', '陕西', '青海',
      '黑龙江'
    ]
  }
}

// 省份选择变化时获取学校列表
const handleProvinceChange = async (value) => {

  if (value && value.length > 0) {
    try {
      loading.value = true
      // 并行获取所有选中省份的学校
      const schoolPromises = value.map(province => 
        axios.get(`/api/v1/utils/schools?province=${encodeURIComponent(province)}`)
      )
      
      const responses = await Promise.all(schoolPromises)
      let allSchools = []
      
      // 合并所有省份的学校
      responses.forEach(response => {
        if (response.data && response.data.success) {
          allSchools = [...allSchools, ...response.data.data]
        }
      })
      
      // 去重
      allSchools = [...new Set(allSchools)]
      schools.value = allSchools
    } catch (error) {
      console.error('获取学校列表失败', error)
      schools.value = []
    } finally {
      loading.value = false
    }
  } else {
    schools.value = []
    // 清空已选择的学校
    formData.kaoyan.schools = []
  }
}

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
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  birthdate: [
    { required: true, message: '请选择出生日期', trigger: 'change' }
  ],
  'kaoyan.provinces': [
    { required: true, message: '请选择关注省份', trigger: 'change' }
  ],
  'kaoyan.schools': [
    { required: true, message: '请选择关注学校', trigger: 'change' }
  ],
  'kaoyan.majors': [
    { required: true, message: '请输入关注专业', trigger: 'blur' }
  ],
  'kaoyan.types': [
    { required: true, message: '请选择关注类型', trigger: 'change' }
  ],
  'kaoyan.keywords': [
    { required: true, message: '请输入关键词', trigger: 'blur' }
  ],
  paymentMethod: [
    { required: true, message: '请选择支付方式', trigger: 'change' }
  ]
}

// 表单引用
const formRef = ref(null)

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        if (!selectedProductId.value) {
          ElMessage.error('请选择一个产品')
          return
        }
        
        loading.value = true
        // 准备提交数据
        const submitData = {
          username: formData.real_name,
          email: formData.email,
          // 普通用户不需要密码字段
          phone: formData.phone,
          real_name: formData.real_name,
          gender: formData.gender,
          birthdate: formData.birthdate ? formData.birthdate.toISOString().split('T')[0] : null,
          kaoyan_requirements: {
            provinces: formData.kaoyan.provinces,
            schools: formData.kaoyan.schools.join(','),
            majors: formData.kaoyan.majors,
            types: formData.kaoyan.types,
            keywords: formData.kaoyan.keywords
          },
          kaogong_requirements: null
        }

        // 调用API创建用户
        const registerResponse = await axios.post('/api/v1/auth/register', submitData)
        
        if (registerResponse.data && (registerResponse.data.code === 200 || registerResponse.data.code === 201)) {
          ElMessage.success('学生信息录入成功！')
          
          // 自动登录
          const loginResponse = await axios.post('/api/v1/auth/login', {
            username: formData.email,
            // 普通用户不需要密码字段
          })
          
          if (loginResponse.data && loginResponse.data.success) {
            // 保存登录信息
            localStorage.setItem('token', loginResponse.data.data.access_token)
            localStorage.setItem('userInfo', JSON.stringify({
              id: loginResponse.data.data.user_id,
              username: loginResponse.data.data.username,
              email: loginResponse.data.data.email,
              phone: loginResponse.data.data.phone,
              is_admin: loginResponse.data.data.is_admin
            }))
            
            // 设置已提交状态，显示支付按钮
            hasSubmitted.value = true
          } else {
            ElMessage.error('自动登录失败：' + (loginResponse.data?.message || '未知错误'))
          }
          
          resetForm()
        } else {
          ElMessage.error('录入失败：' + (registerResponse.data?.message || '未知错误'))
        }
      } catch (error) {
        console.error('录入失败', error)
        ElMessage.error('录入失败：' + (error.response?.data?.message || '网络错误'))
      } finally {
        loading.value = false
      }
    } else {
      ElMessage.error('请检查表单填写是否正确')
    }
  })
}

// 立即支付
const handlePayment = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        if (!selectedProductId.value) {
          ElMessage.error('请选择一个产品')
          return
        }
        
        loading.value = true
        // 准备提交数据（用于支付页面）
        const userData = {
          username: formData.real_name,
          email: formData.email,
          phone: formData.phone,
          password: undefined,
          real_name: formData.real_name,
          gender: formData.gender,
          birthdate: formData.birthdate ? formData.birthdate.toISOString().split('T')[0] : null,
          kaoyan_requirements: {
            provinces: formData.kaoyan.provinces,
            schools: formData.kaoyan.schools.join(','),
            majors: formData.kaoyan.majors,
            types: formData.kaoyan.types,
            keywords: formData.kaoyan.keywords
          },
          kaogong_requirements: null,
          is_admin: false // 明确指定是普通用户
        }
        
        console.log('准备支付的用户数据:', userData)
        
        // 保存用户数据到 localStorage，供支付页面使用
        localStorage.setItem('pendingUserData', JSON.stringify(userData))
        
        // 直接跳转到支付页面，传递产品信息
        router.push({
          path: '/payment',
          query: {
            product_id: selectedProductId.value,
            payment_method: formData.paymentMethod
          }
        })
      } catch (error) {
        console.error('支付失败', error)
        ElMessage.error('支付失败：' + (error.response?.data?.message || '网络错误'))
      } finally {
        loading.value = false
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
  formData.kaoyan = {
    provinces: [],
    schools: [],
    majors: '',
    types: [],
    keywords: ''
  }
}



// 初始化
onMounted(() => {
  getProvinces()
  getProducts()
})
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