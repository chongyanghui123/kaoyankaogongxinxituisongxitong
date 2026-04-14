<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">考公情报管理</h3>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="kaogongSearchQuery"
              placeholder="搜索考公情报"
              clearable
              prefix-icon="Search"
              @keyup.enter="getKaogongInfo"
            >
              <template #append>
                <el-button type="primary" @click="getKaogongInfo">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="8">
            <el-select v-model="kaogongProvinceFilter" placeholder="按省份筛选" clearable @change="getKaogongInfo">
              <el-option label="全部" value="" />
              <el-option
                v-for="province in kaogongProvinces"
                :key="province"
                :label="province"
                :value="province"
              />
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-select v-model="kaogongCategoryFilter" placeholder="按类别筛选" clearable @change="getKaogongInfo">
              <el-option label="全部" value="" />
              <el-option label="公务员" value="公务员" />
              <el-option label="事业单位" value="事业单位" />
              <el-option label="教师" value="教师" />
              <el-option label="医疗" value="医疗" />
            </el-select>
          </el-col>
        </el-row>
      </div>
      
      <!-- 考公情报表格 -->
      <el-table :data="kaogongInfoList" style="width: 100%" v-loading="kaogongLoading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="province" label="省份" width="120" />
        <el-table-column prop="category" label="类别" width="120" />
        <el-table-column prop="position_type" label="岗位类型" />
        <el-table-column prop="url" label="链接" min-width="200">
          <template #default="scope">
            <a :href="scope.row.url" target="_blank">{{ scope.row.url }}</a>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button type="danger" size="small" @click="deleteKaogongInfo(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination" v-if="!kaogongLoading && kaogongInfoList.length > 0">
        <el-pagination
          v-model:current-page="kaogongCurrentPage"
          v-model:page-size="kaogongPageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="kaogongTotal"
          @size-change="kaogongHandleSizeChange"
          @current-change="kaogongHandleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// 考公情报管理相关
const kaogongInfoList = ref([])
const kaogongLoading = ref(false)
const kaogongCurrentPage = ref(1)
const kaogongPageSize = ref(10)
const kaogongTotal = ref(0)
const kaogongSearchQuery = ref('')
const kaogongProvinceFilter = ref('')
const kaogongCategoryFilter = ref('')
const kaogongProvinces = ref([
  '北京', '天津', '河北', '山西', '内蒙古',
  '辽宁', '吉林', '黑龙江', '上海', '江苏',
  '浙江', '安徽', '福建', '江西', '山东',
  '河南', '湖北', '湖南', '广东', '广西',
  '海南', '重庆', '四川', '贵州', '云南',
  '西藏', '陕西', '甘肃', '青海', '宁夏',
  '新疆'
])

// 获取考公情报列表
const getKaogongInfo = async () => {
  try {
    kaogongLoading.value = true
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/kaogong/info/list', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        keyword: kaogongSearchQuery.value,
        province: kaogongProvinceFilter.value,
        category: kaogongCategoryFilter.value,
        skip: (kaogongCurrentPage.value - 1) * kaogongPageSize.value,
        limit: kaogongPageSize.value
      }
    })
    
    if (response.data.success) {
      kaogongInfoList.value = response.data.data.items
      kaogongTotal.value = response.data.data.total
    }
  } catch (error) {
    console.error('获取考公情报失败:', error)
  } finally {
    kaogongLoading.value = false
  }
}

// 处理分页大小变化
const kaogongHandleSizeChange = (size) => {
  kaogongPageSize.value = size
  getKaogongInfo()
}

// 处理当前页码变化
const kaogongHandleCurrentChange = (current) => {
  kaogongCurrentPage.value = current
  getKaogongInfo()
}

// 删除考公情报
const deleteKaogongInfo = async (id) => {
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`/api/v1/kaogong/info/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    ElMessage.success('考公情报删除成功')
    // 刷新考公情报列表
    getKaogongInfo()
  } catch (error) {
    console.error('删除考公情报失败:', error)
    ElMessage.error('删除考公情报失败，请稍后重试')
  }
}

onMounted(() => {
  getKaogongInfo()
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