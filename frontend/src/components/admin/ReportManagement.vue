<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">举报处理</h3>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索举报内容"
              clearable
              prefix-icon="Search"
              @keyup.enter="getReports"
            >
              <template #append>
                <el-button type="primary" @click="getReports">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="8">
            <el-select v-model="typeFilter" placeholder="按举报类型筛选" clearable @change="getReports">
              <el-option label="全部" value="" />
              <el-option label="小组" value="group" />
              <el-option label="帖子" value="post" />
              <el-option label="问题" value="question" />
              <el-option label="回答" value="answer" />
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-select v-model="statusFilter" placeholder="按处理状态筛选" clearable @change="getReports">
              <el-option label="全部" value="" />
              <el-option label="待处理" value="0" />
              <el-option label="已处理" value="1" />
              <el-option label="已忽略" value="2" />
            </el-select>
          </el-col>
        </el-row>
      </div>
      
      <!-- 举报表格 -->
      <el-table 
        ref="reportTable" 
        :data="reports" 
        style="width: 100%" 
        border 
        :empty-text="emptyText"
        :show-header="true"
      >
        <el-table-column type="index" label="序号" width="60" :index="(index) => index + 1" />
        <el-table-column prop="report_type" label="举报类型" width="100" align="center">
          <template #default="scope">
            <el-tag :type="getTypeTagType(scope.row.report_type)">
              {{ getTypeText(scope.row.report_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="target_title" label="目标标题" width="180" :show-overflow-tooltip="true" />
        <el-table-column prop="content" label="举报内容" width="200" :show-overflow-tooltip="true" />
        <el-table-column prop="reason" label="举报原因" width="110" align="center">
          <template #default="scope">
            <el-tag type="warning">{{ getReasonText(scope.row.reason) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="举报时间" width="160" />
        <el-table-column label="处理状态" width="100" align="center">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewReportDetail(scope.row)">详情</el-button>
            <el-button 
              type="success" 
              size="small" 
              @click="handleReport(scope.row, 1)"
              v-if="scope.row.status === 0"
            >
              处理
            </el-button>
            <el-button 
              type="warning" 
              size="small" 
              @click="handleReport(scope.row, 2)"
              v-if="scope.row.status === 0"
            >
              忽略
            </el-button>
            <el-button 
              type="info" 
              size="small" 
              @click="viewReportedContent(scope.row)"
            >
              查看内容
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 举报详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="举报详情"
      width="700px"
    >
      <div v-if="selectedReport" class="report-detail">
        <div class="detail-row">
          <span class="label">举报类型：</span>
          <span class="value">{{ getTypeText(selectedReport.report_type) }}</span>
        </div>
        <div class="detail-row">
          <span class="label">目标ID：</span>
          <span class="value">{{ selectedReport.target_id }}</span>
        </div>
        <div class="detail-row">
          <span class="label">目标标题：</span>
          <span class="value">{{ selectedReport.target_title }}</span>
        </div>
        <div class="detail-row">
          <span class="label">举报原因：</span>
          <span class="value">{{ getReasonText(selectedReport.reason) }}</span>
        </div>
        <div class="detail-row">
          <span class="label">举报人ID：</span>
          <span class="value">{{ selectedReport.reporter_id }}</span>
        </div>
        <div class="detail-row">
          <span class="label">举报时间：</span>
          <span class="value">{{ selectedReport.created_at }}</span>
        </div>
        <div class="detail-row">
          <span class="label">处理状态：</span>
          <span class="value">{{ getStatusText(selectedReport.status) }}</span>
        </div>
        <div class="detail-row">
          <span class="label">处理结果：</span>
          <span class="value">{{ selectedReport.handler_note || '暂无' }}</span>
        </div>
        <div class="content-section">
          <span class="label">举报内容：</span>
          <p>{{ selectedReport.content }}</p>
        </div>
      </div>
    </el-dialog>

    <!-- 处理对话框 -->
    <el-dialog
      v-model="showHandleDialog"
      title="处理举报"
      width="500px"
    >
      <el-form :model="handleForm" label-width="80px">
        <el-form-item label="处理结果">
          <el-select v-model="handleForm.result" placeholder="请选择处理结果">
            <el-option label="删除内容" value="delete" />
            <el-option label="警告用户" value="warning" />
            <el-option label="封禁账号" value="ban" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="处理备注">
          <el-input
            v-model="handleForm.note"
            type="textarea"
            placeholder="请输入处理备注"
            :rows="4"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showHandleDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmHandle">确定处理</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from '../../utils/axios';

const reportTable = ref(null);
const reports = ref([]);
const searchQuery = ref('');
const typeFilter = ref('');
const statusFilter = ref('');
const showDetailDialog = ref(false);
const showHandleDialog = ref(false);
const selectedReport = ref(null);
const emptyText = '暂无数据';
const handleForm = reactive({
  result: '',
  note: ''
});

const getReports = async () => {
  try {
    const params = {
      search: searchQuery.value || undefined,
      type: typeFilter.value || undefined,
      status: statusFilter.value || undefined
    };
    const response = await axios.get('/api/v1/admin/community/reports', { params });
    reports.value = response.data;
  } catch (error) {
    console.error('获取举报列表失败:', error);
    ElMessage.error('获取举报列表失败');
  }
};

const getTypeTagType = (type) => {
  switch (type) {
    case 'group': return 'primary';
    case 'post': return 'success';
    case 'question': return 'warning';
    case 'answer': return 'info';
    default: return 'info';
  }
};

const getTypeText = (type) => {
  switch (type) {
    case 'group': return '小组';
    case 'post': return '帖子';
    case 'question': return '问题';
    case 'answer': return '回答';
    default: return '未知';
  }
};

const getReasonText = (reason) => {
  switch (reason) {
    case 'spam': return '垃圾信息';
    case 'inappropriate': return '内容不当';
    case 'violent': return '暴力内容';
    case 'illegal': return '违法违规';
    case 'other': return '其他';
    default: return reason || '未知';
  }
};

const getStatusType = (status) => {
  switch (status) {
    case 1: return 'success';
    case 0: return 'warning';
    case 2: return 'info';
    default: return 'info';
  }
};

const getStatusText = (status) => {
  switch (status) {
    case 1: return '已处理';
    case 0: return '待处理';
    case 2: return '已忽略';
    default: return '未知';
  }
};

const viewReportDetail = (report) => {
  selectedReport.value = report;
  showDetailDialog.value = true;
};

const handleReport = (report, action) => {
  selectedReport.value = report;
  handleForm.result = '';
  handleForm.note = '';
  showHandleDialog.value = action === 1;
  if (action === 2) {
    ElMessageBox.confirm(
      '确定要忽略这个举报吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(async () => {
      try {
        await axios.put(`/api/v1/admin/community/reports/${report.id}`, { status: 2, handler_note: '已忽略' });
        report.status = 2;
        ElMessage.success('已忽略');
      } catch (error) {
        console.error('忽略举报失败:', error);
        ElMessage.error('忽略举报失败');
      }
    }).catch(() => {
      ElMessage.info('已取消');
    });
  }
};

const confirmHandle = async () => {
  if (!handleForm.result) {
    ElMessage.warning('请选择处理结果');
    return;
  }
  
  try {
    await axios.put(`/api/v1/admin/community/reports/${selectedReport.value.id}`, {
      status: 1,
      handler_note: `${handleForm.result === 'delete' ? '删除内容' : handleForm.result === 'warning' ? '警告用户' : handleForm.result === 'ban' ? '封禁账号' : '其他'}${handleForm.note ? ` - ${handleForm.note}` : ''}`
    });
    selectedReport.value.status = 1;
    selectedReport.value.handler_note = handleForm.handler_note;
    showHandleDialog.value = false;
    ElMessage.success('处理成功');
  } catch (error) {
    console.error('处理举报失败:', error);
    ElMessage.error('处理举报失败');
  }
};

const viewReportedContent = (report) => {
  ElMessage.info(`正在查看${getTypeText(report.report_type)}内容，ID: ${report.target_id}`);
};

onMounted(() => {
  getReports();
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

.report-detail {
  padding: 10px;
}

.detail-row {
  margin-bottom: 10px;
  font-size: 14px;
}

.detail-row .label {
  display: inline-block;
  width: 100px;
  font-weight: bold;
  color: #666;
}

.detail-row .value {
  color: #333;
}

.content-section {
  margin-top: 20px;
}

.content-section .label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: #666;
}

.content-section p {
  padding: 15px;
  background: #fafafa;
  border-radius: 4px;
  line-height: 1.8;
}
</style>