Page({
  data: {
    title: '',
    content: '',
    category: '',
    tags: '',
    categories: ['考研', '公务员', '数学', '英语', '政治', '专业课', '其他'],
    categoryIndex: 0
  },

  onTitleInput(e) {
    this.setData({ title: e.detail.value });
  },

  onContentInput(e) {
    this.setData({ content: e.detail.value });
  },

  onCategoryChange(e) {
    const index = parseInt(e.detail.value);
    this.setData({
      categoryIndex: index,
      category: this.data.categories[index]
    });
  },

  onTagsInput(e) {
    this.setData({ tags: e.detail.value });
  },

  submitQuestion() {
    if (!this.data.title.trim()) {
      wx.showToast({
        title: '请输入问题标题',
        icon: 'none'
      });
      return;
    }

    if (!this.data.content.trim()) {
      wx.showToast({
        title: '请输入问题内容',
        icon: 'none'
      });
      return;
    }

    const app = getApp();
    wx.request({
      url: `${app.globalData.baseUrl}/community/questions`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      },
      data: {
        title: this.data.title,
        content: this.data.content,
        category: this.data.category,
        tags: this.data.tags
      },
      success: (res) => {
        if (res.statusCode === 200) {
          wx.showToast({
            title: '提交成功',
            icon: 'success'
          });
          setTimeout(() => {
            wx.navigateBack();
          }, 1500);
        } else {
          wx.showToast({
            title: res.data.detail || '提交失败',
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
