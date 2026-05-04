<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">小组管理</h3>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索小组名称"
              clearable
              prefix-icon="Search"
              @keyup.enter="getGroups"
            >
              <template #append>
                <el-button type="primary" @click="getGroups">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="8">
            <el-select v-model="statusFilter" placeholder="按状态筛选" clearable @change="getGroups">
              <el-option label="全部" value="" />
              <el-option label="正常" value="1" />
              <el-option label="禁用" value="0" />
            </el-select>
          </el-col>
        </el-row>
      </div>
      
      <!-- 小组表格 -->
      <el-table 
        ref="groupTable" 
        :data="groups" 
        style="width: 100%" 
        border 
        :empty-text="emptyText"
        :show-header="true"
      >
        <el-table-column type="index" label="序号" width="60" :index="(index) => index + 1" />
        <el-table-column prop="name" label="小组名称" width="150" :show-overflow-tooltip="true" />
        <el-table-column prop="description" label="描述" width="200" :show-overflow-tooltip="true" />
        <el-table-column prop="member_count" label="成员数" width="80" align="center" />
        <el-table-column prop="tags" label="标签" width="120" :show-overflow-tooltip="true" />
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="状态" width="80" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
              {{ scope.row.status === 1 ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewGroupDetail(scope.row)">详情</el-button>
            <el-button 
              type="warning" 
              size="small" 
              @click="toggleGroupStatus(scope.row)"
            >
              {{ scope.row.status === 1 ? '禁用' : '启用' }}
            </el-button>
            <el-button type="danger" size="small" @click="deleteGroup(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 小组详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="小组详情"
      width="600px"
    >
      <el-form v-if="selectedGroup" label-width="100px">
        <el-form-item label="小组名称">
          <span>{{ selectedGroup.name }}</span>
        </el-form-item>
        <el-form-item label="描述">
          <span>{{ selectedGroup.description }}</span>
        </el-form-item>
        <el-form-item label="成员数">
          <span>{{ selectedGroup.member_count }}</span>
        </el-form-item>
        <el-form-item label="今日活跃">
          <span>{{ selectedGroup.active_today }}</span>
        </el-form-item>
        <el-form-item label="帖子数">
          <span>{{ selectedGroup.post_count }}</span>
        </el-form-item>
        <el-form-item label="创建时间">
          <span>{{ selectedGroup.created_at }}</span>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from '../../utils/axios';

const groupTable = ref(null);
const groups = ref([]);
const searchQuery = ref('');
const statusFilter = ref('');
const showDetailDialog = ref(false);
const selectedGroup = ref(null);
const emptyText = '暂无数据';

const getGroups = async () => {
  try {
    const params = {
      search: searchQuery.value || undefined,
      status: statusFilter.value || undefined
    };
    const response = await axios.get('/api/v1/admin/community/groups', { params });
    groups.value = response.data;
  } catch (error) {
    console.error('获取小组列表失败:', error);
    ElMessage.error('获取小组列表失败');
  }
};

const viewGroupDetail = (group) => {
  selectedGroup.value = group;
  showDetailDialog.value = true;
};

const toggleGroupStatus = async (group) => {
  try {
    const newStatus = group.status === 1 ? 0 : 1;
    await axios.put(`/api/v1/admin/community/groups/${group.id}/status`, { status: newStatus });
    group.status = newStatus;
    ElMessage.success(newStatus === 1 ? '小组已启用' : '小组已禁用');
  } catch (error) {
    console.error('修改小组状态失败:', error);
    ElMessage.error('修改小组状态失败');
  }
};

const deleteGroup = async (groupId) => {
  ElMessageBox.confirm(
    '确定要删除这个小组吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await axios.delete(`/api/v1/admin/community/groups/${groupId}`);
      groups.value = groups.value.filter(g => g.id !== groupId);
      ElMessage.success('删除成功');
    } catch (error) {
      console.error('删除小组失败:', error);
      ElMessage.error('删除小组失败');
    }
  }).catch(() => {
    ElMessage.info('已取消删除');
  });
};

onMounted(() => {
  getGroups();
});
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  margin: 0;
  font-size: 18px;
}

.search-filter {
  margin-bottom: 20px;
}
</style>