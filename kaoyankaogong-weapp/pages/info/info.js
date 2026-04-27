// info.js
Page({
  data: {
    infoList: [],
    activeTab: 'latest',
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
    userInfo: null,
    userVipType: 0,
    searchText: '',
    kaoyanTotal: 0,
    kaogongTotal: 0,
    todayCount: 0
  },
  
  onLoad(options) {
    if (options.search) {
      this.setData({ searchText: options.search });
    }
  },
  
  onShow() {
    this.getUserInfo();
    this.setData({ page: 1, infoList: [], hasMore: true });
    this.fetchData();
  },
  
  getUserInfo() {
    const app = getApp();
    let userInfo = app.globalData.userInfo;
    if (!userInfo) {
      userInfo = wx.getStorageSync('userInfo');
      if (userInfo) {
        app.globalData.userInfo = userInfo;
      }
    }
    
    const vipType = userInfo ? (userInfo.vip_type || userInfo.is_vip_active || 3) : 0;
    this.setData({ 
      userInfo: userInfo,
      userVipType: vipType
    });
    
    if (userInfo && this.data.activeTab === 'latest') {
      this.setData({ activeTab: 'recommend' });
    }
  },
  
  formatTime(timeStr) {
    if (timeStr && typeof timeStr === 'string') {
      timeStr = timeStr.replace('T', ' ');
      if (timeStr.includes('.')) {
        timeStr = timeStr.split('.')[0];
      }
    }
    return timeStr;
  },
  
  switchTab(e) {
    const tab = e.currentTarget.dataset.tab;
    this.setData({
      activeTab: tab,
      page: 1,
      infoList: [],
      hasMore: true
    });
    this.fetchData();
  },
  
  async fetchData() {
    try {
      const app = getApp();
      const isLogin = !!app.globalData.userInfo;
      
      this.setData({ loading: true });
      
      if (this.data.activeTab === 'recommend' && isLogin) {
        await this.fetchRecommendData(app);
      } else if (this.data.activeTab === 'hot') {
        await this.fetchHotData(app, isLogin);
      } else {
        await this.fetchLatestData(app, isLogin);
      }
    } catch (error) {
      console.error('获取数据失败:', error);
      this.setData({ loading: false });
    }
  },
  
  async fetchRecommendData(app) {
    this.setData({ loading: true });
    
    const params = {
      page: this.data.page,
      page_size: this.data.pageSize
    };
    
    if (this.data.currentTime !== '全部') {
      params.time = this.data.timeList.find(t => t.label === this.data.currentTime)?.value || '';
    }
    if (this.data.searchText) {
      params.search = this.data.searchText;
    }
    
    try {
      const response = await app.request({
        url: '/info/list',
        data: params
      });
      
      if (response.success) {
        const newData = response.data.items.map(item => ({
          ...item,
          time: this.formatTime(item.time)
        }));
        const total = response.data.total || 0;
        this.setData({
          infoList: this.data.page === 1 ? newData : [...this.data.infoList, ...newData],
          hasMore: total > this.data.infoList.length + newData.length,
          loading: false
        });
        this.checkFavorites();
      } else {
        this.setData({ loading: false });
      }
    } catch (error) {
      console.error('获取推荐数据失败:', error);
      this.setData({ loading: false });
    }
  },
  
  async fetchLatestData(app, isLogin) {
    const params = { limit: this.data.pageSize };
    if (this.data.currentTime !== '全部') {
      const timeValue = this.data.timeList.find(t => t.label === this.data.currentTime)?.value;
      if (timeValue) params.time = timeValue;
    }
    if (this.data.searchText) {
      params.search = this.data.searchText;
    }
    
    try {
      const response = await app.request({
        url: '/info/public/latest',
        data: params
      });
      
      if (response.success) {
        const data = response.data;
        const items = (data.items || []).map(item => ({
          ...item,
          time: this.formatTime(item.time)
        }));
        this.setData({
          infoList: this.data.page === 1 ? items : [...this.data.infoList, ...items],
          kaoyanTotal: data.kaoyan_total || 0,
          kaogongTotal: data.kaogong_total || 0,
          todayCount: data.today_count || 0,
          hasMore: false,
          loading: false
        });
        this.checkFavorites();
      } else {
        this.setData({ loading: false });
      }
    } catch (error) {
      console.error('获取最新数据失败:', error);
      this.setData({ loading: false });
    }
  },
  
  async fetchHotData(app, isLogin) {
    try {
      const response = await app.request({
        url: '/info/public/hot',
        data: { limit: this.data.pageSize }
      });
      
      if (response.success) {
        const items = (response.data || []).map(item => ({
          ...item,
          time: this.formatTime(item.time)
        }));
        this.setData({
          infoList: items,
          hasMore: false,
          loading: false
        });
        this.checkFavorites();
      } else {
        this.setData({ loading: false });
      }
    } catch (error) {
      console.error('获取热门数据失败:', error);
      this.setData({ loading: false });
    }
  },
  
  loadMore() {
    if (!this.data.loading && this.data.hasMore) {
      this.setData({ page: this.data.page + 1 });
      this.fetchData();
    }
  },
  
  onSearchInput(e) {
    this.setData({ searchText: e.detail.value });
  },
  
  onSearchConfirm() {
    this.setData({ page: 1, infoList: [], hasMore: true });
    this.fetchData();
  },
  
  showTimePicker() {
    this.setData({ showTimePicker: true });
  },
  
  bindTimeChange(e) {
    const index = e.detail.value[0];
    const selectedTime = this.data.timeList[index];
    this.setData({
      currentTime: selectedTime.label,
      showTimePicker: false,
      page: 1,
      infoList: [],
      hasMore: true
    });
    this.fetchData();
  },
  
  navigateToDetail(e) {
    const id = e.currentTarget.dataset.id;
    const type = e.currentTarget.dataset.type || '';
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}&type=${type}`
    });
  },
  
  navigateToLogin() {
    wx.switchTab({
      url: '/pages/user/user'
    });
  },
  
  async toggleFavorite(e) {
    const app = getApp();
    if (!app.globalData.userInfo) {
      this.navigateToLogin();
      return;
    }
    
    const id = e.currentTarget.dataset.id;
    const type = e.currentTarget.dataset.type;
    const index = e.currentTarget.dataset.index;
    const item = this.data.infoList[index];
    const category = type === '考研' ? 1 : 2;
    
    try {
      let response;
      if (item.is_favorited) {
        response = await app.request({
          url: `/users/favorites/${id}/${category}`,
          method: 'DELETE'
        });
      } else {
        response = await app.request({
          url: `/users/favorites/${id}/${category}`,
          method: 'POST'
        });
      }
      
      if (response.success) {
        const newFavState = !item.is_favorited;
        const newFavCount = newFavState
          ? (item.favorite_count || 0) + 1
          : Math.max(0, (item.favorite_count || 0) - 1);
        
        this.setData({
          [`infoList[${index}].is_favorited`]: newFavState,
          [`infoList[${index}].favorite_count`]: newFavCount
        });
        
        wx.showToast({
          title: newFavState ? '收藏成功' : '取消收藏',
          icon: 'none',
          duration: 1000
        });
      }
    } catch (error) {
      console.error('收藏操作失败:', error);
      wx.showToast({
        title: '操作失败',
        icon: 'none'
      });
    }
  },
  
  async checkFavorites() {
    const app = getApp();
    if (!app.globalData.userInfo) return;
    
    try {
      const response = await app.request({
        url: '/users/favorites',
        data: { page: 1, page_size: 100 }
      });
      
      if (response.success) {
        const favMap = {};
        (response.data.items || []).forEach(fav => {
          const key = `${fav.category}_${fav.info_id}`;
          favMap[key] = true;
        });
        
        const updatedList = this.data.infoList.map(item => {
          const category = item.type === '考研' ? 1 : 2;
          const key = `${category}_${item.id}`;
          return { ...item, is_favorited: !!favMap[key] };
        });
        
        this.setData({ infoList: updatedList });
      }
    } catch (error) {
      console.error('检查收藏状态失败:', error);
    }
  }
});
