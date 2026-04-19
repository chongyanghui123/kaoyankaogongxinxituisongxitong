// app.js
App({
  onLaunch() {
    // 初始化时执行
    console.log('小程序启动');
    
    // 检查登录状态
    this.checkLoginStatus();
    
    // 跳转到我的页面
    console.log('跳转到我的页面');
    wx.switchTab({
      url: '/pages/user/user',
      success: function(res) {
        console.log('跳转到我的页面成功');
      },
      fail: function(res) {
        console.error('跳转到我的页面失败:', res);
      }
    });
  },
  
  onShow() {
    // 小程序显示时执行
    console.log('小程序显示');
  },
  
  onHide() {
    // 小程序隐藏时执行
    console.log('小程序隐藏');
  },
  
  globalData: {
    userInfo: null,
    token: null,
    baseUrl: 'http://localhost:8002/api/v1' // 后端API基础地址
  },
  
  // 检查登录状态
  checkLoginStatus() {
    const token = wx.getStorageSync('token');
    const userInfo = wx.getStorageSync('userInfo');
    
    console.log('检查登录状态，token:', token);
    console.log('检查登录状态，userInfo:', userInfo);
    
    if (token && userInfo) {
      this.globalData.token = token;
      this.globalData.userInfo = userInfo;
      console.log('登录状态检查完成，已设置token和用户信息');
    } else {
      console.log('登录状态检查完成，未找到token或用户信息');
    }
  },
  
  // 登录方法
  async login(phone, password) {
    try {
      console.log('开始登录，手机号:', phone, '密码:', password);
      // 发送手机号和密码到后端获取token
      const response = await this.request({
        url: '/auth/login',
        method: 'POST',
        data: {
          username: phone,
          password: password
        }
      });
      
      console.log('登录响应:', response);
      
      if (response.success) {
        console.log('登录成功，用户信息:', response.data);
        this.globalData.token = response.data.access_token;
        this.globalData.userInfo = {
          id: response.data.user_id,
          username: response.data.username,
          email: response.data.email,
          phone: response.data.phone,
          is_vip: response.data.is_vip,
          is_admin: response.data.is_admin,
          vip_type: response.data.vip_type,
          vip_end_time: response.data.vip_end_time
        };
        
        // 存储到本地
        wx.setStorageSync('token', response.data.access_token);
        wx.setStorageSync('userInfo', this.globalData.userInfo);
        
        console.log('登录成功，已设置token和用户信息');
        console.log('当前token:', this.globalData.token);
        console.log('当前用户信息:', this.globalData.userInfo);
        
        // 检查是否需要修改密码
        if (response.data.need_change_password) {
          wx.showToast({
            title: '首次登录，请修改密码',
            icon: 'none'
          });
          
          // 跳转到修改密码页面
          wx.navigateTo({
            url: '/pages/change-password/change-password'
          });
        }
        
        return true;
      } else {
        console.log('登录失败，原因:', response.message);
        throw new Error(response.message || '登录失败');
      }
    } catch (error) {
      console.error('登录失败:', error);
      throw error;
    }
  },
  
  // 通用网络请求方法
  request(options) {
    return new Promise((resolve, reject) => {
      const token = this.globalData.token;
      const url = this.globalData.baseUrl + options.url;
      console.log('开始发送网络请求:', url);
      console.log('请求数据:', options.data);
      console.log('Token:', token);
      
      const header = {
        'Content-Type': 'application/json'
      };
      
      if (token) {
        header['Authorization'] = `Bearer ${token}`;
      }
      
      console.log('请求头:', header);
      
      wx.request({
        url: url,
        method: options.method || 'GET',
        data: options.data,
        header: header,
        timeout: 30000, // 添加超时设置，30秒
        success:(res) => {
          console.log('网络请求成功，状态码:', res.statusCode);
          console.log('响应数据:', res.data);
          if (res.statusCode === 200) {
            resolve(res.data);
          } else if (res.statusCode === 401) {
            // 未登录或token过期
            wx.removeStorageSync('token');
            wx.removeStorageSync('userInfo');
            this.globalData.token = null;
            this.globalData.userInfo = null;
            
            wx.showToast({
              title: '登录已过期，请重新登录',
              icon: 'none'
            });
            
            // 跳转到登录页面
            wx.navigateTo({
              url: '/pages/user/user'
            });
            
            reject({ success: false, message: '登录已过期' });
          } else {
            console.log('网络请求失败，状态码:', res.statusCode);
            reject({ success: false, message: '网络请求失败' });
          }
        },
        fail(err) {
          console.error('网络请求失败:', err);
          console.error('错误详情:', JSON.stringify(err));
          reject({ success: false, message: '网络请求失败' });
        },
        complete(res) {
          console.log('网络请求完成:', res);
        }
      });
    });
  },
  
  // 退出登录
  logout() {
    wx.removeStorageSync('token');
    wx.removeStorageSync('userInfo');
    this.globalData.token = null;
    this.globalData.userInfo = null;
    
    wx.showToast({
      title: '退出登录成功',
      icon: 'success'
    });
  }
});