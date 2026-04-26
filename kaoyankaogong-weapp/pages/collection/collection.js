const app = getApp()

Page({
  data: {
    activeTab: 'info',
    favorites: [],
    hasMore: true,
    page: 1,
    pageSize: 10,
    loading: false
  },

  onLoad() {
    this.fetchFavorites();
  },

  onShow() {
    this.setData({ page: 1, favorites: [], hasMore: true });
    this.fetchFavorites();
  },

  switchTab(e) {
    const tab = e.currentTarget.dataset.tab;
    if (tab === this.data.activeTab) return;
    this.setData({
      activeTab: tab,
      page: 1,
      favorites: [],
      hasMore: true
    });
    this.fetchFavorites();
  },

  async fetchFavorites() {
    if (this.data.loading) return;

    this.setData({ loading: true });

    try {
      const app = getApp();
      
      if (!app.globalData.userInfo) {
        this.setData({ loading: false });
        return;
      }

      if (this.data.activeTab === 'info') {
        await this.fetchInfoFavorites(app);
      } else {
        await this.fetchMaterialFavorites(app);
      }
    } catch (error) {
      console.error('获取收藏失败:', error);
    } finally {
      this.setData({ loading: false });
    }
  },

  async fetchInfoFavorites(app) {
    try {
      const response = await app.request({
        url: '/users/favorites',
        data: {
          page: this.data.page,
          page_size: this.data.pageSize
        }
      });

      if (response.success) {
        const items = (response.data.items || []).map(item => ({
          id: item.id,
          info_id: item.info_id,
          category: item.category,
          title: item.title || '',
          summary: item.summary || '',
          publish_time: item.publish_time || '',
          created_at: item.created_at || '',
          type: 'info'
        }));
        
        const favorites = this.data.page === 1 ? items : [...this.data.favorites, ...items];
        this.setData({
          favorites,
          hasMore: items.length === this.data.pageSize,
          page: this.data.page + 1
        });
      }
    } catch (error) {
      console.error('获取情报收藏失败:', error);
    }
  },

  async fetchMaterialFavorites(app) {
    try {
      const response = await app.request({
        url: '/learning_materials/favorites',
        data: {
          page: this.data.page,
          page_size: this.data.pageSize
        }
      });

      if (response.success) {
        const items = (response.data.items || []).map(item => ({
          id: item.id,
          info_id: item.id,
          category: item.type,
          title: item.title || '',
          summary: item.description || '',
          publish_time: item.upload_time || '',
          created_at: item.created_at || '',
          type: 'material'
        }));
        
        const favorites = this.data.page === 1 ? items : [...this.data.favorites, ...items];
        this.setData({
          favorites,
          hasMore: items.length === this.data.pageSize,
          page: this.data.page + 1
        });
      }
    } catch (error) {
      console.error('获取资料收藏失败:', error);
    }
  },

  loadMore() {
    this.fetchFavorites();
  },

  async deleteFavorite(e) {
    const infoId = e.currentTarget.dataset.infoId;
    const category = e.currentTarget.dataset.category;
    const type = e.currentTarget.dataset.type;
    const index = e.currentTarget.dataset.index;
    
    wx.showModal({
      title: '确认删除',
      content: '确定要取消收藏该内容吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            const app = getApp();
            let response;
            
            if (type === 'material') {
              response = await app.request({
                url: `/learning_materials/materials/${infoId}/favorite`,
                method: 'DELETE'
              });
            } else {
              response = await app.request({
                url: `/users/favorites/${infoId}/${category}`,
                method: 'DELETE'
              });
            }

            if (response.success) {
              const favorites = this.data.favorites.filter(
                (item, i) => i !== index
              );
              this.setData({ favorites });
              wx.showToast({ title: '取消收藏成功', icon: 'success' });
            } else {
              wx.showToast({ title: '取消收藏失败', icon: 'none' });
            }
          } catch (error) {
            console.error('取消收藏失败:', error);
            wx.showToast({ title: '取消收藏失败', icon: 'none' });
          }
        }
      }
    });
  },

  goToDetail(e) {
    const infoId = e.currentTarget.dataset.infoId;
    const category = e.currentTarget.dataset.category;
    const type = e.currentTarget.dataset.type;
    
    if (type === 'material') {
      wx.navigateTo({
        url: `/pages/learning-materials/learning-materials?material_id=${infoId}`
      });
    } else {
      wx.navigateTo({
        url: `/pages/detail/detail?id=${infoId}&category=${category}`
      });
    }
  },

  onReachBottom() {
    this.loadMore();
  },

  onPullDownRefresh() {
    this.setData({
      favorites: [],
      hasMore: true,
      page: 1
    });
    this.fetchFavorites();
    wx.stopPullDownRefresh();
  }
});
