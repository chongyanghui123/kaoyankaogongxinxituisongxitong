// app.js
App({
  onShow() {
    // 小程序显示时执行
    this.applyTheme(this.globalData.theme);
  },
  
  onLaunch() {
    // 初始化时执行
    
    // 检查登录状态
    this.checkLoginStatus();
    
    // 加载主题设置
    this.loadTheme();
    
    // 监听页面路由变化，确保每个页面都应用主题
    wx.onAppRoute(() => {
      this.applyTheme(this.globalData.theme);
    });
    
    // 跳转到我的页面
    wx.switchTab({
      url: '/pages/user/user',
      success: function(res) {
      },
      fail: function(res) {
        console.error('跳转到我的页面失败:', res);
      }
    });
  },
  
  onHide() {
    // 小程序隐藏时执行
  },
  
  globalData: {
    userInfo: null,
    token: '',
    baseUrl: 'http://192.168.1.154:8000/api/v1', // 后端API基础地址
    theme: 'default' // 默认主题
  },
  
  // 检查登录状态
  checkLoginStatus() {
    const token = wx.getStorageSync('token');
    const userInfo = wx.getStorageSync('userInfo');
    
    if (token && userInfo) {
      this.globalData.token = token;
      this.globalData.userInfo = userInfo;
    } else {
    }
  },
  
  // 登录方法
  async login(phone, password) {
    try {
      // 发送手机号和密码到后端获取token
      const response = await this.request({
        url: '/auth/login',
        method: 'POST',
        data: {
          username: phone,
          password: password
        }
      });
      
      if (response.success) {
        this.globalData.token = response.data.access_token;
        this.globalData.userInfo = {
          id: response.data.user_id,
          username: response.data.username,
          email: response.data.email,
          phone: response.data.phone,
          is_vip: response.data.is_vip,
          is_admin: response.data.is_admin,
          vip_type: response.data.vip_type,
          vip_end_time: response.data.vip_end_time,
          need_change_password: response.data.need_change_password
        };
        
        // 存储到本地
        wx.setStorageSync('token', response.data.access_token);
        wx.setStorageSync('userInfo', this.globalData.userInfo);
        
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
      
      const header = {
        'Content-Type': 'application/json'
      };
      
      if (token) {
        header['Authorization'] = `Bearer ${token}`;
      }
      
      wx.request({
        url: url,
        method: options.method || 'GET',
        data: options.data,
        header: header,
        timeout: 30000, // 添加超时设置，30秒
        success:(res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else if (res.statusCode === 401 || res.statusCode === 403 || res.statusCode === 404) {
            // 未登录、token无效或用户不存在
            wx.removeStorageSync('token');
            wx.removeStorageSync('userInfo');
            this.globalData.token = null;
            this.globalData.userInfo = null;
            
            wx.showToast({
              title: '登录已失效，请重新登录',
              icon: 'none'
            });
            
            // 跳转到登录页面
            wx.navigateTo({
              url: '/pages/user/user'
            });
            
            reject({ success: false, message: '登录已失效' });
          } else {
            reject({ success: false, message: '网络请求失败' });
          }
        },
        fail(err) {
          console.error('网络请求失败:', err);
          console.error('错误详情:', JSON.stringify(err));
          reject({ success: false, message: '网络请求失败' });
        },
        complete(res) {
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
  },
  
  // 加载主题设置
  loadTheme() {
    const savedTheme = wx.getStorageSync('systemTheme');
    if (savedTheme) {
      this.globalData.theme = savedTheme;
      this.applyTheme(savedTheme);
    } else {
      // 默认使用浅色主题
      this.applyTheme('default');
    }
  },
  
  // 切换主题
  changeTheme(theme) {
    this.globalData.theme = theme;
    wx.setStorageSync('systemTheme', theme);
    this.applyTheme(theme);
  },
  
  // 应用主题
  applyTheme(theme) {
    // 根据不同主题设置不同的导航栏和背景颜色
    switch (theme) {
      case 'dark':
        // 深色主题
        wx.setNavigationBarColor({
          frontColor: '#ffffff',
          backgroundColor: '#1a1a1a'
        });
        wx.setBackgroundColor({
          backgroundColor: '#1a1a1a'
        });
        break;
      case 'eye':
        // 护眼模式
        wx.setNavigationBarColor({
          frontColor: '#000000',
          backgroundColor: '#f7f3e9'
        });
        wx.setBackgroundColor({
          backgroundColor: '#f7f3e9'
        });
        break;
      default:
        // 默认主题
        wx.setNavigationBarColor({
          frontColor: '#000000',
          backgroundColor: '#f5f7fa'
        });
        wx.setBackgroundColor({
          backgroundColor: '#f5f7fa'
        });
        break;
    }
    
    // 更新所有页面的主题数据
    const pages = getCurrentPages();
    pages.forEach(page => {
      page.setData({ theme });
    });
  }
});