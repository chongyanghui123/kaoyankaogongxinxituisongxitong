// message.js
Page({
  data: {
    activeTab: 'all',
    messages: [],
    hasMore: true,
    page: 1,
    pageSize: 10,
    userInfo: null
  },
  
  onLoad() {
    // 页面加载时执行

    this.getUserInfo();
    this.fetchMessages();
  },
  
  // 获取用户信息
  getUserInfo() {
    const app = getApp();
    const userInfo = app.globalData.userInfo;
    
    if (userInfo) {
      this.setData({
        userInfo: userInfo
      });
    }
  },
  
  onShow() {
    // 页面显示时执行

    // 重新获取用户信息，确保用户类型的变化能够及时反映
    this.getUserInfo();
  },
  
  // 切换标签
  switchTab(e) {
    const tab = e.currentTarget.dataset.tab;
    this.setData({
      activeTab: tab,
      page: 1,
      messages: []
    });
    this.fetchMessages();
  },
  
  // 格式化时间
  formatTime(timeStr) {
    // 处理 ISO 格式的时间字符串
    if (timeStr && typeof timeStr === 'string') {
      // 替换 'T' 为空格
      timeStr = timeStr.replace('T', ' ');
      // 移除毫秒部分
      if (timeStr.includes('.')) {
        timeStr = timeStr.split('.')[0];
      }
    }
    return timeStr;
  },

  // 获取消息列表
  async fetchMessages() {
    try {
      const app = getApp();
      
      // 检查用户是否登录
      if (!app.globalData.userInfo) {
        // 用户未登录，跳转到登录页面
        wx.showToast({
          title: '请先登录',
          icon: 'none'
        });
        
        wx.navigateTo({
          url: '/pages/user/user'
        });
        
        return;
      }
      
      // 构建请求参数
      const params = {
        tab: this.data.activeTab,
        page: this.data.page,
        page_size: this.data.pageSize
      };
      
      // 调用API获取消息列表
      const response = await app.request({
        url: '/message/list',
        data: params
      });
      
      if (response.success) {
        const newData = response.data.items.map(item => ({
          ...item,
          time: this.formatTime(item.time)
        }));
        const hasMore = response.data.total > this.data.messages.length + newData.length;
        
        this.setData({
          messages: this.data.page === 1 ? newData : [...this.data.messages, ...newData],
          hasMore: hasMore
        });
      }
    } catch (error) {
      console.error('获取消息列表失败:', error);
    }
  },
  
  // 加载更多
  loadMore() {
    if (this.data.hasMore) {
      this.setData({
        page: this.data.page + 1
      });
      this.fetchMessages();
    }
  },
  
  // 标记为已读
  async markAsRead(e) {
    const id = e.currentTarget.dataset.id;
    const read = e.currentTarget.dataset.read;
    
    if (!read) {
      try {
        const app = getApp();
        
        // 调用API标记为已读
        const response = await app.request({
          url: `/message/read/${id}`,
          method: 'POST'
        });
        
        if (response.success) {
          // 更新本地数据
          const messages = this.data.messages.map(message => {
            if (message.id === id) {
              return { ...message, read: true };
            }
            return message;
          });
          
          this.setData({
            messages: messages
          });
        }
      } catch (error) {
        console.error('标记已读失败:', error);
      }
    }
  }
});