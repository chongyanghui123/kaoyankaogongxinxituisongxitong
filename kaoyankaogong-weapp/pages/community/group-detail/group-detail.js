Page({
  data: {
    groupId: null,
    group: {},
    messages: [],
    inputText: '',
    scrollToView: '',
    loading: false,
    currentUserId: null,
    pollTimer: null,
    isMember: false,
    showJoinTip: false
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ groupId: options.id });
      
      const userInfo = wx.getStorageSync('userInfo');
      if (userInfo) {
        this.setData({ currentUserId: userInfo.id });
      }
      
      this.loadGroupInfo();
      this.checkMembership();
    }
  },

  onUnload() {
    this.stopPolling();
  },

  onShow() {
    if (this.data.groupId && this.data.isMember) {
      this.loadMessages();
    }
  },

  loadGroupInfo() {
    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    
    wx.request({
      url: `${app.globalData.baseUrl}/community/groups/${this.data.groupId}`,
      method: 'GET',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const group = res.data;
          wx.setNavigationBarTitle({
            title: group.name
          });
          this.setData({ group });
        }
      }
    });
  },

  checkMembership() {
    const app = getApp();
    const userInfo = wx.getStorageSync('userInfo');
    const token = app.globalData.token || wx.getStorageSync('token');
    
    if (!userInfo || !token) {
      this.setData({ 
        isMember: false,
        showJoinTip: true 
      });
      return;
    }

    wx.request({
      url: `${app.globalData.baseUrl}/community/groups/${this.data.groupId}/members`,
      method: 'GET',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const members = res.data || [];
          const isMember = members.some(member => member.user_id === userInfo.id && member.status === 1);
          
          this.setData({ 
            isMember,
            showJoinTip: !isMember
          });
          
          if (isMember) {
            this.loadMessages();
            this.startPolling();
          }
        } else {
          this.setData({ 
            isMember: false,
            showJoinTip: true 
          });
        }
      },
      fail: () => {
        this.setData({ 
          isMember: false,
          showJoinTip: true 
        });
      }
    });
  },

  joinGroup() {
    const isLoggedIn = wx.getStorageSync('isLoggedIn');
    if (!isLoggedIn) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      setTimeout(() => {
        wx.navigateTo({
          url: '/pages/user/user'
        });
      }, 1500);
      return;
    }

    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    
    wx.request({
      url: `${app.globalData.baseUrl}/community/groups/${this.data.groupId}/join`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          wx.showToast({
            title: '加入成功',
            icon: 'success',
            duration: 2000
          });
          
          // 延迟刷新状态，让用户看到提示
          setTimeout(() => {
            this.checkMembership();
          }, 1000);
        } else {
          wx.showToast({
            title: res.data.detail || '加入失败',
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

  loadMessages() {
    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    
    wx.request({
      url: `${app.globalData.baseUrl}/community/groups/${this.data.groupId}/messages`,
      method: 'GET',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const messages = (res.data || []).map(msg => {
            const isSelf = msg.user_id === this.data.currentUserId;
            return {
              id: msg.id,
              user_id: msg.user_id,
              senderName: msg.sender_name || '用户' + msg.user_id,
              avatar: msg.sender_avatar || '/images/default-avatar.png',
              message_type: msg.message_type,
              content: msg.content,
              image_url: msg.image_url,
              time: this.formatTime(msg.created_at),
              isSelf: isSelf
            };
          });
          
          this.setData({ messages });
          
          if (messages.length > 0) {
            this.setData({
              scrollToView: `msg-${messages[messages.length - 1].id}`
            });
          }
        }
      }
    });
  },

  startPolling() {
    this.stopPolling();
    
    this.data.pollTimer = setInterval(() => {
      this.loadMessages();
    }, 3000);
  },

  stopPolling() {
    if (this.data.pollTimer) {
      clearInterval(this.data.pollTimer);
      this.data.pollTimer = null;
    }
  },

  onInput(e) {
    this.setData({ inputText: e.detail.value });
  },

  sendMessage() {
    if (!this.data.inputText.trim()) {
      return;
    }

    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    const content = this.data.inputText.trim();
    
    wx.request({
      url: `${app.globalData.baseUrl}/community/groups/${this.data.groupId}/messages`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      data: {
        message_type: 1,
        content: content
      },
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({ inputText: '' });
          this.loadMessages();
        } else {
          wx.showToast({
            title: res.data.detail || '发送失败',
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

  chooseImage() {
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFilePath = res.tempFilePaths[0];
        this.uploadAndSendImage(tempFilePath);
      }
    });
  },

  uploadAndSendImage(filePath) {
    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    
    wx.uploadFile({
      url: `${app.globalData.baseUrl}/community/upload`,
      filePath: filePath,
      name: 'file',
      header: {
        'Authorization': `Bearer ${token}`
      },
      success: (res) => {
        const data = JSON.parse(res.data);
        if (data.url) {
          this.sendImageMessage(data.url);
        } else {
          wx.showToast({
            title: '上传失败',
            icon: 'none'
          });
        }
      },
      fail: () => {
        wx.showToast({
          title: '上传失败',
          icon: 'none'
        });
      }
    });
  },

  sendImageMessage(imageUrl) {
    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    
    wx.request({
      url: `${app.globalData.baseUrl}/community/groups/${this.data.groupId}/messages`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      data: {
        message_type: 2,
        image_url: imageUrl
      },
      success: (res) => {
        if (res.statusCode === 200) {
          this.loadMessages();
        } else {
          wx.showToast({
            title: res.data.detail || '发送失败',
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

  previewImage(e) {
    const url = e.currentTarget.dataset.url;
    wx.previewImage({
      urls: [url],
      current: url
    });
  },

  formatTime(timeStr) {
    const time = new Date(timeStr);
    const now = new Date();
    const diff = now - time;
    
    if (diff < 60000) {
      return '刚刚';
    } else if (diff < 3600000) {
      return Math.floor(diff / 60000) + '分钟前';
    } else if (diff < 86400000) {
      return Math.floor(diff / 3600000) + '小时前';
    } else {
      const hour = time.getHours().toString().padStart(2, '0');
      const minute = time.getMinutes().toString().padStart(2, '0');
      return `${hour}:${minute}`;
    }
  },

  onPullDownRefresh() {
    this.loadMessages();
    wx.stopPullDownRefresh();
  }
});
