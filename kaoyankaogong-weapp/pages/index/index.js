// index.js
Page({
  data: {
    latestInfo: [],
    historyInfo: [],
    searchText: '',
    userInfo: null,
    showKaoyan: true,
    showKaogong: true
  },
  
  onLoad() {
    // 页面加载时执行
    console.log('首页加载');
    this.getUserInfo();
    this.fetchData();
  },
  
  // 获取用户信息
  async getUserInfo() {
    try {
      const app = getApp();
      // 从全局数据中获取用户信息
      let userInfo = app.globalData.userInfo;
      
      // 如果全局数据中没有用户信息，从本地存储中读取
      if (!userInfo) {
        userInfo = wx.getStorageSync('userInfo');
        // 如果本地存储中有用户信息，更新全局数据
        if (userInfo) {
          app.globalData.userInfo = userInfo;
        }
      }
      
      if (userInfo) {
        this.setData({
          userInfo: userInfo
        });
        
        // 根据用户的VIP类型设置显示的情报入口
        this.updateCategoryVisibility(userInfo);
      }
    } catch (error) {
      console.error('获取用户信息失败:', error);
    }
  },
  
  // 根据用户类型更新分类可见性
  updateCategoryVisibility(userInfo) {
    const vipType = userInfo.vip_type;
    let showKaoyan = true;
    let showKaogong = true;
    
    // 1-考研VIP, 2-考公VIP, 3-双赛道VIP
    if (vipType === 1) {
      // 考研VIP，只显示考研情报
      showKaoyan = true;
      showKaogong = false;
    } else if (vipType === 2) {
      // 考公VIP，只显示考公情报
      showKaoyan = false;
      showKaogong = true;
    } else if (vipType === 3) {
      // 双赛道VIP，显示两者
      showKaoyan = true;
      showKaogong = true;
    }
    
    this.setData({
      showKaoyan: showKaoyan,
      showKaogong: showKaogong
    });
  },
  
  onShow() {
    // 页面显示时执行
    console.log('首页显示');
    // 重新获取用户信息，确保登录状态更新
    this.getUserInfo();
    
    // 检查用户是否登录，如果未登录，清空情报内容
    const app = getApp();
    if (!app.globalData.userInfo) {
      this.setData({
        latestInfo: [],
        historyInfo: []
      });
    }
  },
  
  // 获取数据
  async fetchData() {
    try {
      const app = getApp();
      
      // 检查用户是否登录
      if (!app.globalData.userInfo) {
        // 用户未登录，不获取数据
        console.log('用户未登录，跳过数据获取');
        return;
      }
      
      // 调用API获取最新情报
      const latestResponse = await app.request({
        url: '/info/latest'
      });
      
      if (latestResponse.success) {
        this.setData({
          latestInfo: latestResponse.data
        });
      }
      
      // 调用API获取历史情报
      const historyResponse = await app.request({
        url: '/info/hot'
      });
      
      if (historyResponse.success) {
        this.setData({
          historyInfo: historyResponse.data
        });
      }
    } catch (error) {
      console.error('获取数据失败:', error);
    }
  },
  
  // 搜索输入
  onSearchInput(e) {
    this.setData({
      searchText: e.detail.value
    });
  },
  
  // 搜索确认
  onSearchConfirm() {
    if (this.data.searchText) {
      wx.navigateTo({
        url: `/pages/info/info?search=${encodeURIComponent(this.data.searchText)}`
      });
    }
  },
  
  // 导航到情报列表
  navigateToInfo(e) {
    const type = e.currentTarget.dataset.type;
    wx.navigateTo({
      url: `/pages/info/info?type=${type}`
    });
  },
  
  // 导航到情报详情
  navigateToDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },
  
  // 导航到订阅管理
  navigateToSubscription() {
    wx.navigateTo({
      url: '/pages/subscription/subscription'
    });
  },
  
  // 导航到消息中心
  navigateToMessage() {
    wx.navigateTo({
      url: '/pages/message/message'
    });
  },
  
  // 导航到登录页面
  navigateToLogin() {
    wx.navigateTo({
      url: '/pages/user/user'
    });
  }
});