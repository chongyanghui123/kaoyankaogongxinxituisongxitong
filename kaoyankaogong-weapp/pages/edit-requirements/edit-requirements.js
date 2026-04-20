// edit-requirements.js
const app = getApp()

Page({
  data: {
    loading: false,
    userInfo: null,
    kaoyanRequirements: {
      province: '',
      school: '',
      major: '',
      type: '',
      keywords: ''
    },
    kaogongRequirements: {
      province: '',
      school: '',
      major: '',
      type: '',
      keywords: ''
    }
  },

  onLoad() {
    this.getUserInfo()
    this.getRequirements()
  },

  // 获取用户信息
  getUserInfo() {
    const userInfo = app.globalData.userInfo
    if (userInfo) {
      this.setData({
        userInfo: userInfo
      })
    } else {
      wx.navigateBack()
    }
  },

  // 获取需求信息
  getRequirements() {
    const app = getApp()
    if (!app.globalData.token) {
      wx.navigateBack()
      return
    }

    this.setData({ loading: true })
    wx.request({
      url: app.globalData.baseUrl + '/users/profile',
      method: 'GET',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token
      },
      success: (res) => {
        this.setData({ loading: false })
        if (res.data.success) {
          const userData = res.data.data
          
          // 处理考研需求信息
          if (userData.kaoyan_requirements) {
            this.setData({
              'kaoyanRequirements.province': userData.kaoyan_requirements.province || '',
              'kaoyanRequirements.school': userData.kaoyan_requirements.school || '',
              'kaoyanRequirements.major': userData.kaoyan_requirements.major || '',
              'kaoyanRequirements.type': userData.kaoyan_requirements.type || '',
              'kaoyanRequirements.keywords': userData.kaoyan_requirements.keywords || ''
            })
          }

          // 处理考公需求信息
          if (userData.kaogong_requirements) {
            this.setData({
              'kaogongRequirements.province': userData.kaogong_requirements.province || '',
              'kaogongRequirements.school': userData.kaogong_requirements.school || '',
              'kaogongRequirements.major': userData.kaogong_requirements.major || '',
              'kaogongRequirements.type': userData.kaogong_requirements.type || '',
              'kaogongRequirements.keywords': userData.kaogong_requirements.keywords || ''
            })
          }
        } else {
          wx.showToast({
            title: res.data.message || '获取需求信息失败',
            icon: 'none'
          })
        }
      },
      fail: (err) => {
        this.setData({ loading: false })
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        })
      }
    })
  },

  // 考研需求信息输入处理
  onKaoyanProvinceInput(e) {
    this.setData({ 'kaoyanRequirements.province': e.detail.value })
  },

  onKaoyanSchoolInput(e) {
    this.setData({ 'kaoyanRequirements.school': e.detail.value })
  },

  onKaoyanMajorInput(e) {
    this.setData({ 'kaoyanRequirements.major': e.detail.value })
  },

  onKaoyanTypeInput(e) {
    this.setData({ 'kaoyanRequirements.type': e.detail.value })
  },

  onKaoyanKeywordsInput(e) {
    this.setData({ 'kaoyanRequirements.keywords': e.detail.value })
  },

  // 考公需求信息输入处理
  onKaogongProvinceInput(e) {
    this.setData({ 'kaogongRequirements.province': e.detail.value })
  },

  onKaogongSchoolInput(e) {
    this.setData({ 'kaogongRequirements.school': e.detail.value })
  },

  onKaogongMajorInput(e) {
    this.setData({ 'kaogongRequirements.major': e.detail.value })
  },

  onKaogongTypeInput(e) {
    this.setData({ 'kaogongRequirements.type': e.detail.value })
  },

  onKaogongKeywordsInput(e) {
    this.setData({ 'kaogongRequirements.keywords': e.detail.value })
  },

  // 保存需求信息
  saveRequirements() {
    const app = getApp()
    if (!app.globalData.token) {
      wx.navigateBack()
      return
    }

    // 构建请求数据
    const data = {
      subscribe_type: this.data.userInfo.vip_type,
      config: {
        kaoyan: this.formatRequirements(this.data.kaoyanRequirements, true), // 考研需求信息包含关注学校
        kaogong: this.formatRequirements(this.data.kaogongRequirements, false) // 考公需求信息不包含关注学校
      }
    }

    this.setData({ loading: true })
    wx.request({
      url: app.globalData.baseUrl + '/users/subscription',
      method: 'PUT',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token,
        'Content-Type': 'application/json'
      },
      data: data,
      success: (res) => {
        this.setData({ loading: false })
        if (res.data.success) {
          wx.showToast({
            title: '保存成功',
            icon: 'success'
          })
          // 刷新用户信息
          this.getUserInfo()
          // 跳转回个人中心页面
          setTimeout(() => {
            wx.navigateBack()
          }, 1500)
        } else {
          wx.showToast({
            title: res.data.message || '保存失败',
            icon: 'none'
          })
        }
      },
      fail: (err) => {
        this.setData({ loading: false })
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        })
      }
    })
  },

  // 格式化需求信息
  formatRequirements(requirements, isKaoyan) {
    const formatted = {
      provinces: requirements.province ? [requirements.province] : [],
      majors: requirements.major,
      types: requirements.type ? [requirements.type] : [],
      keywords: requirements.keywords
    }
    
    // 考研需求信息包含关注学校，考公需求信息不包含
    if (isKaoyan) {
      formatted.schools = requirements.school
    }
    
    return formatted
  },

  // 返回上一页
  navigateBack() {
    wx.navigateBack()
  }
})
