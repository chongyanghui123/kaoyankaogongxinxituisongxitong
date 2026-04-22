// feedback.js
const app = getApp();

Page({
  data: {
    // 反馈类型
    feedbackTypes: ['功能建议', '问题反馈', '其他'],
    feedbackTypeIndex: 0,
    // 反馈内容
    content: '',
    // 联系方式
    contact: '',
    // 加载状态
    loading: false,
    // 历史反馈
    feedbackHistory: [],
    // 分页参数
    page: 1,
    pageSize: 10,
    // 是否还有更多数据
    hasMore: true,
    // 加载历史反馈的状态
    loadingHistory: false
  },

  onLoad() {
    // 加载历史反馈
    this.getFeedbackHistory();
  },

  // 绑定反馈类型变化
  bindFeedbackTypeChange(e) {
    this.setData({
      feedbackTypeIndex: e.detail.value
    });
  },

  // 绑定反馈内容输入
  bindContentInput(e) {
    this.setData({
      content: e.detail.value
    });
  },

  // 绑定联系方式输入
  bindContactInput(e) {
    this.setData({
      contact: e.detail.value
    });
  },

  // 提交反馈
  async submitFeedback() {
    const { feedbackTypeIndex, content, contact } = this.data;
    
    // 验证内容
    if (!content.trim()) {
      wx.showToast({
        title: '请输入反馈内容',
        icon: 'none'
      });
      return;
    }
    
    // 验证联系方式（如果填写）
    if (contact.trim()) {
      const phoneRegex = /^1[3-9]\d{9}$/;
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      
      if (!phoneRegex.test(contact.trim()) && !emailRegex.test(contact.trim())) {
        wx.showToast({
          title: '请输入有效的手机号或邮箱',
          icon: 'none'
        });
        return;
      }
    }
    
    this.setData({ loading: true });
    
    try {
      // 提交反馈
      const res = await app.request({
        url: '/feedback',
        method: 'POST',
        data: {
          type: parseInt(feedbackTypeIndex) + 1, // 类型从1开始
          content: content.trim(),
          contact: contact.trim()
        }
      });
      
      if (res.success) {
        wx.showToast({
          title: '反馈提交成功',
          icon: 'success'
        });
        
        // 清空表单
        this.setData({
          feedbackTypeIndex: 0,
          content: '',
          contact: '',
          feedbackHistory: [],
          page: 1,
          hasMore: true
        });
        
        // 重新加载历史反馈
        this.getFeedbackHistory();
      } else {
        wx.showToast({
          title: res.message || '提交失败，请重试',
          icon: 'none'
        });
      }
    } catch (error) {
      console.error('提交反馈失败:', error);
      wx.showToast({
        title: '网络请求失败',
        icon: 'none'
      });
    } finally {
      this.setData({ loading: false });
    }
  },

  // 获取历史反馈
  async getFeedbackHistory(loadMore = false) {
    // 如果正在加载，则返回
    if (this.data.loadingHistory) {
      return;
    }

    // 如果不是加载更多，且没有更多数据，且已有数据，则返回
    if (!loadMore && !this.data.hasMore && this.data.feedbackHistory.length > 0) {
      return;
    }

    this.setData({ loadingHistory: true });

    try {
      const res = await app.request({
        url: '/feedback',
        method: 'GET',
        data: {
          page: loadMore ? this.data.page + 1 : 1,
          pageSize: this.data.pageSize
        }
      });
      
      if (res.success) {
        const newData = res.data || [];
        let feedbackHistory = this.data.feedbackHistory;
        
        if (loadMore) {
          feedbackHistory = [...feedbackHistory, ...newData];
          this.setData({
            page: this.data.page + 1
          });
        } else {
          feedbackHistory = newData;
          this.setData({
            page: 1
          });
        }

        this.setData({
          feedbackHistory: feedbackHistory,
          hasMore: newData.length >= this.data.pageSize
        });
      }
    } catch (error) {
      console.error('获取历史反馈失败:', error);
    } finally {
      this.setData({ loadingHistory: false });
    }
  },

  // 下拉加载更多
  onReachBottom() {
    if (this.data.hasMore && !this.data.loadingHistory) {
      this.getFeedbackHistory(true);
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.setData({
      page: 1,
      hasMore: true
    });
    this.getFeedbackHistory(false);
    wx.stopPullDownRefresh();
  },

  // 撤回反馈
  async withdrawFeedback(e) {
    const feedbackId = e.currentTarget.dataset.id;
    
    wx.showModal({
      title: '确认撤回',
      content: '确定要撤回这条反馈吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            const result = await app.request({
              url: `/feedback/${feedbackId}/withdraw`,
              method: 'PUT'
            });
            
            if (result.success) {
              wx.showToast({
                title: '撤回成功',
                icon: 'success'
              });
              
              // 重置参数并重新加载历史反馈
              this.setData({
                feedbackHistory: [],
                page: 1,
                hasMore: true
              });
              this.getFeedbackHistory();
            } else {
              wx.showToast({
                title: result.message || '撤回失败',
                icon: 'none'
              });
            }
          } catch (error) {
            console.error('撤回反馈失败:', error);
            wx.showToast({
              title: '网络请求失败',
              icon: 'none'
            });
          }
        }
      }
    });
  },

  // 删除反馈
  async deleteFeedback(e) {
    const feedbackId = e.currentTarget.dataset.id;
    
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这条反馈吗？删除后将无法恢复。',
      success: async (res) => {
        if (res.confirm) {
          try {
            const result = await app.request({
              url: `/feedback/${feedbackId}`,
              method: 'DELETE'
            });
            
            if (result.success) {
              wx.showToast({
                title: '删除成功',
                icon: 'success'
              });
              
              // 重置参数并重新加载历史反馈
              this.setData({
                feedbackHistory: [],
                page: 1,
                hasMore: true
              });
              this.getFeedbackHistory();
            } else {
              wx.showToast({
                title: result.message || '删除失败',
                icon: 'none'
              });
            }
          } catch (error) {
            console.error('删除反馈失败:', error);
            wx.showToast({
              title: '网络请求失败',
              icon: 'none'
            });
          }
        }
      }
    });
  },

  // 返回上一页
  goBack() {
    wx.navigateBack();
  }
});