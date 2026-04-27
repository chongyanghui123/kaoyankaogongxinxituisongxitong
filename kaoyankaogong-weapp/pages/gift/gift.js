const app = getApp()

Page({
  data: {
    gifts: [],
    userPoints: 0,
    loading: true
  },

  onLoad() {
    this.loadData()
  },

  onShow() {
    this.loadData()
  },

  async loadData() {
    await Promise.all([
      this.loadGifts(),
      this.loadUserPoints()
    ])
  },

  async loadGifts() {
    try {
      this.setData({ loading: true })
      
      const response = await app.request({
        url: '/gifts',
        method: 'GET'
      })

      if (response.success && response.data) {
        const gifts = response.data.map(item => ({
          ...item,
          image_url: this.getFullImageUrl(item.image_url)
        }))
        this.setData({
          gifts: gifts,
          loading: false
        })
      } else {
        this.setData({
          gifts: [],
          loading: false
        })
      }
    } catch (error) {
      console.error('加载礼品列表失败:', error)
      this.setData({
        gifts: [],
        loading: false
      })
    }
  },

  async loadUserPoints() {
    try {
      const response = await app.request({
        url: '/sign-in/sign-in/status',
        method: 'GET'
      })

      if (response.success && response.data) {
        this.setData({
          userPoints: response.data.total_points || 0
        })
      }
    } catch (error) {
      console.error('获取用户积分失败:', error)
    }
  },

  async handleExchange(e) {
    const item = e.currentTarget.dataset.item
    
    if (this.data.userPoints < item.points_required) {
      wx.showToast({
        title: '积分不足',
        icon: 'none'
      })
      return
    }

    if (item.stock <= 0) {
      wx.showToast({
        title: '库存不足',
        icon: 'none'
      })
      return
    }

    wx.showModal({
      title: '确认兑换',
      content: `确定使用 ${item.points_required} 积分兑换「${item.name}」吗？`,
      success: async (res) => {
        if (res.confirm) {
          await this.doExchange(item.id)
        }
      }
    })
  },

  async doExchange(giftId) {
    try {
      wx.showLoading({ title: '兑换中...' })
      
      const response = await app.request({
        url: `/gifts/${giftId}/exchange`,
        method: 'POST'
      })

      wx.hideLoading()

      if (response.success) {
        wx.showToast({
          title: '兑换成功',
          icon: 'success'
        })
        
        this.loadData()
      } else if (response.data && response.data.need_address) {
        wx.showModal({
          title: '提示',
          content: '请先在设置页面填写收货地址',
          confirmText: '去设置',
          success: (res) => {
            if (res.confirm) {
              wx.navigateTo({
                url: '/pages/settings/settings'
              })
            }
          }
        })
      } else {
        wx.showToast({
          title: response.message || '兑换失败',
          icon: 'none'
        })
      }
    } catch (error) {
      wx.hideLoading()
      console.error('兑换失败:', error)
      wx.showToast({
        title: '兑换失败，请重试',
        icon: 'none'
      })
    }
  },

  getFullImageUrl(url) {
    if (!url) return ''
    if (url.startsWith('http')) return url
    return 'http://localhost:8000' + url
  },

  goToExchangeHistory() {
    wx.navigateTo({
      url: '/pages/exchange-history/exchange-history'
    })
  },

  onPullDownRefresh() {
    this.loadData().then(() => {
      wx.stopPullDownRefresh()
    })
  }
})
