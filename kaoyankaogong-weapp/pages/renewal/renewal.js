// renewal.js
const app = getApp()

Page({
  data: {
    userInfo: null,
    renewalOptions: [],
    selectedPlan: null,
    showPayModal: false,
    selectedPayMethod: 'wechat',
    loading: true
  },

  async onLoad() {
    await this.getUserInfo()
    this.loadRenewalOptions()
  },

  // 获取用户信息
  async getUserInfo() {
    try {
      await app.fetchUserInfo()
      this.setData({
        userInfo: app.globalData.userInfo
      })
    } catch (error) {
      console.error('获取用户信息失败:', error)
      wx.showToast({ title: '获取用户信息失败', icon: 'none' })
    }
  },

  // 加载续费选项
  async loadRenewalOptions() {
    try {
      wx.showLoading({ title: '加载续费选项...' })
      
      const response = await app.request({
        url: '/payments/renewal-options',
        method: 'GET'
      })

      wx.hideLoading()

      if (response.success && response.data) {
        const renewalOptions = response.data.map(p => ({
          id: p.id,
          name: p.name,
          price: p.price,
          period: p.duration ? (p.duration >= 365 ? '年' : p.duration >= 30 ? '月' : '天') : '月',
          duration: p.duration || 30,
          type: p.type,
          description: p.description || '',
          features: this.getFeaturesByType(p.type, p.description)
        }))

        this.setData({
          renewalOptions,
          selectedPlan: renewalOptions.length > 0 ? renewalOptions[0].id : null,
          loading: false
        })
      } else {
        wx.showToast({ title: response.message || '加载续费选项失败', icon: 'none' })
        this.setData({ loading: false })
      }
    } catch (error) {
      wx.hideLoading()
      console.error('加载续费选项失败:', error)
      wx.showToast({ title: '加载续费选项失败', icon: 'none' })
      this.setData({ loading: false })
    }
  },

  // 根据产品类型获取功能特点
  getFeaturesByType(type, description) {
    if (type === 1) return ['考研情报推送', '院校动态提醒', '考试时间通知', '个性化推荐']
    if (type === 2) return ['考公情报推送', '政策变化提醒', '报名时间通知', '个性化推荐']
    if (type === 3) return ['考研+考公情报推送', '院校动态提醒', '政策变化提醒', '考试/报名时间通知', '个性化推荐']
    return ['情报推送', '个性化推荐']
  },

  // 选择续费套餐
  selectPlan(e) {
    this.setData({ selectedPlan: e.currentTarget.dataset.id })
  },

  // 打开支付模态框
  pay() {
    this.setData({ showPayModal: true })
  },

  // 关闭支付模态框
  closePayModal() {
    this.setData({ showPayModal: false })
  },

  // 选择支付方式
  selectPayMethod(e) {
    this.setData({ selectedPayMethod: e.currentTarget.dataset.method })
  },

  // 确认支付
  async confirmPay() {
    const app = getApp()
    const product = this.data.renewalOptions.find(p => p.id === this.data.selectedPlan)
    if (!product) return

    try {
      wx.showLoading({ title: '创建订单...' })

      const createResponse = await app.request({
        url: '/payments/renew',
        method: 'POST',
        data: {
          payment_method: this.data.selectedPayMethod === 'wechat' ? 1 : 2
        }
      })

      wx.hideLoading()

      if (!createResponse.success) {
        wx.showToast({ title: createResponse.message || '创建订单失败', icon: 'none' })
        return
      }

      const orderId = createResponse.data.id

      wx.showLoading({ title: '支付中...' })

      const payResponse = await app.request({
        url: `/payments/orders/${orderId}/pay`,
        method: 'POST',
        data: {
          pay_method: this.data.selectedPayMethod,
          mock_payment: true
        }
      })

      wx.hideLoading()

      if (payResponse.success) {
        if (payResponse.data && payResponse.data.mock) {
          // 续费成功，显示详细提醒
          const userData = this.data.userInfo
          const product = this.data.renewalOptions.find(p => p.id === this.data.selectedPlan)
          
          if (userData && product) {
            // 立即更新用户信息，获取最新的到期时间
            await this.getUserInfo()
            
            // 再次获取更新后的用户信息
            const updatedUserInfo = this.data.userInfo
            
            wx.showModal({
              title: '续费成功',
              content: `您已成功续费${product.name}！\n新的服务到期时间：${updatedUserInfo.vip_end_time}`,
              showCancel: false,
              confirmText: '确定',
              success: () => {
                this.closePayModal()
                
                setTimeout(() => {
                  wx.switchTab({ url: '/pages/user/user' })
                }, 500)
              }
            })
          } else {
            wx.showToast({ title: '续费成功', icon: 'success' })
            this.closePayModal()
            this.getUserInfo()
            
            setTimeout(() => {
              wx.switchTab({ url: '/pages/user/user' })
            }, 1500)
          }
        } else if (payResponse.data && payResponse.data.timeStamp) {
          wx.requestPayment({
            timeStamp: payResponse.data.timeStamp,
            nonceStr: payResponse.data.nonceStr,
            package: payResponse.data.package,
            signType: payResponse.data.signType,
            paySign: payResponse.data.paySign,
            success: async () => {
              // 支付成功，显示详细提醒
              const userData = this.data.userInfo
              const product = this.data.renewalOptions.find(p => p.id === this.data.selectedPlan)
              
              if (userData && product) {
                // 立即更新用户信息，获取最新的到期时间
                await this.getUserInfo()
                
                // 再次获取更新后的用户信息
                const updatedUserInfo = this.data.userInfo
                
                wx.showModal({
                  title: '续费成功',
                  content: `您已成功续费${product.name}！\n新的服务到期时间：${updatedUserInfo.vip_end_time}`,
                  showCancel: false,
                  confirmText: '确定',
                  success: () => {
                    this.closePayModal()
                    
                    setTimeout(() => {
                      wx.switchTab({ url: '/pages/user/user' })
                    }, 500)
                  }
                })
              } else {
                wx.showToast({ title: '续费成功', icon: 'success' })
                this.closePayModal()
                this.getUserInfo()
                
                setTimeout(() => {
                  wx.switchTab({ url: '/pages/user/user' })
                }, 1500)
              }
            },
            fail: () => {
              wx.showToast({ title: '支付取消', icon: 'none' })
            }
          })
        }
      } else {
        wx.showToast({ title: payResponse.message || '支付失败', icon: 'none' })
      }
    } catch (error) {
      wx.hideLoading()
      console.error('支付失败:', error)
      wx.showToast({ title: '支付失败，请重试', icon: 'none' })
    }
  },

  // 计算续费后到期时间
  calculateRenewedEndTime(vipEndTime, duration) {
    if (!vipEndTime || !duration) return ''
    
    // 解析当前到期时间
    const endDate = new Date(vipEndTime)
    
    // 计算续费后到期时间
    const renewedEndDate = new Date(endDate)
    renewedEndDate.setDate(renewedEndDate.getDate() + duration)
    
    // 格式化日期为 yyyy-mm-dd
    const year = renewedEndDate.getFullYear()
    const month = String(renewedEndDate.getMonth() + 1).padStart(2, '0')
    const day = String(renewedEndDate.getDate()).padStart(2, '0')
    
    return `${year}-${month}-${day}`
  },

  // 阻止事件冒泡
  stopPropagation() {
    // 阻止事件冒泡，防止点击模态框内部时触发关闭事件
  },

  // 返回上一页
  navigateBack() {
    wx.navigateBack()
  }
})
