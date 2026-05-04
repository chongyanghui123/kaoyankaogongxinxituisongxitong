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
    },
    examCountdowns: [],
    dailyPractice: null,
    currentCategory: 'kaoyan',
    selectedOption: null,
    submitted: false,
    showAnswerFlag: false,
    isCorrect: false,
    hotList: [],
    rankList: [],
    showRankModal: false,
    fullRankList: []
  },

  onLoad() {
    this.checkLoginStatus()
    this.loadCarousels()
    this.loadExamCountdowns()
    this.loadDailyPractice()
    this.loadHotList()
    this.loadRankList()
  },

  onShow() {
    this.checkLoginStatus()
    this.loadCarousels()
    if (this.data.isLoggedIn) {
      this.loadSignInStatus()
    }
    this.loadExamCountdowns()
    this.loadDailyPractice(this.data.currentCategory)
    this.loadHotList()
    this.loadRankList()
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
  },

  // 导航到礼品兑换
  navigateToGift() {
    if (!this.data.isLoggedIn) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      })
      return
    }
    
    wx.navigateTo({
      url: '/pages/gift/gift'
    })
  },

  // 加载备考倒计时
  async loadExamCountdowns() {
    try {
      const response = await app.request({
        url: '/utils/exam-countdowns',
        method: 'GET'
      })

      if (response.success && response.data) {
        this.setData({ examCountdowns: response.data })
      } else {
        this.setDefaultCountdowns()
      }
    } catch (error) {
      console.error('加载倒计时失败:', error)
      this.setDefaultCountdowns()
    }
  },

  setDefaultCountdowns() {
    this.setData({ examCountdowns: [] })
  },

  calculateDays(dateStr) {
    const target = new Date(dateStr)
    const now = new Date()
    const diff = target - now
    return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)))
  },

  // 加载每日一练
  async loadDailyPractice(category = 'all') {
    try {
      const response = await app.request({
        url: `/utils/daily-practice?category=${category}`,
        method: 'GET'
      })

      if (response.success && response.data) {
        const dailyPractice = response.data
        
        // 如果用户已经回答过，设置相应状态
        if (dailyPractice.has_answered) {
          this.setData({
            dailyPractice: dailyPractice,
            selectedOption: this.getOptionIndexByLabel(dailyPractice.user_answer),
            submitted: true,
            isCorrect: dailyPractice.is_correct,
            showAnswerFlag: false
          })
        } else {
          this.setData({
            dailyPractice: dailyPractice,
            selectedOption: null,
            submitted: false,
            isCorrect: false,
            showAnswerFlag: false
          })
        }
      } else {
        this.setDefaultPractice(category)
      }
    } catch (error) {
      console.error('加载每日一练失败:', error)
      this.setDefaultPractice(category)
    }
  },

  // 根据选项标签找到对应的索引
  getOptionIndexByLabel(label) {
    if (!this.data.dailyPractice || !this.data.dailyPractice.options) {
      return -1
    }
    return this.data.dailyPractice.options.findIndex(option => option.label === label)
  },

  setDefaultPractice(category = 'all') {
    this.setData({ 
      dailyPractice: null,
      selectedOption: null,
      submitted: false,
      showAnswerFlag: false,
      isCorrect: false
    })
  },

  selectOption(e) {
    const index = e.currentTarget.dataset.index
    this.setData({ selectedOption: index })
  },

  // 切换分类
  switchCategory(e) {
    const category = e.currentTarget.dataset.category
    if (this.data.currentCategory === category) {
      return
    }
    
    this.setData({ currentCategory: category })
    this.loadDailyPractice(category)
  },

  // 提交答案
  async submitAnswer() {
    // 检查是否登录
    if (!this.data.isLoggedIn) {
      wx.showModal({
        title: '提示',
        content: '请先登录后再答题，登录后可获得积分奖励',
        confirmText: '去登录',
        cancelText: '取消',
        success: (res) => {
          if (res.confirm) {
            wx.navigateTo({
              url: '/pages/user/user'
            })
          }
        }
      })
      return
    }

    // 检查是否已经回答过
    if (this.data.dailyPractice && this.data.dailyPractice.has_answered) {
      wx.showModal({
        title: '提示',
        content: '您今天已经回答过该题目了，明天再来吧！',
        showCancel: false,
        confirmText: '知道了'
      })
      return
    }

    if (this.data.selectedOption === null) {
      wx.showToast({
        title: '请选择一个答案',
        icon: 'none'
      })
      return
    }

    if (this.data.submitted) {
      wx.showToast({
        title: '您已经回答过了',
        icon: 'none'
      })
      return
    }

    const selectedOption = this.data.dailyPractice.options[this.data.selectedOption]
    
    try {
      wx.showLoading({ title: '提交答案中...' })
      
      const response = await app.request({
        url: '/utils/daily-practice/answer',
        method: 'POST',
        data: {
          practice_id: this.data.dailyPractice.id,
          user_answer: selectedOption.label
        }
      })

      wx.hideLoading()

      if (response.success && response.data) {
        // 检查是否已经回答过
        if (response.data.already_answered) {
          wx.showModal({
            title: '提示',
            content: '您今天已经回答过该题目了，明天再来吧！',
            showCancel: false,
            confirmText: '知道了'
          })
          
          // 更新状态
          this.setData({
            submitted: true,
            isCorrect: response.data.is_correct,
            showAnswerFlag: false,
            selectedOption: this.getOptionIndexByLabel(response.data.user_answer)
          })
          
          // 更新每日一练状态
          if (this.data.dailyPractice) {
            this.setData({
              'dailyPractice.has_answered': true,
              'dailyPractice.is_correct': response.data.is_correct,
              'dailyPractice.user_answer': response.data.user_answer
            })
          }
          return
        }

        this.setData({
          submitted: true,
          isCorrect: response.data.is_correct,
          showAnswerFlag: false
        })

        // 根据回答结果显示不同的提示
        if (response.data.is_correct) {
          // 答对：显示成功弹窗
          wx.showModal({
            title: '🎉 回答正确！',
            content: `恭喜您获得 ${response.data.score} 个积分！\n\n当前总积分：${response.data.total_points}`,
            showCancel: false,
            confirmText: '太棒了'
          })
          
          // 更新用户积分
          this.setData({
            'signInStatus.total_points': response.data.total_points
          })

          // 更新每日一练状态
          if (this.data.dailyPractice) {
            this.setData({
              'dailyPractice.has_answered': true,
              'dailyPractice.is_correct': true,
              'dailyPractice.user_answer': selectedOption.label
            })
          }
        } else {
          // 答错：显示错误弹窗
          wx.showModal({
            title: '😢 回答错误',
            content: `不要灰心，明天继续加油！`,
            showCancel: false,
            confirmText: '知道了'
          })

          // 更新每日一练状态
          if (this.data.dailyPractice) {
            this.setData({
              'dailyPractice.has_answered': true,
              'dailyPractice.is_correct': false,
              'dailyPractice.user_answer': selectedOption.label
            })
          }
        }
      } else {
        // 检查是否是因为已经回答过
        if (response.message && response.message.includes('已经回答')) {
          wx.showModal({
            title: '提示',
            content: '您今天已经回答过该题目了，明天再来吧！',
            showCancel: false,
            confirmText: '知道了'
          })
          // 刷新每日一练状态
          this.loadDailyPractice(this.data.currentCategory)
        } else {
          wx.showToast({
            title: response.message || '提交失败，请重试',
            icon: 'none'
          })
        }
      }
    } catch (error) {
      wx.hideLoading()
      console.error('提交答案失败:', error)
      wx.showToast({
        title: '网络错误，请重试',
        icon: 'none'
      })
    }
  },

  showAnswer() {
    // 检查是否有答案（未登录用户答案为null）
    if (!this.data.dailyPractice || !this.data.dailyPractice.answer) {
      wx.showModal({
        title: '提示',
        content: '请先登录并答题后查看答案',
        confirmText: '去登录',
        cancelText: '取消',
        success: (res) => {
          if (res.confirm) {
            wx.navigateTo({
              url: '/pages/user/user'
            })
          }
        }
      })
      return
    }
    this.setData({ showAnswerFlag: true })
  },

  hideAnswer() {
    this.setData({ showAnswerFlag: false })
  },

  // 加载今日热点
  async loadHotList() {
    try {
      const response = await app.request({
        url: '/utils/hot-list',
        method: 'GET'
      })

      if (response.success && response.data) {
        this.setData({ hotList: response.data.slice(0, 5) })
      } else {
        this.setDefaultHotList()
      }
    } catch (error) {
      console.error('加载热点失败:', error)
      this.setDefaultHotList()
    }
  },

  setDefaultHotList() {
    this.setData({ hotList: [] })
  },

  // 加载学习排行榜
  async loadRankList() {
    try {
      const response = await app.request({
        url: '/utils/rank-list?limit=5',
        method: 'GET'
      })

      if (response.success && response.data) {
        this.setData({ rankList: response.data })
      } else {
        this.setData({ rankList: [] })
      }
    } catch (error) {
      console.error('加载排行榜失败:', error)
      this.setData({ rankList: [] })
    }
  },

  setDefaultRankList() {
    this.setData({ rankList: [] })
  },

  // 导航方法
  navigateToExamSchedule() {
    wx.showToast({ title: '功能开发中', icon: 'none' })
  },

  navigateToDailyPractice() {
    wx.showToast({ title: '功能开发中', icon: 'none' })
  },

  navigateToInfoList() {
    wx.switchTab({ url: '/pages/info/info' })
  },

  navigateToInfoDetail(e) {
    const id = e.currentTarget.dataset.id
    
    // 增加热点浏览量
    this.incrementHotTopicView(id)
    
    wx.navigateTo({ url: `/pages/info-detail/info-detail?id=${id}` })
  },

  async incrementHotTopicView(topicId) {
    try {
      await app.request({
        url: `/utils/hot-topic/${topicId}/view`,
        method: 'POST'
      })
    } catch (error) {
      console.error('增加浏览量失败:', error)
    }
  },

  navigateToRankList() {
    this.loadFullRankList()
  },

  async loadFullRankList() {
    try {
      wx.showLoading({ title: '加载中...' })
      const response = await app.request({
        url: '/utils/rank-list?limit=20',
        method: 'GET'
      })
      wx.hideLoading()

      if (response.success && response.data) {
        this.setData({
          fullRankList: response.data,
          showRankModal: true
        })
      } else {
        wx.showToast({ title: '暂无排行数据', icon: 'none' })
      }
    } catch (error) {
      wx.hideLoading()
      console.error('加载完整榜单失败:', error)
      wx.showToast({ title: '加载失败', icon: 'none' })
    }
  },

  hideRankModal() {
    this.setData({ showRankModal: false })
  }
})
