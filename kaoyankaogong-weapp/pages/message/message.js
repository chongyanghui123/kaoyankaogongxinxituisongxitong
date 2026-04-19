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
    console.log('消息中心页加载');
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
    console.log('消息中心页显示');
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
        const newData = response.data.items;
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