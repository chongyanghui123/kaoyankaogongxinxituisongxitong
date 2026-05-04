Page({
  data: {
    groupId: null,
    group: {},
    messages: [],
    inputText: '',
    scrollToView: '',
    loading: false,
    currentUserId: null,
    isMember: false,
    showJoinTip: false,
    socketConnected: false,
    reconnectTimer: null,
    reconnectCount: 0,
    members: [],
    showMemberPicker: false,
    mentionedUsers: []
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ groupId: parseInt(options.id) });
      
      const userInfo = wx.getStorageSync('userInfo');
      if (userInfo) {
        this.setData({ currentUserId: userInfo.id });
      }
      
      this.loadGroupInfo();
      this.checkMembership();
    }
  },

  onUnload() {
    this.closeSocket();
  },

  onShow() {
    if (this.data.groupId && this.data.isMember && !this.data.socketConnected) {
      this.connectSocket();
    }
  },

  onHide() {
    this.closeSocket();
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
            this.loadMembers();
            this.connectSocket();
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

  loadMembers() {
    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    
    wx.request({
      url: `${app.globalData.baseUrl}/community/groups/${this.data.groupId}/members`,
      method: 'GET',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const members = (res.data || [])
            .filter(m => m.status === 1)
            .map(m => ({
              user_id: m.user_id,
              username: m.username || '用户' + m.user_id,
              avatar: m.avatar || '/images/default-avatar.png'
            }));
          this.setData({ members });
        }
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
            const highlightedContent = this.highlightMentions(msg.content, msg.mentioned_users);
            return {
              id: msg.id,
              user_id: msg.user_id,
              senderName: msg.sender_name || '用户' + msg.user_id,
              avatar: msg.sender_avatar || '/images/default-avatar.png',
              message_type: msg.message_type,
              content: msg.content,
              highlightedContent: highlightedContent,
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

  connectSocket() {
    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    
    if (!token || this.data.socketConnected) {
      return;
    }

    const socketUrl = `ws://localhost:8000/ws/group/${this.data.groupId}?token=${token}`;
    
    wx.connectSocket({
      url: socketUrl,
      success: () => {
        console.log('WebSocket连接中...');
      },
      fail: (err) => {
        console.error('WebSocket连接失败:', err);
        this.reconnect();
      }
    });

    wx.onSocketOpen(() => {
      console.log('WebSocket连接已打开');
      this.setData({ 
        socketConnected: true,
        reconnectCount: 0
      });
    });

    wx.onSocketMessage((res) => {
      console.log('收到WebSocket消息:', res.data);
      try {
        const message = JSON.parse(res.data);
        this.handleSocketMessage(message);
      } catch (e) {
        console.error('解析消息失败:', e);
      }
    });

    wx.onSocketClose(() => {
      console.log('WebSocket连接已关闭');
      this.setData({ socketConnected: false });
      this.reconnect();
    });

    wx.onSocketError((err) => {
      console.error('WebSocket错误:', err);
      this.setData({ socketConnected: false });
    });
  },

  closeSocket() {
    if (this.data.reconnectTimer) {
      clearTimeout(this.data.reconnectTimer);
      this.setData({ reconnectTimer: null });
    }
    
    if (this.data.socketConnected) {
      wx.closeSocket();
      this.setData({ socketConnected: false });
    }
  },

  reconnect() {
    if (this.data.reconnectCount >= 5) {
      console.log('重连次数已达上限');
      return;
    }

    if (this.data.reconnectTimer) {
      clearTimeout(this.data.reconnectTimer);
    }

    const timer = setTimeout(() => {
      console.log('尝试重连WebSocket...');
      this.setData({ reconnectCount: this.data.reconnectCount + 1 });
      this.connectSocket();
    }, 3000);

    this.setData({ reconnectTimer: timer });
  },

  handleSocketMessage(message) {
    const { type, content, user_id, username, time, mentioned_users } = message;
    
    if (type === 'system') {
      const systemMsg = {
        id: Date.now(),
        user_id: 0,
        senderName: '系统',
        avatar: '/images/system-avatar.png',
        message_type: 0,
        content: content,
        time: this.formatTime(time),
        isSelf: false,
        isSystem: true
      };
      
      this.setData({
        messages: [...this.data.messages, systemMsg],
        scrollToView: `msg-${systemMsg.id}`
      });
      
    } else if (type === 'chat' || type === 'image') {
      const isSelf = user_id === this.data.currentUserId;
      const highlightedContent = this.highlightMentions(content, mentioned_users);
      const newMsg = {
        id: Date.now(),
        user_id: user_id,
        senderName: username || '用户' + user_id,
        avatar: '/images/default-avatar.png',
        message_type: type === 'image' ? 2 : 1,
        content: content,
        highlightedContent: highlightedContent,
        image_url: type === 'image' ? content : null,
        time: this.formatTime(time),
        isSelf: isSelf
      };
      
      this.setData({
        messages: [...this.data.messages, newMsg],
        scrollToView: `msg-${newMsg.id}`
      });
    }
  },

  onInput(e) {
    this.setData({ inputText: e.detail.value });
  },

  sendMessage() {
    if (!this.data.inputText.trim()) {
      return;
    }

    const content = this.data.inputText.trim();
    const mentionedUsers = this.parseMentions(content);
    
    if (this.data.socketConnected) {
      // 使用WebSocket发送
      wx.sendSocketMessage({
        data: JSON.stringify({
          type: 'chat',
          content: content,
          mentioned_users: mentionedUsers
        }),
        success: () => {
          this.setData({ 
            inputText: '',
            mentionedUsers: []
          });
        },
        fail: (err) => {
          console.error('发送消息失败:', err);
          wx.showToast({
            title: '发送失败',
            icon: 'none'
          });
        }
      });
    } else {
      // 降级为HTTP请求
      this.sendMessageViaHttp(content, mentionedUsers);
    }
  },

  sendMessageViaHttp(content, mentionedUsers = []) {
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
    if (this.data.socketConnected) {
      wx.sendSocketMessage({
        data: JSON.stringify({
          type: 'image',
          content: imageUrl
        }),
        success: () => {
          console.log('图片消息发送成功');
        },
        fail: (err) => {
          console.error('发送图片消息失败:', err);
        }
      });
    } else {
      // 降级为HTTP请求
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
          content: imageUrl
        },
        success: (res) => {
          if (res.statusCode === 200) {
            this.loadMessages();
          }
        }
      });
    }
  },

  formatTime(timeStr) {
    if (!timeStr) return '';
    
    const date = new Date(timeStr);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) {
      return '刚刚';
    } else if (diff < 3600000) {
      return Math.floor(diff / 60000) + '分钟前';
    } else if (diff < 86400000) {
      return Math.floor(diff / 3600000) + '小时前';
    } else {
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      const hour = date.getHours().toString().padStart(2, '0');
      const minute = date.getMinutes().toString().padStart(2, '0');
      return `${month}-${day} ${hour}:${minute}`;
    }
  },

  leaveGroup() {
    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    
    wx.showModal({
      title: '确认退出',
      content: '确定要退出该小组吗？',
      success: (res) => {
        if (res.confirm) {
          wx.request({
            url: `${app.globalData.baseUrl}/community/groups/${this.data.groupId}/leave`,
            method: 'POST',
            header: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            success: (res) => {
              if (res.statusCode === 200) {
                wx.showToast({
                  title: '已退出小组',
                  icon: 'success'
                });
                this.closeSocket();
                setTimeout(() => {
                  wx.navigateBack();
                }, 1500);
              } else {
                wx.showToast({
                  title: res.data.detail || '退出失败',
                  icon: 'none'
                });
              }
            }
          });
        }
      }
    });
  },

  showMemberPicker() {
    this.setData({ showMemberPicker: true });
  },

  hideMemberPicker() {
    this.setData({ showMemberPicker: false });
  },

  selectMember(e) {
    const userId = e.currentTarget.dataset.userId;
    const username = e.currentTarget.dataset.username;
    
    let inputText = this.data.inputText;
    let mentionedUsers = [...this.data.mentionedUsers];
    
    if (!mentionedUsers.includes(userId)) {
      mentionedUsers.push(userId);
      inputText += `@${username} `;
    }
    
    this.setData({ 
      inputText,
      mentionedUsers,
      showMemberPicker: false
    });
  },

  parseMentions(content) {
    const mentionedUsers = [];
    const members = this.data.members;
    
    members.forEach(member => {
      if (content.includes(`@${member.username}`)) {
        mentionedUsers.push(member.user_id);
      }
    });
    
    return mentionedUsers;
  },

  highlightMentions(content, mentionedUsers) {
    if (!content) return content;
    if (!mentionedUsers || mentionedUsers.length === 0) {
      const mentionRegex = /@[\u4e00-\u9fa5\w]+/g;
      return content.replace(mentionRegex, '<span class="mention">$&</span>');
    }
    
    let highlighted = content;
    const members = this.data.members;
    
    mentionedUsers.forEach(userId => {
      const member = members.find(m => m.user_id === userId);
      if (member) {
        const regex = new RegExp(`@${member.username}`, 'g');
        highlighted = highlighted.replace(regex, `<span class="mention">@${member.username}</span>`);
      }
    });
    
    return highlighted;
  },

  onShareAppMessage() {
    return {
      title: `加入${this.data.group.name || '学习小组'}，一起学习吧！`,
      path: `/pages/community/group-detail/group-detail?id=${this.data.groupId}`
    };
  }
});
