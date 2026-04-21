// detail.js
Page({
  data: {
    info: {
      id: 1,
      title: '2026年考研初试时间确定，12月26-28日举行',
      content: '教育部公布了2026年全国硕士研究生招生考试初试时间，定于12月26日至28日举行。考生需提前做好准备，合理安排复习计划。\n\n根据教育部发布的通知，2026年全国硕士研究生招生考试初试将于12月26日至28日举行，具体安排如下：\n\n12月26日：上午 思想政治理论、管理类综合能力\n12月26日：下午 外国语\n12月27日：上午 业务课一\n12月27日：下午 业务课二\n12月28日：考试时间超过3小时的科目\n\n考生需注意以下事项：\n1. 及时关注研招网发布的最新信息\n2. 按照规定时间打印准考证\n3. 提前熟悉考点位置和交通路线\n4. 准备好必要的考试用品\n5. 保持良好的心态和作息习惯\n\n祝愿所有考生考试顺利！',
      type: '考研',
      time: '2026-04-18',
      source: '教育部官网'
    },
    relatedInfo: [
      {
        id: 3,
        title: '多所高校2026年考研招生简章发布',
        time: '2026-04-16'
      },
      {
        id: 4,
        title: '2026年考研大纲发布，这些变化要注意',
        time: '2026-04-15'
      }
    ],
    isCollected: false
  },
  
  onLoad(options) {
    // 页面加载时执行

    
    const id = options.id;
    this.fetchInfoDetail(id);
    this.fetchRelatedInfo(id);
  },
  
  onShow() {
    // 页面显示时执行

  },
  
  // 获取情报详情
  async fetchInfoDetail(id) {
    try {
      const app = getApp();
      
      // 调用API获取情报详情
      const response = await app.request({
        url: `/info/detail/${id}`
      });
      
      if (response.success) {
        this.setData({
          info: response.data
        });
      }
    } catch (error) {
      console.error('获取情报详情失败:', error);
      // 使用模拟数据
    }
  },
  
  // 获取相关情报
  async fetchRelatedInfo(id) {
    try {
      const app = getApp();
      
      // 调用API获取相关情报
      const response = await app.request({
        url: `/info/related/${id}`
      });
      
      if (response.success) {
        this.setData({
          relatedInfo: response.data
        });
      }
    } catch (error) {
      console.error('获取相关情报失败:', error);
      // 使用模拟数据
    }
  },
  
  // 收藏情报
  collectInfo() {
    this.setData({
      isCollected: !this.data.isCollected
    });
    
    wx.showToast({
      title: this.data.isCollected ? '收藏成功' : '取消收藏',
      icon: 'success'
    });
  },
  
  // 分享情报
  shareInfo() {
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    });
  },
  
  // 复制链接
  copyLink() {
    const link = `https://api.example.com/info/${this.data.info.id}`;
    wx.setClipboardData({
      data: link,
      success() {
        wx.showToast({
          title: '链接已复制',
          icon: 'success'
        });
      }
    });
  },
  
  // 导航到相关情报详情
  navigateToDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?id=${id}`
    });
  },
  
  // 分享到好友
  onShareAppMessage() {
    return {
      title: this.data.info.title,
      path: `/pages/detail/detail?id=${this.data.info.id}`,
      imageUrl: ''
    };
  },
  
  // 分享到朋友圈
  onShareTimeline() {
    return {
      title: this.data.info.title,
      query: `id=${this.data.info.id}`
    };
  }
});