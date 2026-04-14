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
              <el-option label="招生简章" value="招生简章" />
              <el-option label="考试大纲" value="考试大纲" />
              <el-option label="成绩查询" value="成绩查询" />
              <el-option label="复试通知" value="复试通知" />
              <el-option label="录取通知" value="录取通知" />
            </el-select>
          </el-col>
        </el-row>
      </div>
      
      <!-- 考研情报表格 -->
      <el-table :data="kaoyanInfoList" style="width: 100%" v-loading="kaoyanLoading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="province" label="省份" width="120" />
        <el-table-column prop="category" label="类别" width="120" />
        <el-table-column prop="school" label="学校" />
        <el-table-column prop="url" label="链接" min-width="200">
          <template #default="scope">
            <a :href="scope.row.url" target="_blank">{{ scope.row.url }}</a>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
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
import { ElMessage } from 'element-plus'

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
    const response = await axios.get('/api/v1/kaoyan/info/list', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        keyword: kaoyanSearchQuery.value,
        province: kaoyanProvinceFilter.value,
        category: kaoyanCategoryFilter.value,
        skip: (kaoyanCurrentPage.value - 1) * kaoyanPageSize.value,
        limit: kaoyanPageSize.value
      }
    })
    
    if (response.data.success) {
      kaoyanInfoList.value = response.data.data.items
      kaoyanTotal.value = response.data.data.total
    }
  } catch (error) {
    console.error('获取考研情报失败:', error)
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
</style>