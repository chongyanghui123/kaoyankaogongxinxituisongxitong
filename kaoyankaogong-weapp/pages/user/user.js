// user.js
Page({
  data: {
    userInfo: null,
    phone: '',
    password: ''
  },
  
  onLoad() {
    // 页面加载时执行

    this.getUserInfo();
  },
  
  onShow() {
    // 页面显示时执行

    this.getUserInfo();
  },
  
  // 获取用户信息
  getUserInfo() {
    const app = getApp();
    // 从全局数据中获取用户信息
    let userInfo = app.globalData.userInfo;
    
    // 如果全局数据中没有用户信息，从本地存储中读取
    if (!userInfo) {
      userInfo = wx.getStorageSync('userInfo');
      // 如果本地存储中有用户信息，更新全局数据
      if (userInfo) {
        app.globalData.userInfo = userInfo;
      }
    }
    
    // 确保userInfo对象中有is_vip_active字段
    if (userInfo && userInfo.is_vip !== undefined) {
      userInfo.is_vip_active = userInfo.is_vip;
    }
    
    this.setData({
      userInfo: userInfo
    });
  },
  
  // 手机号输入
  bindPhoneInput(e) {
    this.setData({
      phone: e.detail.value
    });
  },
  
  // 密码输入
  bindPasswordInput(e) {
    this.setData({
      password: e.detail.value
    });
  },
  

  
  // 登录
  async login() {
    const { phone, password } = this.data;
    
    if (!phone || !password) {
      wx.showToast({
        title: '请输入手机号和密码',
        icon: 'none'
      });
      return;
    }
    
    const app = getApp();
    try {
      const result = await app.login(phone, password);
      if (result) {
        this.setData({
          userInfo: app.globalData.userInfo
        });
        wx.showToast({
          title: '登录成功',
          icon: 'success'
        });
        
        // 跳转到首页
        wx.navigateTo({
          url: '/pages/index/index'
        });
      }
    } catch (error) {
      console.error('登录失败:', error);
      console.error('错误详情:', JSON.stringify(error));
      wx.showToast({
        title: '登录失败，请重试',
        icon: 'none'
      });
    }
  },
  
  // 退出登录
  logout() {
    const app = getApp();
    app.logout();
    this.setData({
      userInfo: null
    });
  },
  
  // 导航到订阅管理
  navigateToSubscription() {
    if (!this.data.userInfo) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }
    
    wx.navigateTo({
      url: '/pages/subscription/subscription'
    });
  },
  
  // 导航到消息中心
  navigateToMessage() {
    if (!this.data.userInfo) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }
    
    wx.navigateTo({
      url: '/pages/message/message'
    });
  },
  
  // 导航到我的收藏
  navigateToCollection() {
    if (!this.data.userInfo) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }
    
    wx.navigateTo({
      url: '/pages/collection/collection'
    });
  },
  
  // 导航到设置
  navigateToSettings() {
    if (!this.data.userInfo) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }
    
    wx.navigateTo({
      url: '/pages/settings/settings'
    });
  },

  // 导航到学习资料
  navigateToLearningMaterials() {
    if (!this.data.userInfo) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }
    
    wx.navigateTo({
      url: '/pages/learning-materials/learning-materials'
    });
  },

  // 导航到个人中心
  navigateToPersonalCenter() {
    if (!this.data.userInfo) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }
    
    wx.navigateTo({
      url: '/pages/personal-center/personal-center'
    });
  },
  
  // 导航到后台管理
  navigateToAdmin() {
    wx.navigateTo({
      url: '/pages/admin/admin'
    });
  }
});