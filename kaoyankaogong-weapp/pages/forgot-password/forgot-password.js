// forgot-password.js
const app = getApp()

Page({
  data: {
    phone: '',
    code: '',
    newPassword: '',
    confirmPassword: '',
    showNewPassword: false,
    showConfirmPassword: false,
    codeBtnText: '发送验证码',
    canSendCode: true,
    canSubmit: false
  },

  onLoad() {
    // 页面加载
  },

  // 返回上一页
  navigateBack() {
    wx.navigateBack()
  },

  // 手机号输入
  bindPhoneInput(e) {
    this.setData({
      phone: e.detail.value
    })
    this.checkFormValidity()
  },

  // 验证码输入
  bindCodeInput(e) {
    this.setData({
      code: e.detail.value
    })
    this.checkFormValidity()
  },

  // 新密码输入
  bindNewPasswordInput(e) {
    this.setData({
      newPassword: e.detail.value
    })
    this.checkFormValidity()
  },

  // 确认新密码输入
  bindConfirmPasswordInput(e) {
    this.setData({
      confirmPassword: e.detail.value
    })
    this.checkFormValidity()
  },

  // 显示/隐藏新密码
  toggleShowNewPassword() {
    this.setData({
      showNewPassword: !this.data.showNewPassword
    })
  },

  // 显示/隐藏确认密码
  toggleShowConfirmPassword() {
    this.setData({
      showConfirmPassword: !this.data.showConfirmPassword
    })
  },

  // 检查表单是否有效
  checkFormValidity() {
    const { phone, code, newPassword, confirmPassword } = this.data
    const isValid = phone.length === 11 && code.length === 6 && newPassword.length >= 6 && confirmPassword.length >= 6 && newPassword === confirmPassword
    this.setData({
      canSubmit: isValid
    })
  },

  // 发送验证码
  sendCode() {
    const { phone } = this.data
    
    // 验证手机号格式
    if (!/^1[3-9]\d{9}$/.test(phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      })
      return
    }

    // 发送验证码请求
    wx.showLoading({ title: '发送中...' })
    wx.request({
      url: app.globalData.baseUrl + '/auth/send-sms-code',
      method: 'POST',
      data: {
        phone: phone,
        type: 'reset_password'
      },
      success: (res) => {
        wx.hideLoading()
        
        if (res.data.success) {
          wx.showToast({
            title: '验证码已发送',
            icon: 'success'
          })
          
          // 倒计时
          this.startCountdown()
        } else {
          wx.showToast({
            title: res.data.message || '发送失败',
            icon: 'none'
          })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        console.error('发送验证码失败:', err)
        wx.showToast({
          title: '网络请求失败',
          icon: 'none'
        })
      }
    })
  },

  // 倒计时
  startCountdown() {
    let countdown = 60
    this.setData({
      canSendCode: false,
      codeBtnText: `${countdown}s`
    })

    const timer = setInterval(() => {
      countdown--
      
      if (countdown <= 0) {
        clearInterval(timer)
        this.setData({
          canSendCode: true,
          codeBtnText: '发送验证码'
        })
      } else {
        this.setData({
          codeBtnText: `${countdown}s`
        })
      }
    }, 1000)
  },

  // 确认重置密码
  confirmResetPassword() {
    const { phone, code, newPassword } = this.data
    
    // 验证密码强度
    if (newPassword.length < 6) {
      wx.showToast({
        title: '密码长度至少6位',
        icon: 'none'
      })
      return
    }

    wx.showLoading({ title: '重置中...' })
    wx.request({
      url: app.globalData.baseUrl + '/auth/reset-password',
      method: 'POST',
      data: {
        phone: phone,
        code: code,
        new_password: newPassword
      },
      success: (res) => {
        wx.hideLoading()
        
        if (res.data.success) {
          wx.showToast({
            title: '密码重置成功',
            icon: 'success'
          })
          
          // 重置成功后跳转登录页
          setTimeout(() => {
            wx.navigateBack({
              delta: 2
            })
          }, 1500)
        } else {
          wx.showToast({
            title: res.data.message || '重置失败',
            icon: 'none'
          })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        console.error('重置密码失败:', err)
        wx.showToast({
          title: '网络请求失败',
          icon: 'none'
        })
      }
    })
  }
})
