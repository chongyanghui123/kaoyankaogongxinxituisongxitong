// pages/download-history/download-history.js
const app = getApp()

Page({
  data: {
    downloads: [],
    loading: false,
    currentPage: 1,
    pageSize: 10,
    total: 0,
    typeFilter: '', // 类型筛选：''-全部，'1'-考研，'2'-考公
    typeOptions: [{value: '', text: '全部'}, {value: '1', text: '考研'}, {value: '2', text: '考公'}]
  },

  onLoad() {
    this.getDownloads()
  },

  // 获取下载记录
  getDownloads() {
    this.setData({ loading: true })
    const data = {
      page: this.data.currentPage,
      page_size: this.data.pageSize
    }
    if (this.data.typeFilter) {
      data.type = this.data.typeFilter
    }
    wx.request({
      url: app.globalData.baseUrl + '/learning_materials/downloads',
      method: 'GET',
      header: {
        'Authorization': 'Bearer ' + app.globalData.token
      },
      data: data,
      success: (res) => {
        if (res.data.success) {
          // 处理图片路径，使用相对路径
          const downloads = res.data.data.items || []
          downloads.forEach(download => {
            if (download.cover_image) {
              // 保持相对路径，让小程序通过后端 API 获取图片
              // 例如：/uploads/d171db14-3828-4049-8053-6885092c2b7e.png
            }
          })
          this.setData({
            downloads: downloads,
            total: res.data.data.total
          })
        } else {
          this.setData({ downloads: [], total: 0 })
        }
      },
      fail: (err) => {
        this.setData({ downloads: [], total: 0 })
        wx.showToast({ title: '网络错误', icon: 'none' })
      },
      complete: () => {
        this.setData({ loading: false })
      }
    })
  },

  // 重新下载
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
          const download = this.data.downloads.find(d => d.material_id === materialId)
          const filename = download ? download.material_title : `资料${materialId}`
          const fileExtension = '.pdf' // 默认扩展名
          
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

  // 查看文件
  viewFile(e) {
    const materialId = e.currentTarget.dataset.id
    const materialTitle = e.currentTarget.dataset.title
    const filename = materialTitle || `资料${materialId}`
    const fileExtension = '.pdf' // 默认扩展名
    const filePath = wx.env.USER_DATA_PATH + '/' + filename + fileExtension
    
    const fs = wx.getFileSystemManager()
    // 检查文件是否存在
    fs.access({
      path: filePath,
      success: () => {
        // 文件存在，打开文件
        wx.openDocument({
          filePath: filePath,
          showMenu: true,
          success: (res) => {

          },
          fail: (err) => {
            wx.showToast({ title: '打开文件失败', icon: 'none' })
          }
        })
      },
      fail: () => {
        // 文件不存在，提示用户重新下载
        wx.showToast({ title: '文件不存在，请重新下载', icon: 'none' })
      }
    })
  },

  // 删除下载记录
  deleteDownload(e) {
    const downloadId = e.currentTarget.dataset.id
    
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这条下载记录吗？',
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({ title: '删除中...' })
          wx.request({
            url: app.globalData.baseUrl + `/learning_materials/downloads/${downloadId}`,
            method: 'DELETE',
            header: {
              'Authorization': 'Bearer ' + app.globalData.token
            },
            success: (res) => {
              wx.hideLoading()
              if (res.data.success) {
                wx.showToast({ title: '删除成功', icon: 'success' })
                // 刷新下载记录列表
                this.getDownloads()
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

  // 处理类型筛选
  handleTypeChange(e) {
    this.setData({ typeFilter: e.detail.value, currentPage: 1 })
    this.getDownloads()
  },

  // 处理分页
  handleLoadMore() {
    if (this.data.downloads.length < this.data.total) {
      this.setData({ currentPage: this.data.currentPage + 1 })
      this.getDownloads()
    }
  }
})
