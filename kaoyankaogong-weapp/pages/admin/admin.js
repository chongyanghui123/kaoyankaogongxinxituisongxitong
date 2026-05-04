// admin.js
Page({
  data: {
    stats: {
      userCount: 1234,
      vipCount: 567,
      infoCount: 890,
      pushCount: 2345
    }
  },
  
  onLoad() {
    // 页面加载时执行

    this.fetchSystemStats();
  },
  
  onShow() {
    // 页面显示时执行

  },
  
  // 获取系统统计数据
  async fetchSystemStats() {
    try {
      const app = getApp();
      
      // 调用API获取系统统计数据
      const response = await app.request({
        url: '/admin/stats'
      });
      
      if (response.success) {
        this.setData({
          stats: response.data
        });
      }
    } catch (error) {
      console.error('获取系统统计数据失败:', error);
      // 使用模拟数据
    }
  },
  
  // 导航到用户管理
  navigateToUserManagement() {
    wx.navigateTo({
      url: '/pages/admin/userManagement/userManagement'
    });
  },
  
  // 导航到情报管理
  navigateToInfoManagement() {
    wx.navigateTo({
      url: '/pages/admin/infoManagement/infoManagement'
    });
  },
  
  // 导航到推送管理
  navigateToPushManagement() {
    wx.navigateTo({
      url: '/pages/admin/pushManagement/pushManagement'
    });
  },
  
  // 导航到系统设置
  navigateToSystemSettings() {
    wx.navigateTo({
      url: '/pages/admin/systemSettings/systemSettings'
    });
  },
  
  // 触发考研情报推送
  async triggerKaoyanPush() {
    try {
      const app = getApp();
      
      wx.showLoading({ title: '推送中...' });
      
      // 调用API触发考研情报推送
      const response = await app.request({
        url: '/push/trigger/kaoyan',
        method: 'POST'
      });
      
      wx.hideLoading();
      
      if (response.success) {
        wx.showToast({
          title: '考研情报推送触发成功',
          icon: 'success'
        });
      } else {
        wx.showToast({
          title: '推送触发失败',
          icon: 'none'
        });
      }
    } catch (error) {
      wx.hideLoading();
      console.error('触发考研情报推送失败:', error);
      wx.showToast({
        title: '推送触发失败',
        icon: 'none'
      });
    }
  },
  
  // 触发考公情报推送
  async triggerKaogongPush() {
    try {
      const app = getApp();
      
      wx.showLoading({ title: '推送中...' });
      
      // 调用API触发考公情报推送
      const response = await app.request({
        url: '/push/trigger/kaogong',
        method: 'POST'
      });
      
      wx.hideLoading();
      
      if (response.success) {
        wx.showToast({
          title: '考公情报推送触发成功',
          icon: 'success'
        });
      } else {
        wx.showToast({
          title: '推送触发失败',
          icon: 'none'
        });
      }
    } catch (error) {
      wx.hideLoading();
      console.error('触发考公情报推送失败:', error);
      wx.showToast({
        title: '推送触发失败',
        icon: 'none'
      });
    }
  },
  
  // 触发到期提醒推送
  async triggerExpiryPush() {
    try {
      const app = getApp();
      
      wx.showLoading({ title: '推送中...' });
      
      // 调用API触发到期提醒推送
      const response = await app.request({
        url: '/push/trigger/expiry',
        method: 'POST'
      });
      
      wx.hideLoading();
      
      if (response.success) {
        wx.showToast({
          title: '到期提醒推送触发成功',
          icon: 'success'
        });
      } else {
        wx.showToast({
          title: '推送触发失败',
          icon: 'none'
        });
      }
    } catch (error) {
      wx.hideLoading();
      console.error('触发到期提醒推送失败:', error);
      wx.showToast({
        title: '推送触发失败',
        icon: 'none'
      });
    }
  }
});