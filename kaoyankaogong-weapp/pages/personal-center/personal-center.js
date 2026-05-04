// personal-center.js
const app = getApp()

Page({
  data: {
    userInfo: null
  },

  onLoad() {
    this.getUserInfo()
  },

  onShow() {
    // 每次页面显示时更新用户信息
    this.getUserInfo()
  },

  // 获取用户详细信息
  getUserInfo() {
    if (!app.globalData.token) {
      wx.redirectTo({ url: '/pages/user/user' })
      return
    }

    wx.showLoading({ title: '加载中...' })
    wx.request({
      url: app.globalData.baseUrl + '/users/profile',
      method: 'GET',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token
      },
      success: (res) => {
        wx.hideLoading()

        
        // 检查返回数据格式并转换
        let userData = res.data
        
        // 如果返回的是标准API格式（有data字段）
        if (userData && userData.success && userData.data) {
          userData = userData.data
        }
        
        // 确保数据格式符合页面显示要求
        const formattedData = {
          username: userData.username || '',
          email: userData.email || '',
          phone: userData.phone || '',
          real_name: userData.real_name || '',
          avatar: userData.avatar || '',
          is_vip: userData.is_vip || false,
          vip_type: userData.vip_type || 0,
          vip_end_time: userData.vip_end_time ? userData.vip_end_time : '',
          created_at: userData.created_at ? userData.created_at : '',
          kaoyan_requirements: userData.kaoyan_requirements || {},
          kaogong_requirements: userData.kaogong_requirements || {}
        }
        
        console.log('用户信息数据:', userData);
        console.log('格式化后的用户信息:', formattedData);
        this.setData({
          userInfo: formattedData
        })
      },
      fail: (err) => {
        wx.hideLoading()
        console.error('获取用户信息失败:', err)
        wx.showToast({ title: '获取用户信息失败', icon: 'none' })
      }
    })
  },

  // 返回上一页
  navigateBack() {
    wx.navigateBack()
  },

  // 跳转到续费页面
  navigateToRenewal() {
    wx.navigateTo({
      url: '/pages/renewal/renewal'
    })
  }
})
