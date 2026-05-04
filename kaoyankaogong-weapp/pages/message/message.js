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
    // 重新获取消息列表，确保消息及时更新
    this.setData({
      page: 1,
      messages: [],
      hasMore: true
    });
    this.fetchMessages();
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
        this.setData({
          messages: [],
          loading: false
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
  async markAsRead(id, read) {
    if (!read) {
      try {
        const app = getApp();
        
        // 调用API标记为已读
        const response = await app.request({
          url: `/message/read/${id}`,
          method: 'POST'
        });
        
        if (response.success) {
          // 更新本地数据，标记所有消息为已读（实现用户需求：点击一个消息，所有小红点消失）
          const messages = this.data.messages.map(message => {
            return { ...message, read: true };
          });
          
          this.setData({
            messages: messages
          });
        }
      } catch (error) {
        console.error('标记已读失败:', error);
      }
    }
  },

  // 删除消息
  async deleteMessage(e) {
    const messageId = e.currentTarget.dataset.messageId;
    
    // 显示删除确认对话框
    wx.showModal({
      title: '删除消息',
      content: '确定要删除这条消息吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            const app = getApp();
            
            // 调用API删除消息
            const response = await app.request({
              url: `/message/${messageId}`,
              method: 'DELETE'
            });
            
            if (response.success) {
              // 从本地数据中删除该消息
              const messages = this.data.messages.filter(msg => msg.id !== messageId);
              this.setData({
                messages: messages
              });
              
              wx.showToast({
                title: '删除成功',
                icon: 'success'
              });
            } else {
              wx.showToast({
                title: '删除失败',
                icon: 'error'
              });
            }
          } catch (error) {
            console.error('删除消息失败:', error);
            wx.showToast({
              title: '删除失败',
              icon: 'error'
            });
          }
        }
      }
    });
  },

  // 导航到详情或显示系统通知
  async navigateToDetail(e) {
    const infoId = e.currentTarget.dataset.id;
    const messageId = e.currentTarget.dataset.messageId;
    const read = e.currentTarget.dataset.read;
    const message = this.data.messages.find(msg => msg.id === messageId);
    
    // 先标记为已读
    await this.markAsRead(messageId, read);
    
    // 如果是系统通知、到期提醒或没有对应的情报ID，直接显示通知内容
    if (message && (message.type === 'system' || message.type === 'expiry' || infoId === 0)) {
      // 显示通知内容
      wx.showModal({
        title: message.type === 'expiry' ? '到期提醒' : '系统通知',
        content: message.content,
        showCancel: false,
        confirmText: '知道了'
      });
    } else if (infoId) {
      // 导航到情报详情页面
      wx.navigateTo({
        url: `/pages/detail/detail?id=${infoId}`
      });
    } else {
      // 没有情报ID，显示弹窗
      wx.showModal({
        title: '通知',
        content: message ? message.content : '暂无内容',
        showCancel: false,
        confirmText: '知道了'
      });
    }
  }
});