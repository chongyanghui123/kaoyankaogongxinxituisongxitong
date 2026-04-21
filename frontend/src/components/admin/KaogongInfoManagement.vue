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
              <el-option label="公务员" value="0" />
              <el-option label="事业单位" value="1" />
              <el-option label="教师" value="2" />
              <el-option label="医疗" value="3" />
            </el-select>
          </el-col>
        </el-row>
        <div class="action-buttons">
          <el-button type="danger" @click="deleteAllKaogongInfo">全部删除</el-button>
        </div>
      </div>
      
      <!-- 考公情报表格 -->
      <el-table :data="kaogongInfoList" style="width: 100%" v-loading="kaogongLoading">
        <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="province" label="省份" width="120" />
        <el-table-column prop="category_text" label="类别" width="120" />
        <el-table-column prop="position_type" label="岗位类别" />
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
                        <div v-if="item.requirements && item.requirements.kaogong">
                          <p><strong>考公需求:</strong></p>
                          <p>关键词: {{ item.requirements.kaogong.keywords || '无' }}</p>
                          <p>省份: {{ item.requirements.kaogong.provinces || '无' }}</p>
                          <p>岗位类别: {{ item.requirements.kaogong.position_types || '无' }}</p>
                          <p>专业: {{ item.requirements.kaogong.majors || '无' }}</p>
                          <p>学历要求: {{ item.requirements.kaogong.education || '无' }}</p>
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
import { ElMessage, ElMessageBox } from 'element-plus'

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
    const params = {
      page: kaogongCurrentPage.value,
      page_size: kaogongPageSize.value
    }
    if (kaogongSearchQuery.value) {
      params.keyword = kaogongSearchQuery.value
    }
    if (kaogongProvinceFilter.value) {
      params.province = kaogongProvinceFilter.value
    }
    if (kaogongCategoryFilter.value !== '') {
      params.category = Number(kaogongCategoryFilter.value)
    }
    
    const response = await axios.get('/api/v1/kaogong/info/list', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params
    })
    
    if (response.data && response.data.total !== undefined) {
      kaogongInfoList.value = response.data.items || []
      kaogongTotal.value = response.data.total
    } else {
      kaogongInfoList.value = []
      kaogongTotal.value = 0
    }
  } catch (error) {

    kaogongInfoList.value = []
    kaogongTotal.value = 0
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

// 删除所有考公情报
const deleteAllKaogongInfo = async () => {
  try {
    // 确认删除
    const confirmed = await ElMessageBox.confirm('确定要删除所有考公情报吗？此操作不可恢复！', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    if (confirmed) {
      const token = localStorage.getItem('token')
      await axios.delete('/api/v1/kaogong/delete-all', {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        data: {} // 发送空数据以满足 DELETE 请求的数据要求
      })
      ElMessage.success('所有考公情报删除成功')
      // 刷新考公情报列表
      getKaogongInfo()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除所有考公情报失败:', error)
      ElMessage.error('删除所有考公情报失败，请稍后重试')
    }
  }
}

onMounted(() => {
  getKaogongInfo()
})
</script>

<style scoped>
.admin-content {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
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