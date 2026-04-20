// info.js
Page({
  data: {
    infoList: [],
    currentTime: '全部',
    timeList: [
      { label: '全部', value: '' },
      { label: '近一周', value: 'week' },
      { label: '近一月', value: 'month' },
      { label: '近三月', value: 'quarter' }
    ],
    showTimePicker: false,
    timeIndex: [0],
    loading: false,
    hasMore: true,
    page: 1,
    pageSize: 10,
    userInfo: null
  },
  
  onLoad(options) {
    // 页面加载时执行
    console.log('情报列表页加载', options);
    
    if (options.search) {
      this.setData({
        searchText: options.search
      });
    }
    
    // 加载数据
    this.fetchData();
  },
  
  onShow() {
    // 页面显示时执行
    console.log('情报列表页显示');
  },
  
  // 格式化时间
  formatTime(timeStr) {
    console.log('格式化时间前:', timeStr);
    // 处理 ISO 格式的时间字符串
    if (timeStr && typeof timeStr === 'string') {
      // 替换 'T' 为空格
      timeStr = timeStr.replace('T', ' ');
      // 移除毫秒部分
      if (timeStr.includes('.')) {
        timeStr = timeStr.split('.')[0];
      }
    }
    console.log('格式化时间后:', timeStr);
    return timeStr;
  },

  // 获取数据
  async fetchData() {
    try {
      const app = getApp();
      
      // 检查用户是否登录
      if (!app.globalData.userInfo) {
        // 用户未登录，跳转到登录页面
        wx.showToast({
          title: '请先登录',
          icon: 'none'
        });
        
        wx.navigateTo({
          url: '/pages/user/user'
        });
        
        this.setData({ loading: false });
        return;
      }
      
      this.setData({ loading: true });
      
      // 构建请求参数
      const params = {
        page: this.data.page,
        page_size: this.data.pageSize
      };
      
      if (this.data.currentTime !== '全部') {
        params.time = this.data.currentTime;
      }
      
      if (this.data.searchText) {
        params.search = this.data.searchText;
      }
      
      // 调用API获取情报列表
      const response = await app.request({
        url: '/info/list',
        data: params
      });
      
      if (response.success) {
        const newData = response.data.items.map(item => ({
          ...item,
          time: this.formatTime(item.time)
        }));
        const hasMore = response.data.total > this.data.infoList.length + newData.length;
        
        this.setData({
          infoList: this.data.page === 1 ? newData : [...this.data.infoList, ...newData],
          hasMore: hasMore,
          loading: false
        });
      } else {
        this.setData({ loading: false });
        wx.showToast({
          title: '获取数据失败',
          icon: 'none'
        });
      }
    } catch (error) {
      console.error('获取数据失败:', error);
      this.setData({ loading: false });
    }
  },
  
  // 加载更多
  loadMore() {
    if (!this.data.loading && this.data.hasMore) {
      this.setData({
        page: this.data.page + 1
      });
      this.fetchData();
    }
  },
  
  // 显示时间选择器
  showTimePicker() {
    this.setData({
      showTimePicker: true
    });
  },
  
  // 绑定时间选择
  bindTimeChange(e) {
    const index = e.detail.value[0];
    const selectedTime = this.data.timeList[index];
    
    this.setData({
      currentTime: selectedTime.label,
      showTimePicker: false,
      page: 1,
      infoList: []
    });
    
    this.fetchData();
  },
  
  // 导航到情报详情
  navigateToDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  }
});