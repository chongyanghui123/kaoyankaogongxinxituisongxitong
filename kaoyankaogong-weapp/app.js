// app.js
App({
  onShow() {
    // 小程序显示时执行
    this.applyTheme(this.globalData.theme);
  },

  onLaunch() {
    console.log('[APP] baseUrl:', this.globalData.baseUrl);
    this.checkLoginStatus();

    // 加载主题设置
    this.loadTheme();

    // 监听页面路由变化，确保每个页面都应用主题
    wx.onAppRoute(() => {
      this.applyTheme(this.globalData.theme);
    });


  },

  onHide() {
    // 小程序隐藏时执行
  },

  globalData: {
    userInfo: null,
    token: '',
    baseUrl: 'http://localhost:8000/api/v1',
    theme: 'default' // 默认主题
  },

  // 检查登录状态
  checkLoginStatus() {
    const token = wx.getStorageSync('token');
    const refreshToken = wx.getStorageSync('refresh_token');
    const userInfo = wx.getStorageSync('userInfo');

    if (token && userInfo) {
      this.globalData.token = token;
      this.globalData.userInfo = userInfo;
    } else if (refreshToken && userInfo) {
      // 如果有refreshToken但没有accessToken，尝试刷新token
      this.refreshToken(refreshToken).then(res => {
        if (res.success) {
          this.globalData.token = res.data.access_token;
          this.globalData.userInfo = userInfo;
          wx.setStorageSync('token', res.data.access_token);
        } else {
          // 刷新失败，清除存储
          this.handleLoginExpired();
        }
      }).catch(() => {
        // 刷新失败，清除存储
        this.handleLoginExpired();
      });
    } else {
    }
  },

  // 登录方法
  async login(phone, password) {
    try {
      const url = this.globalData.baseUrl + '/auth/login';
      const response = await new Promise((resolve, reject) => {
        wx.request({
          url: url,
          method: 'POST',
          data: {
            username: phone,
            password: password
          },
          header: {
            'Content-Type': 'application/json'
          },
          timeout: 30000,
          success: (res) => resolve(res),
          fail: (err) => reject(err)
        });
      });

      if (response.statusCode === 200 && response.data.success) {
        const data = response.data.data;
        this.globalData.token = data.access_token;
        this.globalData.userInfo = {
          id: data.user_id,
          username: data.username,
          email: data.email,
          phone: data.phone,
          is_vip: data.is_vip,
          is_admin: data.is_admin,
          vip_type: data.vip_type,
          vip_end_time: data.vip_end_time,
          need_change_password: data.need_change_password
        };

        wx.setStorageSync('token', data.access_token);
        wx.setStorageSync('refresh_token', data.refresh_token);
        wx.setStorageSync('userInfo', this.globalData.userInfo);

        if (data.need_change_password) {
          wx.showToast({
            title: '首次登录，请修改密码',
            icon: 'none'
          });
          wx.navigateTo({
            url: '/pages/change-password/change-password'
          });
        }

        return true;
      } else if (response.statusCode === 401) {
        const message = response.data?.message || '用户名或密码错误';
        throw new Error(message);
      } else if (response.statusCode === 400) {
        const message = response.data?.message || '请求参数错误';
        throw new Error(message);
      } else {
        throw new Error(response.data?.message || '登录失败');
      }
    } catch (error) {
      console.error('登录失败:', error);
      throw error;
    }
  },

  // 通用网络请求方法
  async request(options) {
    try {
      const token = this.globalData.token;
      const url = this.globalData.baseUrl + options.url;

      const header = {
        'Content-Type': 'application/json'
      };

      if (token) {
        header['Authorization'] = `Bearer ${token}`;
      }

      const response = await new Promise((resolve, reject) => {
        wx.request({
          url: url,
          method: options.method || 'GET',
          data: options.data,
          header: header,
          timeout: 30000, // 添加超时设置，30秒
          success: (res) => {
            resolve(res);
          },
          fail: (err) => {
            reject(err);
          }
        });
      });

      if (response.statusCode === 200) {
        return response.data;
      } else if (response.statusCode === 401) {
        // Token过期，尝试刷新token
        const refreshToken = wx.getStorageSync('refresh_token');
        if (refreshToken) {
          try {
            const refreshResponse = await this.refreshToken(refreshToken);
            if (refreshResponse.success) {
              // 刷新成功，重新请求
              this.globalData.token = refreshResponse.data.access_token;
              wx.setStorageSync('token', refreshResponse.data.access_token);
              
              // 重新请求原接口
              const newHeader = {
                ...header,
                'Authorization': `Bearer ${this.globalData.token}`
              };
              const retryResponse = await new Promise((resolve, reject) => {
                wx.request({
                  url: url,
                  method: options.method || 'GET',
                  data: options.data,
                  header: newHeader,
                  timeout: 30000,
                  success: (res) => {
                    resolve(res);
                  },
                  fail: (err) => {
                    reject(err);
                  }
                });
              });
              
              if (retryResponse.statusCode === 200) {
                return retryResponse.data;
              } else {
                throw new Error('刷新token后请求仍失败');
              }
            } else {
              throw new Error('刷新token失败');
            }
          } catch (error) {
            // 刷新token失败，跳转到登录页面
            this.handleLoginExpired();
            throw error;
          }
        } else {
          // 没有refreshToken，跳转到登录页面
          this.handleLoginExpired();
          throw new Error('登录已失效');
        }
      } else if (response.statusCode === 403) {
        // 权限不足
        this.handleLoginExpired();
        throw new Error('登录已失效');
      } else if (response.statusCode === 404) {
        // 资源不存在
        throw new Error('请求的资源不存在');
      } else if (response.statusCode === 400) {
        // 400错误，通常是业务逻辑错误
        const errorMessage = response.data?.message || '请求参数错误';
        throw new Error(errorMessage);
      } else {
        throw new Error('网络请求失败');
      }
    } catch (error) {
      console.error('网络请求失败:', error);
      throw error;
    }
  },

  // 刷新token
  refreshToken(refreshToken) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: this.globalData.baseUrl + '/refresh',
        method: 'POST',
        data: {
          refresh_token: refreshToken
        },
        header: {
          'Content-Type': 'application/json'
        },
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(res);
          }
        },
        fail: (err) => {
          reject(err);
        }
      });
    });
  },

  // 处理登录过期
  handleLoginExpired() {
    wx.removeStorageSync('token');
    wx.removeStorageSync('refresh_token');
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
  },

  // 退出登录
  logout() {
    wx.removeStorageSync('token');
    wx.removeStorageSync('refresh_token');
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