// change-password.js
Page({
  data: {
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
    isFirstLogin: false,
    showOldPassword: false,
    showNewPassword: false,
    showConfirmPassword: false
  },
  
  onLoad() {
    // 页面加载时执行
    const app = getApp();
    // 检查用户是否是第一次登录
    this.setData({
      isFirstLogin: app.globalData.userInfo && app.globalData.userInfo.need_change_password
    });
  },
  
  // 显示/隐藏旧密码
  toggleShowOldPassword() {
    this.setData({
      showOldPassword: !this.data.showOldPassword
    });
  },
  
  // 显示/隐藏新密码
  toggleShowNewPassword() {
    this.setData({
      showNewPassword: !this.data.showNewPassword
    });
  },
  
  // 显示/隐藏确认密码
  toggleShowConfirmPassword() {
    this.setData({
      showConfirmPassword: !this.data.showConfirmPassword
    });
  },
  
  // 旧密码输入
  bindOldPasswordInput(e) {
    this.setData({
      oldPassword: e.detail.value
    });
  },
  
  // 新密码输入
  bindNewPasswordInput(e) {
    this.setData({
      newPassword: e.detail.value
    });
  },
  
  // 确认新密码输入
  bindConfirmPasswordInput(e) {
    this.setData({
      confirmPassword: e.detail.value
    });
  },
  
  // 修改密码
  changePassword() {
    const { oldPassword, newPassword, confirmPassword, isFirstLogin } = this.data;
    
    // 验证输入
    if (!isFirstLogin && !oldPassword) {
      wx.showToast({
        title: '请输入旧密码',
        icon: 'none'
      });
      return;
    }
    
    if (!newPassword || !confirmPassword) {
      wx.showToast({
        title: '请输入新密码和确认密码',
        icon: 'none'
      });
      return;
    }
    
    if (newPassword !== confirmPassword) {
      wx.showToast({
        title: '两次输入的新密码不一致',
        icon: 'none'
      });
      return;
    }
    
    if (newPassword.length < 6) {
      wx.showToast({
        title: '新密码长度至少6位',
        icon: 'none'
      });
      return;
    }
    
    // 调用修改密码API
    const app = getApp();
    const data = isFirstLogin ? {
      new_password: newPassword
    } : {
      old_password: oldPassword,
      new_password: newPassword
    };
    
    app.request({
      url: '/auth/change-password',
      method: 'POST',
      data: data
    }).then(response => {

      
      if (response.success) {
        // 修改成功，更新用户信息
        const userInfo = app.globalData.userInfo;
        userInfo.need_change_password = false;
        app.globalData.userInfo = userInfo;
        wx.setStorageSync('userInfo', userInfo);
        
        wx.showToast({
          title: '密码修改成功',
          icon: 'success'
        });
        
        // 跳转到个人中心页面
        setTimeout(() => {
          wx.navigateBack({
            delta: 1
          });
        }, 1500);
      } else {
        wx.showToast({
          title: response.message || '密码修改失败',
          icon: 'none'
        });
      }
    }).catch(error => {
      console.error('修改密码失败:', error);
      wx.showToast({
        title: '网络请求失败，请重试',
        icon: 'none'
      });
    });
  }
});