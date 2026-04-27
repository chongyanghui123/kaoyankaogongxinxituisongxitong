Page({
  data: {
    groupId: null,
    posts: [],
    loading: false
  },

  onLoad(options) {
    if (options.groupId) {
      this.setData({ groupId: options.groupId });
      this.loadPosts();
    }
  },

  loadPosts() {
    this.setData({ loading: true });
    
    const app = getApp();
    wx.request({
      url: `${app.globalData.baseUrl}/community/groups/${this.data.groupId}/posts`,
      method: 'GET',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({ 
            posts: res.data || [],
            loading: false 
          });
        } else {
          wx.showToast({
            title: '加载失败',
            icon: 'none'
          });
          this.setData({ loading: false });
        }
      },
      fail: () => {
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        });
        this.setData({ loading: false });
      }
    });
  },

  navigateToPost(e) {
    const postId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/community/post-detail/post-detail?id=${postId}`
    });
  },

  createPost() {
    const isLoggedIn = wx.getStorageSync('isLoggedIn');
    if (!isLoggedIn) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }

    wx.navigateTo({
      url: `/pages/community/create-post/create-post?groupId=${this.data.groupId}`
    });
  },

  onPullDownRefresh() {
    this.loadPosts();
    wx.stopPullDownRefresh();
  }
});
