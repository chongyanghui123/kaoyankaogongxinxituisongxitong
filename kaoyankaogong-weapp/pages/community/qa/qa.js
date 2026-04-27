// qa.js
Page({
  data: {
    // 问题分类
    categories: ['全部', '考研', '公务员', '数学', '英语', '政治', '专业课'],
    activeCategory: '全部',
    // 问题数据
    questions: [],
    // 加载状态
    loading: false,
    // 错误信息
    error: ''
  },

  onLoad() {
    // 页面加载时的初始化逻辑
    console.log('问答板块页面加载');
    this.loadQuestions();
  },

  onShow() {
    // 页面显示时的逻辑
    console.log('问答板块页面显示');
  },

  // 加载问题数据
  loadQuestions() {
    this.setData({ loading: true, error: '' });
    
    // 构建请求参数
    const category = this.data.activeCategory === '全部' ? '' : this.data.activeCategory;
    const url = `http://localhost:8000/api/v1/community/questions${category ? `?category=${encodeURIComponent(category)}` : ''}`;
    
    // 调用后端API获取问题列表
    wx.request({
      url: url,
      method: 'GET',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      },
      success: (res) => {
        console.log('获取问题列表成功:', res.data);
        // 直接使用返回的数组
        const questions = (res.data || []).map(question => ({
          id: question.id,
          title: question.title,
          content: question.content,
          views: question.view_count,
          answers: question.answer_count,
          likes: question.like_count,
          author: '用户' + question.user_id, // 模拟用户名
          avatar: question.title.charAt(0), // 模拟头像
          time: this.formatTime(question.created_at)
        }));
        this.setData({ questions });
      },
      fail: (err) => {
        console.error('获取问题列表失败:', err);
        this.setData({ error: '网络错误，请稍后重试' });
      },
      complete: () => {
        this.setData({ loading: false });
      }
    });
  },

  // 格式化时间
  formatTime(timestamp) {
    const now = new Date();
    const date = new Date(timestamp);
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return '刚刚';
    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    if (days < 7) return `${days}天前`;
    return date.toLocaleDateString();
  },

  // 导航到问题详情页
  navigateToQuestionDetail(e) {
    const questionId = e.currentTarget.dataset.id || 1; // 默认使用第一个问题的ID
    wx.navigateTo({
      url: `/pages/community/question-detail/question-detail?id=${questionId}`
    });
  },

  // 提问
  askQuestion() {
    // 检查用户是否登录
    const isLoggedIn = wx.getStorageSync('isLoggedIn');
    if (!isLoggedIn) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }

    // 跳转到提问页面
    wx.navigateTo({
      url: '/pages/community/ask-question/ask-question'
    });
  },

  // 切换分类
  switchCategory(e) {
    const category = e.currentTarget.dataset.category;
    this.setData({
      activeCategory: category
    });
    // 根据分类重新加载问题
    this.loadQuestions();
  },

  // 搜索问题
  searchQuestion(e) {
    const keyword = e.detail.value;
    // 这里可以根据关键词搜索问题
    console.log('搜索关键词:', keyword);
  }
});