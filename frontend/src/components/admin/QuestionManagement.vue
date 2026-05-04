<template>
  <div class="admin-content">
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <h3 class="title">问答管理</h3>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <div class="search-filter">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input
              v-model="searchQuery"
              placeholder="搜索问题标题"
              clearable
              prefix-icon="Search"
              @keyup.enter="getQuestions"
            >
              <template #append>
                <el-button type="primary" @click="getQuestions">搜索</el-button>
              </template>
            </el-input>
          </el-col>
          <el-col :span="8">
            <el-select v-model="categoryFilter" placeholder="按分类筛选" clearable @change="getQuestions">
              <el-option label="全部" value="" />
              <el-option label="考研" value="考研" />
              <el-option label="公务员" value="公务员" />
              <el-option label="数学" value="数学" />
              <el-option label="英语" value="英语" />
              <el-option label="政治" value="政治" />
              <el-option label="专业课" value="专业课" />
            </el-select>
          </el-col>
          <el-col :span="8">
            <el-select v-model="statusFilter" placeholder="按状态筛选" clearable @change="getQuestions">
              <el-option label="全部" value="" />
              <el-option label="正常" value="1" />
              <el-option label="待审核" value="0" />
              <el-option label="已关闭" value="2" />
            </el-select>
          </el-col>
        </el-row>
      </div>
      
      <!-- 问题表格 -->
      <el-table 
        ref="questionTable" 
        :data="questions" 
        style="width: 100%" 
        border 
        :empty-text="emptyText"
        :show-header="true"
      >
        <el-table-column type="index" label="序号" width="60" :index="(index) => index + 1" />
        <el-table-column prop="title" label="问题标题" width="200" :show-overflow-tooltip="true" />
        <el-table-column prop="category" label="分类" width="100" align="center" />
        <el-table-column prop="view_count" label="浏览量" width="80" align="center" />
        <el-table-column prop="answer_count" label="回答数" width="80" align="center" />
        <el-table-column prop="like_count" label="点赞数" width="80" align="center" />
        <el-table-column prop="created_at" label="提问时间" width="160" />
        <el-table-column label="状态" width="90" align="center">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewQuestionDetail(scope.row)">详情</el-button>
            <el-button 
              type="success" 
              size="small" 
              @click="approveQuestion(scope.row)"
              v-if="scope.row.status === 0"
            >
              通过
            </el-button>
            <el-button 
              type="warning" 
              size="small" 
              @click="rejectQuestion(scope.row)"
              v-if="scope.row.status === 0"
            >
              拒绝
            </el-button>
            <el-button type="danger" size="small" @click="deleteQuestion(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 问题详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="问题详情"
      width="700px"
    >
      <div v-if="selectedQuestion" class="question-detail">
        <h4>{{ selectedQuestion.title }}</h4>
        <div class="detail-info">
          <span class="info-item">分类：{{ selectedQuestion.category }}</span>
          <span class="info-item">浏览量：{{ selectedQuestion.view_count }}</span>
          <span class="info-item">回答数：{{ selectedQuestion.answer_count }}</span>
          <span class="info-item">点赞数：{{ selectedQuestion.like_count }}</span>
          <span class="info-item">提问者ID：{{ selectedQuestion.user_id }}</span>
          <span class="info-item">提问时间：{{ selectedQuestion.created_at }}</span>
        </div>
        <div class="content-section">
          <h5>问题内容：</h5>
          <p>{{ selectedQuestion.content }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import axios from '../../utils/axios';

const questionTable = ref(null);
const questions = ref([]);
const searchQuery = ref('');
const categoryFilter = ref('');
const statusFilter = ref('');
const showDetailDialog = ref(false);
const selectedQuestion = ref(null);
const emptyText = '暂无数据';

const getQuestions = async () => {
  try {
    const params = {
      search: searchQuery.value || undefined,
      category: categoryFilter.value || undefined,
      status: statusFilter.value || undefined
    };
    const response = await axios.get('/api/v1/admin/community/questions', { params });
    questions.value = response.data;
  } catch (error) {
    console.error('获取问题列表失败:', error);
    ElMessage.error('获取问题列表失败');
  }
};

const getStatusType = (status) => {
  switch (status) {
    case 1: return 'success';
    case 0: return 'warning';
    case 2: return 'danger';
    default: return 'info';
  }
};

const getStatusText = (status) => {
  switch (status) {
    case 1: return '正常';
    case 0: return '待审核';
    case 2: return '已关闭';
    default: return '未知';
  }
};

const viewQuestionDetail = (question) => {
  selectedQuestion.value = question;
  showDetailDialog.value = true;
};

const approveQuestion = async (question) => {
  try {
    await axios.put(`/api/v1/admin/community/questions/${question.id}/approve`);
    question.status = 1;
    ElMessage.success('审核通过');
  } catch (error) {
    console.error('审核失败:', error);
    ElMessage.error('审核失败');
  }
};

const rejectQuestion = async (question) => {
  try {
    await axios.put(`/api/v1/admin/community/questions/${question.id}/reject`);
    question.status = 2;
    ElMessage.success('已拒绝');
  } catch (error) {
    console.error('拒绝失败:', error);
    ElMessage.error('拒绝失败');
  }
};

const deleteQuestion = async (questionId) => {
  ElMessageBox.confirm(
    '确定要删除这个问题吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await axios.delete(`/api/v1/admin/community/questions/${questionId}`);
      questions.value = questions.value.filter(q => q.id !== questionId);
      ElMessage.success('删除成功');
    } catch (error) {
      console.error('删除问题失败:', error);
      ElMessage.error('删除问题失败');
    }
  }).catch(() => {
    ElMessage.info('已取消删除');
  });
};

onMounted(() => {
  getQuestions();
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

.question-detail {
  padding: 10px;
}

.question-detail h4 {
  margin-bottom: 15px;
  font-size: 16px;
  color: #333;
}

.detail-info {
  margin-bottom: 20px;
}

.info-item {
  display: inline-block;
  margin-right: 20px;
  margin-bottom: 10px;
  padding: 5px 10px;
  background: #f5f7fa;
  border-radius: 4px;
  font-size: 14px;
}

.content-section h5 {
  margin-bottom: 10px;
  font-size: 14px;
  color: #666;
}

.content-section p {
  padding: 15px;
  background: #fafafa;
  border-radius: 4px;
  line-height: 1.8;
}
</style>