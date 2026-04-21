<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">考研情报管理</h3>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="kaoyanSearchQuery"
              placeholder="搜索考研情报"
              clearable
              prefix-icon="Search"
              @keyup.enter="getKaoyanInfo"
            >
              <template #append>
                <el-button type="primary" @click="getKaoyanInfo">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="8">
            <el-select v-model="kaoyanProvinceFilter" placeholder="按省份筛选" clearable @change="getKaoyanInfo">
              <el-option label="全部" value="" />
              <el-option
                v-for="province in kaoyanProvinces"
                :key="province"
                :label="province"
                :value="province"
              />
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-select v-model="kaoyanCategoryFilter" placeholder="按类别筛选" clearable @change="getKaoyanInfo">
              <el-option label="全部" value="" />
              <el-option label="招生简章" value="0" />
              <el-option label="考试大纲" value="1" />
              <el-option label="成绩查询" value="2" />
              <el-option label="复试通知" value="3" />
              <el-option label="录取通知" value="4" />
              <el-option label="普通通知" value="5" />
            </el-select>
          </el-col>
        </el-row>
        <div class="action-buttons">
          <el-button type="danger" @click="deleteAllKaoyanInfo">全部删除</el-button>
        </div>
      </div>
      
      <!-- 考研情报表格 -->
      <el-table :data="kaoyanInfoList" style="width: 100%" v-loading="kaoyanLoading">
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="category_text" label="类别" width="120" />
        <el-table-column prop="province" label="省份" width="120" />
        <el-table-column prop="school" label="学校" width="200" />
        <el-table-column label="用户需求" width="250">
          <template #default="scope">
            <div class="user-requirements">
              <div v-if="(scope.row.user_requirements || []).length > 0">
                <template v-for="(item, index) in (scope.row.user_requirements || []).slice(0, 3)" :key="index">
                  <el-popover
                    placement="top"
                    width="400"
                    trigger="hover"
                    popper-class="requirements-popover"
                  >
                    <template #default>
                      <div class="requirements-details">
                        <h4>{{ item.username || '未知用户' }} ({{ item.email || '未知邮箱' }})</h4>
                        <div v-if="item.requirements && item.requirements.kaoyan">
                          <p><strong>考研需求:</strong></p>
                          <p>关键词: {{ item.requirements.kaoyan.keywords || '无' }}</p>
                          <p>省份: {{ item.requirements.kaoyan.provinces || '无' }}</p>
                          <p>学校: {{ item.requirements.kaoyan.schools || '无' }}</p>
                          <p>专业: {{ item.requirements.kaoyan.majors || '无' }}</p>
                        </div>
                      </div>
                    </template>
                    <template #reference>
                      <el-tag size="small" style="margin-right: 5px; margin-bottom: 5px;">
                        {{ item.username || '未知用户' }}
                      </el-tag>
                    </template>
                  </el-popover>
                </template>
                <el-tag
                  v-if="(scope.row.user_requirements || []).length > 3"
                  size="small"
                  type="info"
                >
                  +{{ (scope.row.user_requirements || []).length - 3 }}
                </el-tag>
              </div>
              <span v-else>无</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="url" label="链接" min-width="200">
          <template #default="scope">
            <a :href="scope.row.url" target="_blank">{{ scope.row.url }}</a>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column prop="is_processed" label="是否处理" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.is_processed ? 'success' : 'danger'">
              {{ scope.row.is_processed ? '已处理' : '未处理' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button type="danger" size="small" @click="deleteKaoyanInfo(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination" v-if="!kaoyanLoading && kaoyanInfoList.length > 0">
        <el-pagination
          v-model:current-page="kaoyanCurrentPage"
          v-model:page-size="kaoyanPageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="kaoyanTotal"
          @size-change="kaoyanHandleSizeChange"
          @current-change="kaoyanHandleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

// 考研情报管理相关
const kaoyanInfoList = ref([])
const kaoyanLoading = ref(false)
const kaoyanCurrentPage = ref(1)
const kaoyanPageSize = ref(10)
const kaoyanTotal = ref(0)
const kaoyanSearchQuery = ref('')
const kaoyanProvinceFilter = ref('')
const kaoyanCategoryFilter = ref('')
const kaoyanProvinces = ref([
  '北京', '天津', '河北', '山西', '内蒙古',
  '辽宁', '吉林', '黑龙江', '上海', '江苏',
  '浙江', '安徽', '福建', '江西', '山东',
  '河南', '湖北', '湖南', '广东', '广西',
  '海南', '重庆', '四川', '贵州', '云南',
  '西藏', '陕西', '甘肃', '青海', '宁夏',
  '新疆'
])

// 获取考研情报列表
const getKaoyanInfo = async () => {
  try {
    kaoyanLoading.value = true
    const token = localStorage.getItem('token')
    const params = {
      page: kaoyanCurrentPage.value,
      page_size: kaoyanPageSize.value
    }
    if (kaoyanSearchQuery.value) {
      params.keyword = kaoyanSearchQuery.value
    }
    if (kaoyanProvinceFilter.value) {
      params.province = kaoyanProvinceFilter.value
    }
    if (kaoyanCategoryFilter.value !== '') {
      params.category = Number(kaoyanCategoryFilter.value)
    }
    
    const response = await axios.get('/api/v1/kaoyan/info/list', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params
    })
    
    if (response.data && response.data.total !== undefined) {
      kaoyanInfoList.value = response.data.items || []
      kaoyanTotal.value = response.data.total
    } else {
      kaoyanInfoList.value = []
      kaoyanTotal.value = 0
    }
  } catch (error) {

    kaoyanInfoList.value = []
    kaoyanTotal.value = 0
  } finally {
    kaoyanLoading.value = false
  }
}

// 处理分页大小变化
const kaoyanHandleSizeChange = (size) => {
  kaoyanPageSize.value = size
  getKaoyanInfo()
}

// 处理当前页码变化
const kaoyanHandleCurrentChange = (current) => {
  kaoyanCurrentPage.value = current
  getKaoyanInfo()
}

// 删除考研情报
const deleteKaoyanInfo = async (id) => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`/api/v1/kaoyan/info/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    ElMessage.success('考研情报删除成功')
    // 刷新考研情报列表
    getKaoyanInfo()
  } catch (error) {
    console.error('删除考研情报失败:', error)
    ElMessage.error('删除考研情报失败，请稍后重试')
  }
}

// 删除所有考研情报
const deleteAllKaoyanInfo = async () => {
  try {
    // 确认删除
    const confirmed = await ElMessageBox.confirm('确定要删除所有考研情报吗？此操作不可恢复！', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    if (confirmed) {
      const token = localStorage.getItem('token')
      await axios.delete('/api/v1/kaoyan/delete-all', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        data: {} // 发送空数据以满足 DELETE 请求的数据要求
      })
      ElMessage.success('所有考研情报删除成功')
      // 刷新考研情报列表
      getKaoyanInfo()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除所有考研情报失败:', error)
      ElMessage.error('删除所有考研情报失败，请稍后重试')
    }
  }
}

onMounted(() => {
  getKaoyanInfo()
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

.user-requirements {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.requirements-details {
  font-size: 14px;
  line-height: 1.5;
}

.requirements-details h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.requirements-details p {
  margin: 5px 0;
}
</style>