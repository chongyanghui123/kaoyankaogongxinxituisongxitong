// subscription.js
Page({
  data: {
    userInfo: null,
    subscriptionType: '未订阅',
    remainingDays: 0,
    plans: [
      {
        id: 1,
        name: '考研套餐',
        price: 99,
        period: '月',
        features: [
          '考研情报推送',
          '院校动态提醒',
          '考试时间通知',
          '个性化推荐'
        ]
      },
      {
        id: 2,
        name: '考公套餐',
        price: 99,
        period: '月',
        features: [
          '考公情报推送',
          '政策变化提醒',
          '报名时间通知',
          '个性化推荐'
        ]
      },
      {
        id: 3,
        name: '双赛道套餐',
        price: 169,
        period: '月',
        features: [
          '考研+考公情报推送',
          '院校动态提醒',
          '政策变化提醒',
          '考试时间通知',
          '报名时间通知',
          '个性化推荐'
        ]
      }
    ],
    selectedPlan: 1,
    showPayModal: false,
    selectedPayMethod: 'wechat'
  },
  
  onLoad() {
    // 页面加载时执行

    this.getUserInfo();
  },
  
  onShow() {
    // 页面显示时执行

    this.getUserInfo();
  },
  
  // 获取用户信息
  getUserInfo() {
    const app = getApp();
    const userInfo = app.globalData.userInfo;
    
    if (userInfo) {
      this.setData({
        userInfo: userInfo
      });
      
      // 计算订阅类型和剩余天数
      this.calculateSubscriptionInfo();
    } else {
      // 用户未登录，跳转到登录页面
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      
      wx.navigateTo({
        url: '/pages/user/user'
      });
    }
  },
  
  // 计算订阅信息
  calculateSubscriptionInfo() {
    const userInfo = this.data.userInfo;
    if (!userInfo) return;
    

    
    // 获取订阅类型
    let subscriptionType = '未订阅';
    if (userInfo.vip_type === 1) {
      subscriptionType = '考研套餐';
    } else if (userInfo.vip_type === 2) {
      subscriptionType = '考公套餐';
    } else if (userInfo.vip_type === 3) {
      subscriptionType = '双赛道套餐';
    }
    
    // 计算剩余天数
    let remainingDays = 0;

    if (userInfo.is_vip && userInfo.vip_end_time) {
      const endTime = new Date(userInfo.vip_end_time);
      const now = new Date();
      const diffTime = endTime - now;
      remainingDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }
    
    this.setData({
      subscriptionType: subscriptionType,
      remainingDays: remainingDays
    });
  },
  
  // 选择套餐
  selectPlan(e) {
    const planId = e.currentTarget.dataset.id;
    this.setData({
      selectedPlan: planId
    });
  },
  
  // 支付
  pay() {
    this.setData({
      showPayModal: true
    });
  },
  
  // 关闭支付弹窗
  closePayModal() {
    this.setData({
      showPayModal: false
    });
  },
  
  // 选择支付方式
  selectPayMethod(e) {
    const method = e.currentTarget.dataset.method;
    this.setData({
      selectedPayMethod: method
    });
  },
  
  // 确认支付
  async confirmPay() {
    try {
      const app = getApp();
      const selectedPlan = this.data.plans.find(plan => plan.id === this.data.selectedPlan);
      
      // 调用支付API
      const response = await app.request({
        url: '/payment/create',
        method: 'POST',
        data: {
          plan_id: this.data.selectedPlan,
          amount: selectedPlan.price,
          pay_method: this.data.selectedPayMethod
        }
      });
      
      if (response.success) {
        // 发起支付
        wx.requestPayment({
          timeStamp: response.data.timeStamp,
          nonceStr: response.data.nonceStr,
          package: response.data.package,
          signType: response.data.signType,
          paySign: response.data.paySign,
          success: (res) => {
            wx.showToast({
              title: '支付成功',
              icon: 'success'
            });
            this.closePayModal();
            // 刷新用户信息
            this.getUserInfo();
          },
          fail: (res) => {
            wx.showToast({
              title: '支付失败',
              icon: 'none'
            });
          }
        });
      } else {
        wx.showToast({
          title: '创建订单失败',
          icon: 'none'
        });
      }
    } catch (error) {
      console.error('支付失败:', error);
      wx.showToast({
        title: '支付失败，请重试',
        icon: 'none'
      });
    }
  }
});