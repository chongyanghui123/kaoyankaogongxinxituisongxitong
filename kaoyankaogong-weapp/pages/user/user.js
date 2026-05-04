Page({
  data: {
    userInfo: null,
    bindPhone: '',
    bindCode: '',
    countdown: 0,
    showBindPhone: false
  },

  onLoad() {
    this.getUserInfo();
  },

  onShow() {
    this.getUserInfo();
  },

  async getUserInfo() {
    const app = getApp();
    
    // 尝试从服务器获取最新用户信息
    try {
      await app.fetchUserInfo();
    } catch (error) {
      console.error('获取用户信息失败:', error);
      // 如果获取失败，使用缓存数据
      let userInfo = app.globalData.userInfo;
      if (!userInfo) {
        userInfo = wx.getStorageSync('userInfo');
        if (userInfo) {
          app.globalData.userInfo = userInfo;
        }
      }
    }

    let userInfo = app.globalData.userInfo;
    if (userInfo && userInfo.is_vip !== undefined) {
      userInfo.is_vip_active = userInfo.is_vip;
    }

    this.setData({
      userInfo: userInfo,
      showBindPhone: userInfo && !userInfo.phone_bound
    });
  },

  bindPhoneNoInput(e) {
    this.setData({ bindPhone: e.detail.value });
  },

  bindCodeInput(e) {
    this.setData({ bindCode: e.detail.value });
  },

  async wechatLogin() {
    const app = getApp();
    try {
      wx.showLoading({ title: '登录中...' });
      const result = await app.wechatLogin();
      wx.hideLoading();

      if (result && result.success) {
        this.setData({
          userInfo: app.globalData.userInfo,
          showBindPhone: !result.phone_bound
        });
        wx.showToast({ title: '登录成功', icon: 'success' });

        if (!app.globalData.userInfo.is_vip) {
          setTimeout(() => {
            wx.showModal({
              title: '欢迎使用',
              content: '您当前为普通用户，可使用学习小组、问答、礼品兑换等功能。升级VIP可解锁情报推送等高级功能，是否前往查看？',
              confirmText: '去看看',
              cancelText: '以后再说',
              success: (res) => {
                if (res.confirm) {
                  wx.navigateTo({ url: '/pages/subscription/subscription' });
                }
              }
            });
          }, 1500);
        }
      }
    } catch (error) {
      wx.hideLoading();
      wx.showToast({
        title: error.message || '微信登录失败',
        icon: 'none'
      });
    }
  },

  async sendBindCode() {
    const { bindPhone, countdown } = this.data;
    if (countdown > 0) return;
    if (!bindPhone || bindPhone.length !== 11) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' });
      return;
    }
    const app = getApp();
    try {
      wx.showLoading({ title: '发送中...' });
      await app.sendPhoneCode(bindPhone, 'bind_phone');
      wx.hideLoading();
      wx.showToast({ title: '验证码已发送', icon: 'success' });
      this.startCountdown();
    } catch (error) {
      wx.hideLoading();
      wx.showToast({ title: error.message || '发送失败', icon: 'none' });
    }
  },

  startCountdown() {
    this.setData({ countdown: 60 });
    const timer = setInterval(() => {
      const current = this.data.countdown;
      if (current <= 1) {
        clearInterval(timer);
        this.setData({ countdown: 0 });
      } else {
        this.setData({ countdown: current - 1 });
      }
    }, 1000);
  },

  async bindPhoneSubmit() {
    const { bindPhone, bindCode } = this.data;
    if (!bindPhone || bindPhone.length !== 11) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' });
      return;
    }
    if (!bindCode) {
      wx.showToast({ title: '请输入验证码', icon: 'none' });
      return;
    }
    const app = getApp();
    try {
      wx.showLoading({ title: '绑定中...' });
      await app.bindPhone(bindPhone, bindCode);
      wx.hideLoading();
      this.setData({
        userInfo: app.globalData.userInfo,
        showBindPhone: false
      });
      wx.showToast({ title: '绑定成功', icon: 'success' });
    } catch (error) {
      wx.hideLoading();
      wx.showToast({ title: error.message || '绑定失败', icon: 'none' });
    }
  },

  logout() {
    const app = getApp();
    app.logout();
    this.setData({
      userInfo: null,
      showBindPhone: false
    });
  },

  navigateToSubscription() {
    if (!this.data.userInfo) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    wx.navigateTo({ url: '/pages/subscription/subscription' });
  },

  navigateToMessage() {
    if (!this.data.userInfo) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    wx.navigateTo({ url: '/pages/message/message' });
  },

  navigateToCollection() {
    if (!this.data.userInfo) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    wx.navigateTo({ url: '/pages/collection/collection' });
  },

  navigateToFeedback() {
    if (!this.data.userInfo) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    wx.navigateTo({ url: '/pages/feedback/feedback' });
  },

  navigateToSettings() {
    if (!this.data.userInfo) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    wx.navigateTo({ url: '/pages/settings/settings' });
  },

  navigateToLearningMaterials() {
    if (!this.data.userInfo) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    wx.navigateTo({ url: '/pages/learning-materials/learning-materials' });
  },

  navigateToGift() {
    if (!this.data.userInfo) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    wx.navigateTo({ url: '/pages/gift/gift' });
  },

  navigateToPersonalCenter() {
    if (!this.data.userInfo) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    wx.navigateTo({ url: '/pages/personal-center/personal-center' });
  },

  navigateToAdmin() {
    wx.navigateTo({ url: '/pages/admin/admin' });
  }
});
