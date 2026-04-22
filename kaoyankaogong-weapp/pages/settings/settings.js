// pages/settings/settings.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    cacheSize: '0.0MB',
    themeIndex: 0,
    themeOptions: [
      { name: '默认主题', value: 'default' },
      { name: '深色主题', value: 'dark' },
      { name: '护眼模式', value: 'eye' }
    ],
    pushFrequencyOptions: [
      { value: 'hourly', label: '每小时' },
      { value: 'daily', label: '每天' },
      { value: 'weekly', label: '每周' }
    ],
    pushFrequencyIndex: 1, // 默认每天
    pushTimeIndex: 0,
    pushTimeOptions: [
      { time: '08:00', label: '08:00' },
      { time: '09:00', label: '09:00' },
      { time: '10:00', label: '10:00' },
      { time: '11:00', label: '11:00' },
      { time: '12:00', label: '12:00' },
      { time: '13:00', label: '13:00' },
      { time: '14:00', label: '14:00' },
      { time: '15:00', label: '15:00' },
      { time: '16:00', label: '16:00' },
      { time: '17:00', label: '17:00' },
      { time: '18:00', label: '18:00' },
      { time: '19:00', label: '19:00' },
      { time: '20:00', label: '20:00' },
      { time: '21:00', label: '21:00' },
      { time: '22:00', label: '22:00' }
    ]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.calculateCacheSize();
    
    // 读取本地存储中的主题设置
    const savedTheme = wx.getStorageSync('systemTheme');
    if (savedTheme) {
      // 查找对应的主题索引
      const themeIndex = this.data.themeOptions.findIndex(option => option.value === savedTheme);
      if (themeIndex !== -1) {
        this.setData({
          themeIndex: themeIndex,
          theme: savedTheme
        });
      }
    } else {
      // 默认使用浅色主题
      this.setData({
        theme: 'default'
      });
    }
    
    // 调用后端API获取服务器上的推送设置
    this.getPushSettings();
  },
  
  // 调用后端API获取推送设置
  async getPushSettings() {
    try {
      const app = getApp();
      const token = wx.getStorageSync('token');
      
      // 调用获取订阅配置API
      const response = await app.request({
        url: '/users/subscription',
        method: 'GET',
        header: {
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (response.success && response.data.config) {
        // 获取服务器上的推送配置
        const serverPushConfig = response.data.config.push || {};
        
        // 更新推送频率设置
        if (serverPushConfig.frequency) {
          const pushFrequencyIndex = this.data.pushFrequencyOptions.findIndex(option => option.value === serverPushConfig.frequency);
          if (pushFrequencyIndex !== -1) {
            this.setData({
              pushFrequencyIndex: pushFrequencyIndex
            });
            // 保存到本地存储
            wx.setStorageSync('pushFrequency', serverPushConfig.frequency);
          }
        }
        
        // 更新推送时间设置
        if (serverPushConfig.time) {
          const pushTimeIndex = this.data.pushTimeOptions.findIndex(option => option.time === serverPushConfig.time);
          if (pushTimeIndex !== -1) {
            this.setData({
              pushTimeIndex: pushTimeIndex
            });
            // 保存到本地存储
            wx.setStorageSync('pushTime', serverPushConfig.time);
          }
        }
      }
    } catch (error) {
      console.error('获取推送设置失败:', error);
      // 从本地存储读取备用设置
      this.getLocalPushSettings();
    }
  },
  
  // 从本地存储读取推送设置
  getLocalPushSettings() {
    // 读取本地存储中的推送频率设置
    const savedPushFrequency = wx.getStorageSync('pushFrequency');
    if (savedPushFrequency) {
      const pushFrequencyIndex = this.data.pushFrequencyOptions.findIndex(option => option.value === savedPushFrequency);
      if (pushFrequencyIndex !== -1) {
        this.setData({
          pushFrequencyIndex: pushFrequencyIndex
        });
      }
    }
    
    // 读取本地存储中的推送时间设置
    const savedPushTime = wx.getStorageSync('pushTime');
    if (savedPushTime) {
      const pushTimeIndex = this.data.pushTimeOptions.findIndex(option => option.time === savedPushTime);
      if (pushTimeIndex !== -1) {
        this.setData({
          pushTimeIndex: pushTimeIndex
        });
      }
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },

  // 切换信息推送频率
  changePushFrequency(e) {
    const index = e.detail.value;
    const pushFrequency = this.data.pushFrequencyOptions[index].value;
    
    this.setData({
      pushFrequencyIndex: index
    });
    
    // 保存设置到本地存储
    wx.setStorageSync('pushFrequency', pushFrequency);
    
    // 调用后端API更新推送频率设置
    this.updatePushFrequency(pushFrequency);
    
    // 显示切换成功提示
    wx.showToast({
      title: '推送频率已设置为' + this.data.pushFrequencyOptions[index].label,
      icon: 'success'
    });
  },
  
  // 切换信息推送时间
  changePushTime(e) {
    const index = e.detail.value;
    const pushTime = this.data.pushTimeOptions[index].time;
    
    this.setData({
      pushTimeIndex: index
    });
    
    // 保存设置到本地存储
    wx.setStorageSync('pushTime', pushTime);
    
    // 调用后端API更新推送时间设置
    this.updatePushTime(pushTime);
    
    // 显示切换成功提示
    wx.showToast({
      title: '推送时间已设置为' + pushTime,
      icon: 'success'
    });
  },
  
  // 调用后端API更新推送频率
  async updatePushFrequency(pushFrequency) {
    try {
      const app = getApp();
      const token = wx.getStorageSync('token');
      
      // 调用更新订阅配置API
      const response = await app.request({
        url: '/users/subscription',
        method: 'PUT',
        data: {
          subscribe_type: 3, // 默认双赛道
          config: {
            kaoyan: {},
            kaogong: {},
            push: {
              frequency: pushFrequency,
              time: wx.getStorageSync('pushTime') || '08:00'
            }
          }
        },
        header: {
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (response.success) {
        console.log('推送频率更新成功');
      } else {
        console.error('推送频率更新失败:', response.message);
      }
    } catch (error) {
      console.error('推送频率更新失败:', error);
    }
  },
  
  // 调用后端API更新推送时间
  async updatePushTime(pushTime) {
    try {
      const app = getApp();
      const token = wx.getStorageSync('token');
      
      // 调用更新订阅配置API
      const response = await app.request({
        url: '/users/subscription',
        method: 'PUT',
        data: {
          subscribe_type: 3, // 默认双赛道
          config: {
            kaoyan: {},
            kaogong: {},
            push: {
              frequency: wx.getStorageSync('pushFrequency') || 'daily',
              time: pushTime
            }
          }
        },
        header: {
          'Authorization': 'Bearer ' + token
        }
      });
      
      if (response.success) {
        console.log('推送时间更新成功');
      } else {
        console.error('推送时间更新失败:', response.message);
      }
    } catch (error) {
      console.error('推送时间更新失败:', error);
    }
  },

  // 切换系统主题
  changeTheme(e) {
    const index = e.detail.value;
    const theme = this.data.themeOptions[index].value;
    
    this.setData({
      themeIndex: index,
      theme: theme
    });
    
    // 调用全局主题切换方法
    const app = getApp();
    app.changeTheme(theme);
    
    // 显示切换成功提示
    wx.showToast({
      title: '主题已切换为' + this.data.themeOptions[index].name,
      icon: 'success'
    });
  },

  // 导航到修改密码页面
  navigateToChangePassword() {
    wx.navigateTo({
      url: '../change-password/change-password'
    });
  },

  // 导航到找回密码页面
  navigateToForgotPassword() {
    wx.navigateTo({
      url: '../forgot-password/forgot-password'
    });
  },

  // 计算缓存大小
  calculateCacheSize() {
    wx.getStorageInfo({
      success: (res) => {
        let cacheSize = res.currentSize / 1024;
        this.setData({
          cacheSize: cacheSize.toFixed(1) + 'MB'
        });
      }
    });
  },

  // 清除缓存
  clearCache() {
    wx.showModal({
      title: '确认清除',
      content: '确定要清除所有缓存吗？',
      success: (res) => {
        if (res.confirm) {
          wx.clearStorageSync();
          this.setData({
            cacheSize: '0.0MB'
          });
          wx.showToast({
            title: '缓存已清除',
            icon: 'success'
          });
        }
      }
    });
  },

  // 显示关于信息
  showAbout() {
    wx.showModal({
      title: '关于系统',
      content: '考研考公双赛道情报监控系统\n\n版本：v1.0.0\n\n功能：提供考研和考公相关的最新资讯、学习资料和考试信息\n\n开发者：情报监控团队',
      showCancel: false
    });
  },

  // 退出登录
  logout() {
    wx.showModal({
      title: '确认退出',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          // 清除登录状态
          wx.removeStorageSync('token');
          wx.removeStorageSync('userInfo');
          // 跳转到登录页面
          wx.reLaunch({
            url: '../user/user'
          });
        }
      }
    });
  }
})