const app = getApp()

Page({
  data: {
    address: {
      real_name: '',
      phone: '',
      address: ''
    },
    saving: false
  },

  onLoad() {
    this.loadAddress()
  },

  async loadAddress() {
    try {
      const response = await app.request({
        url: '/users/address',
        method: 'GET'
      })
      
      if (response.success && response.data) {
        this.setData({
          address: response.data
        })
      }
    } catch (error) {
      console.error('加载地址失败:', error)
    }
  },

  onInputName(e) {
    this.setData({
      'address.real_name': e.detail.value
    })
  },

  onInputPhone(e) {
    this.setData({
      'address.phone': e.detail.value
    })
  },

  onInputAddress(e) {
    this.setData({
      'address.address': e.detail.value
    })
  },

  validatePhone(phone) {
    return /^1[3-9]\d{9}$/.test(phone)
  },

  async saveAddress() {
    const { real_name, phone, address } = this.data.address

    if (!real_name || !real_name.trim()) {
      wx.showToast({
        title: '请输入收货人姓名',
        icon: 'none'
      })
      return
    }

    if (!phone || !this.validatePhone(phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      })
      return
    }

    if (!address || !address.trim()) {
      wx.showToast({
        title: '请输入详细地址',
        icon: 'none'
      })
      return
    }

    this.setData({ saving: true })

    try {
      const response = await app.request({
        url: '/users/address',
        method: 'PUT',
        data: {
          real_name: real_name.trim(),
          phone: phone.trim(),
          address: address.trim()
        }
      })

      if (response.success) {
        wx.showToast({
          title: '保存成功',
          icon: 'success'
        })
        
        setTimeout(() => {
          wx.navigateBack()
        }, 1500)
      } else {
        wx.showToast({
          title: response.message || '保存失败',
          icon: 'none'
        })
      }
    } catch (error) {
      console.error('保存地址失败:', error)
      wx.showToast({
        title: '保存失败',
        icon: 'none'
      })
    } finally {
      this.setData({ saving: false })
    }
  }
})
