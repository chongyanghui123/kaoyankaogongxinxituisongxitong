// groups.js
Page({
  data: {
    hotGroups: [],
    recommendedGroups: [],
    loading: false,
    error: '',
    searchText: '',
    userInfo: null
  },

  onLoad() {
    console.log('学习小组页面加载');
    const userInfo = wx.getStorageSync('userInfo');
    this.setData({ userInfo });
    this.loadGroups();
  },

  onShow() {
    console.log('学习小组页面显示');
    this.loadGroups();
  },

  loadGroups() {
    this.setData({ loading: true, error: '' });
    
    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    
    wx.request({
      url: `${app.globalData.baseUrl}/community/groups`,
      method: 'GET',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      success: (res) => {
        console.log('获取小组列表成功:', res.data);
        const groups = res.data || [];
        
        // 获取用户加入的小组
        this.checkMembershipForGroups(groups, token);
      },
      fail: (err) => {
        console.error('获取小组列表失败:', err);
        this.setData({ error: '网络错误，请稍后重试', loading: false });
      }
    });
  },

  checkMembershipForGroups(groups, token) {
    const app = getApp();
    const userInfo = this.data.userInfo;
    
    if (!userInfo || !token) {
      // 用户未登录，所有小组都显示"加入"
      const sortedGroups = [...groups].sort((a, b) => b.member_count - a.member_count);
      const hotGroups = sortedGroups.slice(0, 3).map(group => ({
        id: group.id,
        name: group.name,
        avatar: group.avatar || `/${group.name.charAt(0)}`,
        members: group.member_count,
        activeToday: group.active_today || 0,
        isMember: false
      }));
      const recommendedGroups = sortedGroups.slice(3, 7).map(group => ({
        id: group.id,
        name: group.name,
        avatar: group.avatar || `/${group.name.charAt(0)}`,
        members: group.member_count,
        activeToday: group.active_today || 0,
        isMember: false
      }));
      this.setData({ hotGroups, recommendedGroups, loading: false });
      return;
    }

    // 检查每个小组的成员状态
    const checkPromises = groups.map(group => {
      return new Promise((resolve) => {
        wx.request({
          url: `${app.globalData.baseUrl}/community/groups/${group.id}/members`,
          method: 'GET',
          header: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          success: (res) => {
            if (res.statusCode === 200) {
              const members = res.data || [];
              const isMember = members.some(member => member.user_id === userInfo.id && member.status === 1);
              resolve({ ...group, isMember });
            } else {
              resolve({ ...group, isMember: false });
            }
          },
          fail: () => {
            resolve({ ...group, isMember: false });
          }
        });
      });
    });

    Promise.all(checkPromises).then(groupsWithMembership => {
      const sortedGroups = [...groupsWithMembership].sort((a, b) => b.member_count - a.member_count);
      const hotGroups = sortedGroups.slice(0, 3).map(group => ({
        id: group.id,
        name: group.name,
        avatar: group.avatar || `/${group.name.charAt(0)}`,
        members: group.member_count,
        activeToday: group.active_today || 0,
        isMember: group.isMember
      }));
      const recommendedGroups = sortedGroups.slice(3, 7).map(group => ({
        id: group.id,
        name: group.name,
        avatar: group.avatar || `/${group.name.charAt(0)}`,
        members: group.member_count,
        activeToday: group.active_today || 0,
        isMember: group.isMember
      }));
      this.setData({ hotGroups, recommendedGroups, loading: false });
    });
  },

  toggleMembership(e) {
    const groupId = e.currentTarget.dataset.id;
    const index = e.currentTarget.dataset.index;
    
    const isLoggedIn = wx.getStorageSync('isLoggedIn');
    if (!isLoggedIn) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      setTimeout(() => {
        wx.navigateTo({
          url: '/pages/user/user'
        });
      }, 1500);
      return;
    }

    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    
    // 查找当前小组的状态
    let group = this.data.hotGroups.find(g => g.id === groupId);
    let groupType = 'hotGroups';
    if (!group) {
      group = this.data.recommendedGroups.find(g => g.id === groupId);
      groupType = 'recommendedGroups';
    }

    const url = group.isMember 
      ? `${app.globalData.baseUrl}/community/groups/${groupId}/leave`
      : `${app.globalData.baseUrl}/community/groups/${groupId}/join`;

    wx.request({
      url: url,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      success: (res) => {
        if (res.statusCode === 200) {
          wx.showToast({
            title: group.isMember ? '退出成功' : '加入成功',
            icon: 'success'
          });
          
          // 更新小组状态
          const updateData = {};
          updateData[`${groupType}[${index}].isMember`] = !group.isMember;
          this.setData(updateData);
          
          // 更新成员数量
          const memberUpdate = {};
          memberUpdate[`${groupType}[${index}].members`] = group.isMember ? group.members - 1 : group.members + 1;
          this.setData(memberUpdate);
        } else {
          wx.showToast({
            title: res.data.detail || '操作失败',
            icon: 'none'
          });
        }
      },
      fail: () => {
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        });
      }
    });
  },

  navigateToGroupDetail(e) {
    const groupId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/community/group-detail/group-detail?id=${groupId}`
    });
  },

  createGroup() {
    const isLoggedIn = wx.getStorageSync('isLoggedIn');
    if (!isLoggedIn) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      setTimeout(() => {
        wx.navigateTo({
          url: '/pages/user/user'
        });
      }, 1500);
      return;
    }

    wx.navigateTo({
      url: '/pages/community/create-group/create-group'
    });
  },

  onSearch(e) {
    this.setData({ searchText: e.detail.value });
  }
});
