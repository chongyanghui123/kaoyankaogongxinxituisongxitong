// index.js
const app = getApp()

Page({
  data: {
    carousels: [],
    loading: true,
    isLoggedIn: false,
    signInStatus: {
      has_signed_today: false,
      continuous_days: 0,
      total_points: 0,
      total_sign_days: 0
    }
  },

  onLoad() {
    this.checkLoginStatus()
    this.loadCarousels()
  },

  onShow() {
    this.checkLoginStatus()
    this.loadCarousels()
    if (this.data.isLoggedIn) {
      this.loadSignInStatus()
    }
  },

  checkLoginStatus() {
    const token = wx.getStorageSync('token')
    const isLoggedIn = !!token
    this.setData({ isLoggedIn })
  },

  async loadCarousels() {
    try {
      this.setData({ loading: true })
      
      const baseUrl = app.globalData.baseUrl
      const response = await new Promise((resolve, reject) => {
        wx.request({
          url: baseUrl + '/learning_materials/carousels/active',
          method: 'GET',
          header: { 'Content-Type': 'application/json' },
          timeout: 30000,
          success: (res) => resolve(res),
          fail: (err) => reject(err)
        })
      })

      if (response.statusCode === 200 && response.data && response.data.success && response.data.data) {
        const carousels = response.data.data.map(item => ({
          ...item,
          image_url: this.getFullImageUrl(item.image_url)
        }))
        this.setData({ 
          carousels: carousels,
          loading: false
        })
      } else {
        this.setData({ 
          carousels: [],
          loading: false
        })
      }
    } catch (error) {
      console.error('加载轮播图失败:', error)
      this.setData({ 
        carousels: [],
        loading: false
      })
    }
  },

  getFullImageUrl(url) {
    if (!url) return ''
    if (url.startsWith('http')) return url
    const baseUrl = app.globalData.baseUrl.replace('/api/v1', '')
    return baseUrl + url
  },

  async loadSignInStatus() {
    try {
      const response = await app.request({
        url: '/sign-in/sign-in/status',
        method: 'GET'
      })

      if (response.success && response.data) {
        this.setData({
          signInStatus: response.data
        })
      }
    } catch (error) {
      console.error('获取签到状态失败:', error)
    }
  },

  async handleSignIn() {
    if (this.data.signInStatus.has_signed_today) {
      wx.showToast({
        title: '今日已签到',
        icon: 'none'
      })
      return
    }

    try {
      wx.showLoading({ title: '签到中...' })
      
      const response = await app.request({
        url: '/sign-in/sign-in',
        method: 'POST'
      })

      wx.hideLoading()

      if (response.success) {
        wx.showToast({
          title: `签到成功 +${response.data.points_earned}积分`,
          icon: 'success'
        })
        
        this.setData({
          signInStatus: {
            ...this.data.signInStatus,
            has_signed_today: true,
            continuous_days: response.data.continuous_days,
            total_points: response.data.total_points,
            total_sign_days: (this.data.signInStatus.total_sign_days || 0) + 1
          }
        })
      } else {
        wx.showToast({
          title: response.message || '签到失败',
          icon: 'none'
        })
      }
    } catch (error) {
      wx.hideLoading()
      console.error('签到失败:', error)
      wx.showToast({
        title: '签到失败，请重试',
        icon: 'none'
      })
    }
  },

  goToLogin() {
    wx.navigateTo({
      url: '/pages/user/user'
    })
  },

  

  onPullDownRefresh() {
    Promise.all([
      this.loadCarousels(),
      this.data.isLoggedIn ? this.loadSignInStatus() : Promise.resolve()
    ]).then(() => {
      wx.stopPullDownRefresh()
    })
  },

  // 导航到互动社区
  navigateToCommunity(e) {
    const type = e.currentTarget.dataset.type
    if (type === 'groups') {
      wx.navigateTo({
        url: '/pages/community/groups/groups'
      })
    } else if (type === 'qa') {
      wx.navigateTo({
        url: '/pages/community/qa/qa'
      })
    }
  }
})
