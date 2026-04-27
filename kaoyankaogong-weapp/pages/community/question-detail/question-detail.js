Page({
  data: {
    questionId: null,
    question: {},
    answers: [],
    tagsArray: [],
    isLiked: false,
    showAnswerModal: false,
    answerContent: '',
    loading: false
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ questionId: options.id });
      this.loadQuestionDetail();
      this.loadAnswers();
    }
  },

  loadQuestionDetail() {
    this.setData({ loading: true });
    
    const app = getApp();
    wx.request({
      url: `${app.globalData.baseUrl}/community/questions/${this.data.questionId}`,
      method: 'GET',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const question = res.data;
          const tagsArray = question.tags ? question.tags.split(',') : [];
          question.author_name = '用户' + question.user_id;
          question.author_avatar = '/images/default-avatar.png';
          
          this.setData({ 
            question, 
            tagsArray,
            loading: false 
          });
        } else {
          wx.showToast({
            title: '加载失败',
            icon: 'none'
          });
          this.setData({ loading: false });
        }
      },
      fail: () => {
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        });
        this.setData({ loading: false });
      }
    });
  },

  loadAnswers() {
    const app = getApp();
    wx.request({
      url: `${app.globalData.baseUrl}/community/questions/${this.data.questionId}/answers`,
      method: 'GET',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const answers = (res.data || []).map(answer => {
            answer.author_name = '用户' + answer.user_id;
            answer.author_avatar = '/images/default-avatar.png';
            return answer;
          });
          this.setData({ answers });
        }
      }
    });
  },

  toggleLike() {
    const isLoggedIn = wx.getStorageSync('isLoggedIn');
    if (!isLoggedIn) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }

    const app = getApp();
    const method = this.data.isLiked ? 'DELETE' : 'POST';
    
    wx.request({
      url: `${app.globalData.baseUrl}/community/like?target_type=1&target_id=${this.data.questionId}`,
      method: method,
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const isLiked = !this.data.isLiked;
          const question = this.data.question;
          question.like_count = isLiked ? question.like_count + 1 : question.like_count - 1;
          
          this.setData({ 
            isLiked,
            question
          });
          
          wx.showToast({
            title: isLiked ? '点赞成功' : '取消点赞',
            icon: 'success'
          });
        }
      }
    });
  },

  showAnswerInput() {
    const isLoggedIn = wx.getStorageSync('isLoggedIn');
    if (!isLoggedIn) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }

    this.setData({ showAnswerModal: true });
  },

  hideAnswerInput() {
    this.setData({ 
      showAnswerModal: false,
      answerContent: ''
    });
  },

  onAnswerInput(e) {
    this.setData({ answerContent: e.detail.value });
  },

  submitAnswer() {
    if (!this.data.answerContent.trim()) {
      wx.showToast({
        title: '请输入回答内容',
        icon: 'none'
      });
      return;
    }

    const app = getApp();
    wx.request({
      url: `${app.globalData.baseUrl}/community/questions/${this.data.questionId}/answers`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      },
      data: {
        content: this.data.answerContent
      },
      success: (res) => {
        if (res.statusCode === 200) {
          wx.showToast({
            title: '回答成功',
            icon: 'success'
          });
          
          this.hideAnswerInput();
          this.loadAnswers();
          this.loadQuestionDetail();
        } else {
          wx.showToast({
            title: res.data.detail || '回答失败',
            icon: 'none'
          });
        }
      },
      fail: () => {
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        });
      }
    });
  },

  likeAnswer(e) {
    const answerId = e.currentTarget.dataset.id;
    const app = getApp();
    
    wx.request({
      url: `${app.globalData.baseUrl}/community/like?target_type=2&target_id=${answerId}`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          wx.showToast({
            title: '点赞成功',
            icon: 'success'
          });
          this.loadAnswers();
        }
      }
    });
  },

  showCommentInput(e) {
    wx.showToast({
      title: '评论功能开发中',
      icon: 'none'
    });
  },

  toggleSort() {
    wx.showToast({
      title: '排序功能开发中',
      icon: 'none'
    });
  },

  onShareAppMessage() {
    return {
      title: this.data.question.title,
      path: `/pages/community/question-detail/question-detail?id=${this.data.questionId}`
    };
  }
});
