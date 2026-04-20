// pages/collection/collection.js
const app = getApp()

Page({
  data: {
    favorites: [], // 收藏列表（根据用户类型自动筛选）
    hasMore: true, // 是否还有更多数据
    page: 1, // 当前页码
    pageSize: 10, // 每页数量
    loading: false, // 加载状态
    showDetail: false, // 显示详情页标志
    currentMaterialId: null, // 当前显示的学习资料ID
    currentMaterial: {}, // 当前显示的学习资料详情
    userFavorites: {}, // 存储用户已收藏的资料ID
    showRateDialog: false, // 是否显示评分弹窗
    ratingValue: 0, // 评分值
    currentRatingMaterialId: 0, // 当前评分的资料ID
    showCommentDialog: false, // 是否显示评论弹窗
    commentContent: '', // 评论内容
    currentCommentMaterialId: 0, // 当前评论的资料ID
    showDetailLoading: false, // 详情页加载状态
    userRatings: {}, // 存储用户已评分的资料ID
    userComments: {} // 存储用户已评论的资料ID
  },

  onLoad() {
    console.log('收藏页面加载');
    this.fetchFavorites(); // 加载收藏内容
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
    
    console.log('goToDetail:', e.currentTarget.dataset); // 调试信息
    
    if (type === 'material') {
      // 在收藏页面直接显示学习资料详情
      this.getMaterialDetail(infoId);
    } else {
      // 跳转到传统详情页
      wx.navigateTo({
        url: `/pages/detail/detail?info_id=${infoId}&category=${category}`
      });
    }
  },

  // 关闭学习资料详情
  closeDetail() {
    this.setData({ showDetail: false })
  },

  // 获取学习资料详情
  getMaterialDetail(materialId) {
    // 获取学习资料详情
    wx.showLoading({ title: '加载中...' });
    
    // 直接从API获取资料详情，不依赖页面列表
    wx.request({
      url: app.globalData.baseUrl + `/learning_materials/materials/${materialId}`,
      method: 'GET',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token
      },
      success: (res) => {
        if (res.data.success) {
          const material = res.data.data;
          this.setData({ 
            showDetail: true, 
            currentMaterialId: materialId,
            currentMaterial: material
          });
        }
        wx.hideLoading();
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({
          title: '获取详情失败',
          icon: 'none'
        });
      }
    });
  },

  // 关闭详情
  closeDetail() {
    this.setData({ 
      showDetail: false, 
      currentMaterialId: null,
      currentMaterial: {},
      materials: []
    });
  },

  // 格式化文件大小
  formatFileSize(size) {
    if (size < 1024) {
      return size + 'B';
    } else if (size < 1024 * 1024) {
      return (size / 1024).toFixed(1) + 'KB';
    } else if (size < 1024 * 1024 * 1024) {
      return (size / (1024 * 1024)).toFixed(1) + 'MB';
    } else {
      return (size / (1024 * 1024 * 1024)).toFixed(1) + 'GB';
    }
  },

  // 下载资料
  downloadMaterial(e) {
    const materialId = e.currentTarget.dataset.id;
    const material = this.data.materials.find(m => m.id === materialId);
    if (material) {
      // 实现下载逻辑
      wx.showToast({
        title: '下载功能开发中',
        icon: 'none'
      });
    }
  },

  // 评分
  rateMaterial(e) {
    const materialId = e.currentTarget.dataset.id;
    // 实现评分逻辑
    wx.showToast({
      title: '评分功能开发中',
      icon: 'none'
    });
  },

  // 收藏
  handleFavorite(e) {
    const materialId = e.currentTarget.dataset.id;
    // 实现收藏逻辑
    wx.showToast({
      title: '收藏功能开发中',
      icon: 'none'
    });
  },

  // 评论
  showCommentDialog(e) {
    const materialId = e.currentTarget.dataset.id;
    // 实现评论逻辑
    wx.showToast({
      title: '评论功能开发中',
      icon: 'none'
    });
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