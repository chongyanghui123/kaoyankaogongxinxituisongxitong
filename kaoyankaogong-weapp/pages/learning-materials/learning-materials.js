// pages/learning-materials/learning-materials.js
const app = getApp()

Page({
  data: {
    materials: [],
    categories: [],
    categoryOptions: [{value: '', text: '全部'}],
    categoryFilterName: '全部',
    loading: false,
    currentPage: 1,
    pageSize: 10,
    total: 0,
    searchQuery: '',
    typeFilter: '',
    categoryFilter: '',
    showDetail: false,
    currentMaterial: {},
    comments: [],
    showRateDialog: false,
    ratingValue: 0,
    currentRatingMaterialId: 0,
    showCommentDialog: false,
    commentContent: '',
    userRatings: {},
    userFavorites: {},
    userInfo: null,
    baseUrl: 'http://localhost:8000'
  },

  onLoad(options) {
    // 获取用户信息
    const app = getApp()
    let userInfo = app.globalData.userInfo
    

    
    if (!userInfo) {
      userInfo = wx.getStorageSync('userInfo')
      if (userInfo) {
        app.globalData.userInfo = userInfo
      }
    }
    
    this.setData({ userInfo: userInfo })
    
    // 调试信息

    
    // 检查是否有 material_id 参数
    if (options.material_id) {
      // 转换为数字类型
      const materialId = parseInt(options.material_id)
      // 直接显示对应的学习资料详情
      this.getMaterialDetail(materialId)
    } else {
      // 加载学习资料列表
      this.getCategories()
      this.getMaterials()
    }
  },

  // 获取资料详情
  getMaterialDetail(materialId) {
    wx.showLoading({ title: '加载中...' })
    wx.request({
      url: app.globalData.baseUrl + `/learning_materials/materials/${materialId}`,
      method: 'GET',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token
      },
      success: (res) => {
        if (res.data.success) {
          // 处理图片路径
          let materialData = res.data.data
          if (materialData.cover_image) {
            // 保持相对路径，让小程序通过后端 API 获取图片
          }
          
          this.setData({
            showDetail: true,
            currentMaterial: materialData
          })
          
          // 加载评论
          this.getComments(materialId)
          
          // 检查收藏状态
          this.checkFavoriteStatus(materialId).then(isFavorite => {
            const userFavorites = { ...this.data.userFavorites }
            userFavorites[materialId] = isFavorite
            this.setData({ userFavorites })
          })
        } else {
          wx.showToast({ title: '获取详情失败', icon: 'none' })
        }
      },
      fail: (err) => {
        wx.showToast({ title: '网络错误', icon: 'none' })
      },
      complete: () => {
        wx.hideLoading()
      }
    })
  },

  // 获取资料分类列表
  getCategories() {
    wx.showLoading({ title: '加载中...' })
    // 根据当前类型筛选获取对应的分类
    const type = this.data.typeFilter
    const url = type ? `${app.globalData.baseUrl}/learning_materials/categories?type=${type}` : `${app.globalData.baseUrl}/learning_materials/categories?type=3`
    
    wx.request({
      url: url,
      method: 'GET',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token
      },
      success: (res) => {
        if (res.data.success) {
          const categories = res.data.data
          const categoryOptions = [{value: '', text: '全部'}]
          categories.forEach(c => {
            categoryOptions.push({value: c.id.toString(), text: c.name})
          })
          this.setData({ 
            categories: categories,
            categoryOptions: categoryOptions
          })
          // 更新分类筛选名称
          this.updateCategoryFilterName()
        } else {
          wx.showToast({ title: '获取分类失败', icon: 'none' })
        }
      },
      fail: (err) => {
        wx.showToast({ title: '网络错误', icon: 'none' })
      },
      complete: () => {
        wx.hideLoading()
      }
    })
  },

  // 更新分类筛选名称
  updateCategoryFilterName() {
    const { categoryFilter, categories } = this.data
    if (categoryFilter) {
      const category = categories.find(c => c.id.toString() === categoryFilter)
      this.setData({ categoryFilterName: category ? category.name : '全部' })
    } else {
      this.setData({ categoryFilterName: '全部' })
    }
  },

  // 检查资料收藏状态
  checkRatingStatus(materialId) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: app.globalData.baseUrl + `/learning_materials/materials/${materialId}/rating`,
        method: 'GET',
        header: {
          'Authorization': 'Bearer ' + app.globalData.token
        },
        success: (res) => {
          if (res.data.success && res.data.data) {
            resolve(res.data.data.is_rated)
          } else {
            resolve(false)
          }
        },
        fail: (err) => {
          resolve(false)
        }
      })
    })
  },

  checkFavoriteStatus(materialId) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: app.globalData.baseUrl + `/learning_materials/materials/${materialId}/favorite`,
        method: 'GET',
        header: {
          'Authorization': 'Bearer ' + app.globalData.token
        },
        success: (res) => {
          if (res.data.success) {
            resolve(res.data.data.is_favorited)
          } else {
            resolve(false)
          }
        },
        fail: (err) => {
          resolve(false)
        }
      })
    })
  },

  // 获取学习资料列表
  async getMaterials() {
    this.setData({ loading: true })
    const data = {
      page: this.data.currentPage,
      page_size: this.data.pageSize,
      keyword: this.data.searchQuery
    }
    if (this.data.typeFilter) {
      data.type = this.data.typeFilter
    }
    if (this.data.categoryFilter) {
      data.category_id = this.data.categoryFilter
    }
    wx.request({
      url: app.globalData.baseUrl + '/learning_materials/materials',
      method: 'GET',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token
      },
      data: data,
      success: async (res) => {
        if (res.data.success) {
          // 处理图片路径
          const materials = res.data.data.items || []
          materials.forEach(material => {
            if (material.cover_image) {
              // 确保图片路径是正确的格式
              if (!material.cover_image.startsWith('/')) {
                material.cover_image = '/' + material.cover_image
              }
              // 打印图片路径用于调试
              console.log('图片路径:', material.cover_image)
            }
          })
          
          // 检查每个资料的收藏状态和评分状态
          const userFavorites = { ...this.data.userFavorites }
          const userRatings = { ...this.data.userRatings }
          for (const material of materials) {
            const isFavorite = await this.checkFavoriteStatus(material.id)
            userFavorites[material.id] = isFavorite
            
            const hasRated = await this.checkRatingStatus(material.id)
            userRatings[material.id] = hasRated
          }
          
          this.setData({
            materials: materials,
            total: res.data.data.total,
            userFavorites: userFavorites,
            userRatings: userRatings
          })
        } else {
          this.setData({ materials: [], total: 0 })
        }
      },
      fail: (err) => {
        this.setData({ materials: [], total: 0 })
        wx.showToast({ title: '网络错误', icon: 'none' })
      },
      complete: () => {
        this.setData({ loading: false })
      }
    })
  },

  // 处理搜索
  handleSearch(e) {
    this.setData({ searchQuery: e.detail.value })
  },

  // 提交搜索
  submitSearch() {
    this.setData({ currentPage: 1 })
    this.getMaterials()
  },

  // 处理类型筛选
  handleTypeChange(e) {
    this.setData({ typeFilter: e.detail.value, currentPage: 1, categoryFilter: '' })
    this.getCategories() // 重新获取对应的分类列表
    this.getMaterials() // 重新获取资料列表
  },

  // 处理分类筛选
  handleCategoryChange(e) {
    this.setData({ categoryFilter: e.detail.value, currentPage: 1 })
    this.updateCategoryFilterName()
    this.getMaterials()
  },

  // 显示资料详情
  showMaterialDetail(e) {
    const materialId = e.currentTarget.dataset.id
    const material = this.data.materials.find(m => m.id === materialId)
    
    // 确保用户信息是最新的
    const app = getApp()
    let userInfo = app.globalData.userInfo
    if (!userInfo) {
      userInfo = wx.getStorageSync('userInfo')
      if (userInfo) {
        app.globalData.userInfo = userInfo
      }
    }
    this.setData({ userInfo: userInfo })
    

    
    if (material) {
      // 保持相对路径，让小程序通过后端 API 获取图片
      this.setData({ currentMaterial: material })
      // 获取评论
      this.getComments(materialId)
      this.setData({ showDetail: true })
    }
  },

  // 获取评论
  getComments(materialId) {
    wx.request({
      url: app.globalData.baseUrl + `/learning_materials/materials/${materialId}/comments`,
      method: 'GET',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token
      },
      success: (res) => {
        if (res.data.success) {
          const comments = res.data.data.items || []
          
          const flattenedComments = this.flattenComments(comments)
          
          this.setData({ comments: flattenedComments })
        } else {
          this.setData({ comments: [] })
        }
      },
      fail: (err) => {
        console.error('获取评论请求失败:', err)
        this.setData({ comments: [] })
      }
    })
  },

  flattenComments(comments, depth = 0) {
    let result = []
    for (const comment of comments) {
      result.push({
        ...comment,
        depth: depth
      })
      if (comment.replies && comment.replies.length > 0) {
        result = result.concat(this.flattenComments(comment.replies, depth + 1))
      }
    }
    return result
  },

  // 关闭详情
  closeDetail() {
    // 检查是否是从收藏页面跳转过来的
    const pages = getCurrentPages()
    const currentPage = pages[pages.length - 1]
    const prevPage = pages[pages.length - 2]
    
    if (currentPage.options.material_id && prevPage.route === 'pages/collection/collection') {
      // 是从收藏页面跳转过来的，直接返回
      wx.navigateBack()
    } else {
      // 正常关闭弹窗
      this.setData({ showDetail: false })
    }
  },

  // 下载资料
  downloadMaterial(e) {
    const materialId = e.currentTarget.dataset.id
    wx.showLoading({ title: '下载中...' })
    wx.downloadFile({
      url: app.globalData.baseUrl + `/learning_materials/materials/${materialId}/download`,
      header: {
        'Authorization': 'Bearer ' + app.globalData.token
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const material = this.data.materials.find(m => m.id === materialId) || this.data.currentMaterial
          const filename = material ? material.title : `资料${materialId}`
          const fileExtension = material ? material.file_extension : '.pdf'
          
          const fs = wx.getFileSystemManager()
          fs.saveFile({
            tempFilePath: res.tempFilePath,
            filePath: wx.env.USER_DATA_PATH + '/' + filename + fileExtension,
            success: (res) => {
              wx.hideLoading()
              wx.showToast({ title: '下载成功', icon: 'success' })
            },
            fail: (err) => {
              wx.hideLoading()
              wx.showToast({ title: '保存失败', icon: 'none' })
            }
          })
        } else {
          wx.hideLoading()
          wx.showToast({ title: '下载失败', icon: 'none' })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        wx.showToast({ title: '下载失败', icon: 'none' })
      }
    })
  },

  // 评分资料
  rateMaterial(e) {
    const materialId = e.currentTarget.dataset.id
    // 检查用户是否已经评分过该资料
    if (this.data.userRatings[materialId]) {
      wx.showToast({ title: '您已经评价过该资料，不能重复评价', icon: 'none' })
      return
    }
    this.setData({
      currentRatingMaterialId: materialId,
      ratingValue: 0,
      showRateDialog: true
    })
  },

  // 处理评分变化
  handleRatingChange(e) {
    const score = parseInt(e.currentTarget.dataset.value)
    const starCount = score / 2
    this.setData({ ratingValue: starCount })
  },

  // 提交评分
  submitRating() {
    if (this.data.ratingValue === 0) {
      wx.showToast({ title: '请选择评分', icon: 'none' })
      return
    }
    
    const actualScore = this.data.ratingValue * 2
    
    wx.showLoading({ title: '提交中...' })
    wx.request({
      url: app.globalData.baseUrl + `/learning_materials/materials/${this.data.currentRatingMaterialId}/rating`,
      method: 'POST',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token,
        'Content-Type': 'application/json'
      },
      data: JSON.stringify({
        rating: actualScore
      }),
      success: (res) => {
        wx.hideLoading()
        if (res.statusCode === 400) {
          this.setData({ showRateDialog: false })
          wx.showToast({ title: res.data.message || '您已经评价过该资料', icon: 'none' })
          const userRatings = { ...this.data.userRatings }
          userRatings[this.data.currentRatingMaterialId] = true
          this.setData({ userRatings: userRatings })
        } else if (res.data.success) {
          wx.showToast({ title: '评分成功', icon: 'success' })
          const userRatings = { ...this.data.userRatings }
          userRatings[this.data.currentRatingMaterialId] = true
          this.setData({ 
            showRateDialog: false,
            userRatings: userRatings
          })
          this.getMaterials()
        } else {
          wx.showToast({ title: res.data.message || '评分失败', icon: 'none' })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        // 处理 400 错误，显示后端返回的错误信息

        if (err.errMsg && err.errMsg.includes('400')) {
          // 更新userRatings，记录用户已经评分的资料ID
          const userRatings = { ...this.data.userRatings }
          userRatings[this.data.currentRatingMaterialId] = true
          this.setData({ 
            showRateDialog: false,
            userRatings: userRatings
          })
          wx.showToast({ title: '您已经评价过该资料，不能重复评价', icon: 'none' })
        } else {
          wx.showToast({ title: '网络错误', icon: 'none' })
        }
      }
    })
  },

  // 取消评分
  cancelRating() {
    this.setData({ showRateDialog: false })
  },

  // 显示评论对话框
  showCommentDialog(parentCommentId = null) {
    this.setData({ 
      showCommentDialog: true,
      parentCommentId: parentCommentId
    })
  },

  // 回复评论
  onReply(e) {
    this.showCommentDialog(e.currentTarget.dataset.parentId || e.currentTarget.dataset.id)
  },

  // 处理评论内容变化
  handleCommentChange(e) {
    this.setData({ commentContent: e.detail.value })
  },

  // 提交评论
  submitComment() {
    if (!this.data.commentContent) {
      wx.showToast({ title: '请输入评论内容', icon: 'none' })
      return
    }
    
    const materialId = this.data.currentMaterial.id
    const data = {
      comment: this.data.commentContent
    }
    
    // 如果有父评论ID，添加到数据中
    if (this.data.parentCommentId) {
      let parentCommentId = this.data.parentCommentId
      // 确保 parentCommentId 是有效的数字或字符串
      if (typeof parentCommentId === 'object') {
        // 如果是对象，尝试获取 id 属性
        parentCommentId = parentCommentId.id || null
      }
      // 如果是字符串，尝试转换为数字
      if (typeof parentCommentId === 'string') {
        parentCommentId = parseInt(parentCommentId) || null
      }
      if (parentCommentId) {
        data.parent_comment_id = parentCommentId
      }
    }
    
    // 打印调试信息

    
    wx.showLoading({ title: '提交中...' })
    wx.request({
      url: app.globalData.baseUrl + `/learning_materials/materials/${materialId}/comment`,
      method: 'POST',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token,
        'Content-Type': 'application/json'
      },
      data: JSON.stringify(data),
      success: (res) => {

        wx.hideLoading()
        if (res.data.success) {
          wx.showToast({ title: '评论成功', icon: 'success' })
          this.setData({ 
            showCommentDialog: false,
            commentContent: '',
            parentCommentId: null
          })
          // 刷新评论
          this.getComments(materialId)
        } else {
          wx.showToast({ title: res.data.message || '评论失败', icon: 'none' })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        // 处理 400 错误，显示后端返回的错误信息

        if (err.errMsg && err.errMsg.includes('400')) {
          this.setData({ 
            showCommentDialog: false,
            commentContent: '',
            parentCommentId: null
          })
          wx.showToast({ title: '您已经评论过该资料，不能重复评论', icon: 'none' })
        } else {
          wx.showToast({ title: '网络错误', icon: 'none' })
        }
      }
    })
  },

  // 添加收藏
  addFavorite(materialId) {
    wx.showLoading({ title: '收藏中...' })
    wx.request({
      url: app.globalData.baseUrl + `/learning_materials/materials/${materialId}/favorite`,
      method: 'POST',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token
      },
      success: (res) => {
        wx.hideLoading()
        if (res.data.success) {
          const userFavorites = { ...this.data.userFavorites }
          userFavorites[materialId] = true
          this.setData({ userFavorites: userFavorites })
          wx.showToast({ title: '收藏成功', icon: 'success' })
        } else {
          wx.showToast({ title: res.data.message || '收藏失败', icon: 'none' })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        wx.showToast({ title: '网络错误', icon: 'none' })
      }
    })
  },

  // 取消收藏
  removeFavorite(materialId) {
    wx.showLoading({ title: '取消收藏中...' })
    wx.request({
      url: app.globalData.baseUrl + `/learning_materials/materials/${materialId}/favorite`,
      method: 'DELETE',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token
      },
      success: (res) => {
        wx.hideLoading()
        if (res.data.success) {
          const userFavorites = { ...this.data.userFavorites }
          userFavorites[materialId] = false
          this.setData({ userFavorites: userFavorites })
          wx.showToast({ title: '取消收藏成功', icon: 'success' })
        } else {
          wx.showToast({ title: res.data.message || '取消收藏失败', icon: 'none' })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        wx.showToast({ title: '网络错误', icon: 'none' })
      }
    })
  },

  // 处理收藏按钮点击
  handleFavorite(e) {
    const materialId = e.currentTarget.dataset.id
    const isFavorite = this.data.userFavorites[materialId] || false
    
    if (isFavorite) {
      this.removeFavorite(materialId)
    } else {
      this.addFavorite(materialId)
    }
  },

  // 取消评论
  cancelComment() {
    this.setData({ showCommentDialog: false, commentContent: '' })
  },

  // 删除评论
  deleteComment(e) {
    const commentId = e.currentTarget.dataset.commentId
    const materialId = this.data.currentMaterial.id
    
    wx.showModal({
      title: '确认删除',
      content: '确定要删除该评论及其所有回复吗？',
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({ title: '删除中...' })
          wx.request({
            url: app.globalData.baseUrl + `/learning_materials/materials/${materialId}/comments/${commentId}`,
            method: 'DELETE',
            header: {
              'Authorization': 'Bearer ' + app.globalData.token
            },
            success: (res) => {
              wx.hideLoading()
              if (res.data.success) {
                wx.showToast({ title: '删除成功', icon: 'success' })
                // 刷新评论
                this.getComments(materialId)
              } else {
                wx.showToast({ title: res.data.message || '删除失败', icon: 'none' })
              }
            },
            fail: (err) => {
              wx.hideLoading()
              wx.showToast({ title: '网络错误', icon: 'none' })
            }
          })
        }
      }
    })
  },

  // 跳转到下载历史
  goToDownloadHistory() {
    wx.navigateTo({ url: '/pages/download-history/download-history' })
  },

  // 处理分页
  handleLoadMore() {
    if (this.data.materials.length < this.data.total) {
      this.setData({ currentPage: this.data.currentPage + 1 })
      this.getMaterials()
    }
  }
})
