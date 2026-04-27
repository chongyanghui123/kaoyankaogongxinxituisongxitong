Page({
  data: {
    name: '',
    description: '',
    tags: '',
    joinType: 1
  },

  onNameInput(e) {
    this.setData({ name: e.detail.value });
  },

  onDescriptionInput(e) {
    this.setData({ description: e.detail.value });
  },

  onTagsInput(e) {
    this.setData({ tags: e.detail.value });
  },

  onJoinTypeChange(e) {
    this.setData({ joinType: parseInt(e.detail.value) });
  },

  submitGroup() {
    if (!this.data.name.trim()) {
      wx.showToast({
        title: '请输入小组名称',
        icon: 'none'
      });
      return;
    }

    if (!this.data.description.trim()) {
      wx.showToast({
        title: '请输入小组简介',
        icon: 'none'
      });
      return;
    }

    const app = getApp();
    wx.request({
      url: `${app.globalData.baseUrl}/community/groups`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      },
      data: {
        name: this.data.name,
        description: this.data.description,
        tags: this.data.tags,
        join_type: this.data.joinType
      },
      success: (res) => {
        if (res.statusCode === 200) {
          wx.showToast({
            title: '创建成功',
            icon: 'success'
          });
          setTimeout(() => {
            wx.navigateBack();
          }, 1500);
        } else {
          wx.showToast({
            title: res.data.detail || '创建失败',
            icon: 'none'
          });
        }
      },
      fail: () => {
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        });
      }
    });
  }
});
