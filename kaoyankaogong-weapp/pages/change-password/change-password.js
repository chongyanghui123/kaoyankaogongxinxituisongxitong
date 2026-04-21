// change-password.js
Page({
  data: {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  },
  
  onLoad() {
    // 页面加载时执行

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
    const { oldPassword, newPassword, confirmPassword } = this.data;
    
    // 验证输入
    if (!oldPassword || !newPassword || !confirmPassword) {
      wx.showToast({
        title: '请输入所有密码',
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
    app.request({
      url: '/auth/change-password',
      method: 'POST',
      data: {
        old_password: oldPassword,
        new_password: newPassword
      }
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