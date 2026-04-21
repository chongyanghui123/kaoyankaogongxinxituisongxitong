// pages/collection/collection.js
const app = getApp()

Page({
  data: {
    favorites: [],
    hasMore: true,
    page: 1,
    pageSize: 10,
    loading: false
  },

  onLoad() {

    this.fetchFavorites();
  },

  // 获取收藏内容（根据用户类型自动判断）
  async fetchFavorites() {
    if (this.data.loading || !this.data.hasMore) {
      return;
    }

    this.setData({ loading: true });

    try {
      const app = getApp();
      
      // 检查用户是否登录
      if (!app.globalData.userInfo) {
        this.setData({ loading: false });
        return;
      }

      // 获取传统收藏（kaoyan和kaogong信息）
      const [traditionalResponse, materialResponse] = await Promise.all([
        app.request({
          url: '/users/favorites',
          data: {
            page: this.data.page,
            page_size: this.data.pageSize
          }
        }),
        // 获取学习资料收藏
        app.request({
          url: '/learning_materials/favorites',
          data: {
            page: this.data.page,
            page_size: this.data.pageSize
          }
        })
      ]);

      const allFavorites = [];

      // 处理传统收藏
      if (traditionalResponse.success) {
        const traditionalItems = traditionalResponse.data.items || [];
        traditionalItems.forEach(item => {
          allFavorites.push({
            id: item.id,
            info_id: item.info_id,
            category: item.category,
            title: item.title || '',
            summary: item.summary || '',
            publish_time: item.publish_time || '',
            created_at: item.created_at || '',
            type: 'traditional' // 标记为传统收藏
          });
        });
      }

      // 处理学习资料收藏
      if (materialResponse.success) {
        const materialItems = materialResponse.data.items || [];
        materialItems.forEach(item => {
          allFavorites.push({
            id: item.id,
            info_id: item.id, // 使用资料ID作为info_id
            category: item.type, // 学习资料类型作为分类
            title: item.title,
            summary: item.description || '',
            publish_time: item.upload_time || '',
            created_at: new Date().toISOString(), // 临时时间
            type: 'material' // 标记为学习资料收藏
          });
        });
      }

      // 按创建时间排序
      allFavorites.sort((a, b) => {
        return new Date(b.created_at) - new Date(a.created_at);
      });

      const hasMore = traditionalResponse.success && (traditionalResponse.data.items || []).length === this.data.pageSize ||
                     materialResponse.success && (materialResponse.data.items || []).length === this.data.pageSize;

      // 合并数据
      const favorites = this.data.page === 1 
        ? allFavorites 
        : [...this.data.favorites, ...allFavorites];

      this.setData({
        favorites,
        hasMore: hasMore,
        page: this.data.page + 1
      });
    } catch (error) {
      console.error('获取收藏失败:', error);
    } finally {
      this.setData({ loading: false });
    }
  },

  // 加载更多
  loadMore() {
    this.fetchFavorites();
  },

  // 删除收藏
  async deleteFavorite(e) {
    const { infoId, category, type } = e.currentTarget.dataset;
    
    wx.showModal({
      title: '确认删除',
      content: '确定要取消收藏该内容吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            const app = getApp();
            
            let response;
            
            if (type === 'material') {
              // 删除学习资料收藏
              response = await app.request({
                url: `/learning_materials/materials/${infoId}/favorite`,
                method: 'DELETE'
              });
            } else {
              // 删除传统收藏
              response = await app.request({
                url: `/users/favorites/${infoId}/${category}`,
                method: 'DELETE'
              });
            }

            if (response.success) {
              // 更新收藏列表
              const favorites = this.data.favorites.filter(
                item => item.info_id !== infoId
              );
              
              this.setData({ favorites });

              wx.showToast({
                title: '取消收藏成功',
                icon: 'success'
              });
            } else {
              wx.showToast({
                title: '取消收藏失败',
                icon: 'none'
              });
            }
          } catch (error) {
            console.error('取消收藏失败:', error);
            wx.showToast({
              title: '取消收藏失败',
              icon: 'none'
            });
          }
        }
      }
    });
  },

  // 显示学习资料详情
  goToDetail(e) {
    const { infoId, category, type } = e.currentTarget.dataset;
    

    
    if (type === 'material') {
      // 跳转到学习资料页面并显示对应资料详情
      wx.navigateTo({
        url: `/pages/learning-materials/learning-materials?material_id=${infoId}`
      });
    } else {
      // 跳转到传统详情页
      wx.navigateTo({
        url: `/pages/detail/detail?info_id=${infoId}&category=${category}`
      });
    }
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {
    this.loadMore();
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {
    // 重置数据并重新加载
    this.setData({
      favorites: [],
      hasMore: true,
      page: 1
    });
    
    this.fetchFavorites();
    
    // 停止下拉刷新
    wx.stopPullDownRefresh();
  }
})