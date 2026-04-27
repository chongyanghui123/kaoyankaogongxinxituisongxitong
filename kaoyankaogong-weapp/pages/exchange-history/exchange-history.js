const app = getApp()

Page({
  data: {
    records: [],
    loading: true,
    page: 1,
    pageSize: 20
  },

  onLoad() {
    this.loadRecords()
  },

  async loadRecords() {
    try {
      this.setData({ loading: true })
      
      const response = await app.request({
        url: '/exchanges',
        method: 'GET',
        data: {
          page: this.data.page,
          page_size: this.data.pageSize
        }
      })

      if (response.success && response.data) {
        const records = response.data.items.map(item => ({
          ...item,
          gift_image: this.getFullImageUrl(item.gift_image),
          created_at: this.formatTime(item.created_at)
        }))
        
        this.setData({
          records: records,
          loading: false
        })
      } else {
        this.setData({
          records: [],
          loading: false
        })
      }
    } catch (error) {
      console.error('加载兑换记录失败:', error)
      this.setData({
        records: [],
        loading: false
      })
    }
  },

  formatTime(time) {
    if (!time) return '-'
    const date = new Date(time)
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
  },

  getFullImageUrl(url) {
    if (!url) return ''
    if (url.startsWith('http')) return url
    return 'http://localhost:8000' + url
  },

  onPullDownRefresh() {
    this.setData({ page: 1 })
    this.loadRecords().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  onReachBottom() {
    this.setData({
      page: this.data.page + 1
    })
    this.loadRecords()
  }
})
