Page({
  data: {
    groupId: null,
    title: '',
    content: '',
    images: []
  },

  onLoad(options) {
    if (options.groupId) {
      this.setData({ groupId: options.groupId });
    }
  },

  onTitleInput(e) {
    this.setData({ title: e.detail.value });
  },

  onContentInput(e) {
    this.setData({ content: e.detail.value });
  },

  chooseImage() {
    wx.chooseImage({
      count: 9 - this.data.images.length,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        const tempFilePaths = res.tempFilePaths;
        this.setData({
          images: [...this.data.images, ...tempFilePaths]
        });
      }
    });
  },

  removeImage(e) {
    const index = e.currentTarget.dataset.index;
    const images = this.data.images;
    images.splice(index, 1);
    this.setData({ images });
  },

  submitPost() {
    if (!this.data.title.trim()) {
      wx.showToast({
        title: '请输入标题',
        icon: 'none'
      });
      return;
    }

    if (!this.data.content.trim()) {
      wx.showToast({
        title: '请输入内容',
        icon: 'none'
      });
      return;
    }

    wx.showLoading({ title: '发布中...' });

    // 先上传图片
    if (this.data.images.length > 0) {
      this.uploadImages().then(imageUrls => {
        this.createPost(imageUrls);
      }).catch(() => {
        wx.hideLoading();
        wx.showToast({
          title: '图片上传失败',
          icon: 'none'
        });
      });
    } else {
      this.createPost([]);
    }
  },

  uploadImages() {
    return new Promise((resolve, reject) => {
      const app = getApp();
      const uploadTasks = this.data.images.map(imagePath => {
        return new Promise((res, rej) => {
          wx.uploadFile({
            url: `${app.globalData.baseUrl}/community/upload`,
            filePath: imagePath,
            name: 'file',
            header: {
              'Authorization': `Bearer ${wx.getStorageSync('token')}`
            },
            success: (response) => {
              const data = JSON.parse(response.data);
              if (data.url) {
                res(data.url);
              } else {
                rej(new Error('上传失败'));
              }
            },
            fail: rej
          });
        });
      });

      Promise.all(uploadTasks).then(resolve).catch(reject);
    });
  },

  createPost(imageUrls) {
    const app = getApp();
    wx.request({
      url: `${app.globalData.baseUrl}/community/groups/${this.data.groupId}/posts`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      },
      data: {
        title: this.data.title,
        content: this.data.content,
        image_urls: imageUrls.join(',')
      },
      success: (res) => {
        wx.hideLoading();
        if (res.statusCode === 200) {
          wx.showToast({
            title: '发布成功',
            icon: 'success'
          });
          setTimeout(() => {
            wx.navigateBack();
          }, 1500);
        } else {
          wx.showToast({
            title: res.data.detail || '发布失败',
            icon: 'none'
          });
        }
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        });
      }
    });
  }
});
