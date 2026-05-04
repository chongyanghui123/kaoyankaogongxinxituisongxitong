Page({
  data: {
    userInfo: null,
    products: [],
    selectedPlan: null,
    subscriptionType: '未订阅',
    remainingDays: 0,
    showPayModal: false,
    selectedPayMethod: 'wechat',
    loading: true,
    step: 1,
    isVipUser: false,
    userInfoForm: {
      real_name: '',
      email: '',
      phone: '',
      gender: 0,
      birthdate: ''
    },
    genderOptions: ['男', '女'],
    educationOptions: ['不限', '本科', '硕士', '博士'],
    freshGraduateOptions: ['不限', '是', '否'],
    provinceOptions: [],
    schoolOptions: [],
    allSchools: [],
    kaoyanTypeOptions: ['招生简章', '考试大纲', '成绩查询', '复试通知', '录取通知'],
    kaogongPositionTypeOptions: ['公务员', '事业单位', '教师', '医疗'],
    kaoyanRequirements: {
      provinces: '',
      provincesList: [],
      schools: '',
      schoolsList: [],
      majors: '',
      types: '',
      keywords: '',
      typesIndex: 0
    },
    kaogongRequirements: {
      provinces: '',
      provincesList: [],
      position_types: '',
      majors: '',
      education: 0,
      is_fresh_graduate: 0,
      keywords: '',
      positionTypesIndex: 0
    },
    showMultiSelectModal: false,
    multiSelectTitle: '',
    multiSelectType: '',
    multiSelectTarget: '',
    multiSelectOptions: [],
    multiSelectSelectedCount: 0,
    schoolSearchKeyword: ''
  },

  onLoad() {
    this.getUserInfo();
    this.loadProducts();
    this.getProvinces();
  },

  onShow() {
    this.getUserInfo();
  },

  async getUserInfo() {
    const app = getApp();
    try {
      const response = await app.request({
        url: '/auth/user',
        method: 'GET'
      });

      if (response.success && response.data) {
        const userInfo = response.data;
        app.globalData.userInfo = userInfo;
        wx.setStorageSync('userInfo', userInfo);
        this.setData({ userInfo });
        this.calculateSubscriptionInfo();
      } else {
        // 如果请求失败，从本地存储获取
        let userInfo = app.globalData.userInfo;
        if (!userInfo) {
          userInfo = wx.getStorageSync('userInfo');
          if (userInfo) app.globalData.userInfo = userInfo;
        }

        if (userInfo) {
          this.setData({ userInfo });
          this.calculateSubscriptionInfo();
        }
      }
    } catch (error) {
      console.error('获取用户信息失败:', error);
      // 如果请求失败，从本地存储获取
      let userInfo = app.globalData.userInfo;
      if (!userInfo) {
        userInfo = wx.getStorageSync('userInfo');
        if (userInfo) app.globalData.userInfo = userInfo;
      }

      if (userInfo) {
        this.setData({ userInfo });
        this.calculateSubscriptionInfo();
      }
    }
  },

  calculateSubscriptionInfo() {
    const userInfo = this.data.userInfo;
    if (!userInfo) return;

    let subscriptionType = '未订阅';
    if (userInfo.vip_type === 1) subscriptionType = '考研套餐';
    else if (userInfo.vip_type === 2) subscriptionType = '考公套餐';
    else if (userInfo.vip_type === 3) subscriptionType = '双赛道套餐';

    let remainingDays = 0;
    if (userInfo.is_vip && userInfo.vip_end_time) {
      const endTime = new Date(userInfo.vip_end_time);
      const now = new Date();
      const diffTime = endTime - now;
      remainingDays = Math.max(0, Math.ceil(diffTime / (1000 * 60 * 60 * 24)));
    }

    // 如果用户已经是VIP，直接跳到需求填写步骤
    if (userInfo.is_vip && remainingDays > 0) {
      this.setData({ 
        subscriptionType, 
        remainingDays,
        step: 2,
        showKaoyan: userInfo.vip_type === 1 || userInfo.vip_type === 3,
        showKaogong: userInfo.vip_type === 2 || userInfo.vip_type === 3,
        isVipUser: true
      });
    } else {
      this.setData({ subscriptionType, remainingDays, isVipUser: false });
    }
  },

  async loadProducts() {
    const app = getApp();
    try {
      const response = await app.request({
        url: '/payments/products',
        method: 'GET'
      });

      if (response.success !== false && Array.isArray(response)) {
        const products = response.map(p => ({
          id: p.id,
          name: p.name,
          price: p.price,
          period: p.duration ? (p.duration >= 365 ? '年' : p.duration >= 30 ? '月' : '天') : '月',
          duration: p.duration || 30,
          type: p.type,
          description: p.description || '',
          features: this.getFeaturesByType(p.type, p.description)
        }));

        this.setData({
          products,
          selectedPlan: products.length > 0 ? products[0].id : null,
          loading: false
        });
      } else {
        this.setData({
          products: this.getDefaultPlans(),
          selectedPlan: 1,
          loading: false
        });
      }
    } catch (error) {
      console.error('加载产品失败:', error);
      this.setData({
        products: this.getDefaultPlans(),
        selectedPlan: 1,
        loading: false
      });
    }
  },

  getDefaultPlans() {
    return [
      {
        id: 1, name: '考研套餐', price: 99, period: '月', duration: 30, type: 1,
        features: ['考研情报推送', '院校动态提醒', '考试时间通知', '个性化推荐']
      },
      {
        id: 2, name: '考公套餐', price: 99, period: '月', duration: 30, type: 2,
        features: ['考公情报推送', '政策变化提醒', '报名时间通知', '个性化推荐']
      },
      {
        id: 3, name: '双赛道套餐', price: 169, period: '月', duration: 30, type: 3,
        features: ['考研+考公情报推送', '院校动态提醒', '政策变化提醒', '考试/报名时间通知', '个性化推荐']
      }
    ];
  },

  getFeaturesByType(type, description) {
    if (type === 1) return ['考研情报推送', '院校动态提醒', '考试时间通知', '个性化推荐'];
    if (type === 2) return ['考公情报推送', '政策变化提醒', '报名时间通知', '个性化推荐'];
    if (type === 3) return ['考研+考公情报推送', '院校动态提醒', '政策变化提醒', '考试/报名时间通知', '个性化推荐'];
    return ['情报推送', '个性化推荐'];
  },

  selectPlan(e) {
    this.setData({ selectedPlan: e.currentTarget.dataset.id });
  },

  goToNextStep() {
    if (!this.data.selectedPlan) {
      wx.showToast({ title: '请选择套餐', icon: 'none' });
      return;
    }
    const product = this.data.products.find(p => p.id === this.data.selectedPlan);
    if (!product) return;

    this.setData({
      step: 2,
      showKaoyan: product.type === 1 || product.type === 3,
      showKaogong: product.type === 2 || product.type === 3
    });
  },

  goToPrevStep() {
    this.setData({ step: 1 });
  },

  onKaoyanInput(e) {
    const field = e.currentTarget.dataset.field;
    this.setData({ [`kaoyanRequirements.${field}`]: e.detail.value });
  },

  onKaogongInput(e) {
    const field = e.currentTarget.dataset.field;
    this.setData({ [`kaogongRequirements.${field}`]: e.detail.value });
  },

  onUserInfoInput(e) {
    const field = e.currentTarget.dataset.field;
    this.setData({ [`userInfoForm.${field}`]: e.detail.value });
  },

  onGenderChange(e) {
    this.setData({ [`userInfoForm.gender`]: parseInt(e.detail.value) });
  },

  onBirthdateChange(e) {
    this.setData({ [`userInfoForm.birthdate`]: e.detail.value });
  },

  onKaogongEducationChange(e) {
    this.setData({ [`kaogongRequirements.education`]: parseInt(e.detail.value) });
  },

  onKaogongFreshGraduateChange(e) {
    this.setData({ [`kaogongRequirements.is_fresh_graduate`]: parseInt(e.detail.value) });
  },

  // 考研需求字段的事件处理函数
  onKaoyanProvinceChange(e) {
    const selectedIndex = e.detail.value;
    const selectedProvince = this.data.provinceOptions[selectedIndex];
    this.setData({ 
      [`kaoyanRequirements.provinces`]: selectedProvince,
      [`kaoyanRequirements.provincesIndex`]: selectedIndex
    });
    // 根据省份获取学校列表
    this.getSchoolsByProvince(selectedProvince);
    // 添加选中状态样式
    this.addSelectedStyle('kaoyan_province');
  },

  onKaoyanSchoolChange(e) {
    const selectedIndex = e.detail.value;
    const selectedSchool = this.data.schoolOptions[selectedIndex];
    this.setData({ 
      [`kaoyanRequirements.schools`]: selectedSchool,
      [`kaoyanRequirements.schoolsIndex`]: selectedIndex
    });
    // 添加选中状态样式
    this.addSelectedStyle('kaoyan_school');
  },

  onKaoyanTypeChange(e) {
    const selectedIndex = e.detail.value;
    const selectedType = this.data.kaoyanTypeOptions[selectedIndex];
    this.setData({ 
      [`kaoyanRequirements.types`]: selectedType,
      [`kaoyanRequirements.typesIndex`]: selectedIndex
    });
    // 添加选中状态样式
    this.addSelectedStyle('kaoyan_type');
  },

  // 考公需求字段的事件处理函数
  onKaogongProvinceChange(e) {
    const selectedIndex = e.detail.value;
    const selectedProvince = this.data.provinceOptions[selectedIndex];
    this.setData({ 
      [`kaogongRequirements.provinces`]: selectedProvince,
      [`kaogongRequirements.provincesIndex`]: selectedIndex
    });
    // 添加选中状态样式
    this.addSelectedStyle('kaogong_province');
  },

  onKaogongPositionTypeChange(e) {
    const selectedIndex = e.detail.value;
    const selectedPositionType = this.data.kaogongPositionTypeOptions[selectedIndex];
    this.setData({ 
      [`kaogongRequirements.position_types`]: selectedPositionType,
      [`kaogongRequirements.positionTypesIndex`]: selectedIndex
    });
    // 添加选中状态样式
    this.addSelectedStyle('kaogong_position_type');
  },

  // 显示省份多选弹窗
  showProvincePicker(e) {
    const target = e.currentTarget.dataset.type;
    const currentList = target === 'kaoyan' 
      ? this.data.kaoyanRequirements.provincesList 
      : this.data.kaogongRequirements.provincesList;
    
    const options = this.data.provinceOptions.map(p => ({
      value: p,
      label: p,
      selected: currentList.includes(p)
    }));

    this.setData({
      showMultiSelectModal: true,
      multiSelectTitle: '选择关注省份',
      multiSelectType: 'province',
      multiSelectTarget: target,
      multiSelectOptions: options,
      multiSelectSelectedCount: currentList.length
    });
  },

  // 显示学校多选弹窗
  showSchoolPicker(e) {
    const target = e.currentTarget.dataset.type;
    const provincesList = target === 'kaoyan' 
      ? this.data.kaoyanRequirements.provincesList 
      : this.data.kaogongRequirements.provincesList;
    
    if (provincesList.length === 0) {
      wx.showToast({ title: '请先选择省份', icon: 'none' });
      return;
    }

    const currentList = target === 'kaoyan' 
      ? this.data.kaoyanRequirements.schoolsList 
      : this.data.kaogongRequirements.schoolsList;

    const options = this.data.allSchools
      .filter(s => provincesList.includes(s.province))
      .map(s => ({
        value: s.name,
        label: s.name,
        province: s.province,
        selected: currentList.includes(s.name)
      }));

    this.setData({
      showMultiSelectModal: true,
      multiSelectTitle: '选择目标院校',
      multiSelectType: 'school',
      multiSelectTarget: target,
      multiSelectOptions: options,
      multiSelectSelectedCount: currentList.length,
      schoolSearchKeyword: ''
    });
  },

  // 关闭多选弹窗
  closeMultiSelectModal() {
    this.setData({ showMultiSelectModal: false });
  },

  // 切换多选项
  toggleMultiSelectItem(e) {
    const value = e.currentTarget.dataset.value;
    const options = this.data.multiSelectOptions.map(item => {
      if (item.value === value) {
        return { ...item, selected: !item.selected };
      }
      return item;
    });
    
    const selectedCount = options.filter(item => item.selected).length;
    this.setData({ multiSelectOptions: options, multiSelectSelectedCount: selectedCount });
  },

  // 学校搜索
  onSchoolSearch(e) {
    const keyword = e.detail.value.toLowerCase();
    this.setData({ schoolSearchKeyword: keyword });
    
    const target = this.data.multiSelectTarget;
    const provincesList = target === 'kaoyan' 
      ? this.data.kaoyanRequirements.provincesList 
      : this.data.kaogongRequirements.provincesList;
    const currentList = target === 'kaoyan' 
      ? this.data.kaoyanRequirements.schoolsList 
      : this.data.kaogongRequirements.schoolsList;

    let filteredSchools = this.data.allSchools.filter(s => provincesList.includes(s.province));
    
    if (keyword) {
      filteredSchools = filteredSchools.filter(s => 
        s.name.toLowerCase().includes(keyword)
      );
    }

    const options = filteredSchools.map(s => ({
      value: s.name,
      label: s.name,
      province: s.province,
      selected: currentList.includes(s.name)
    }));

    this.setData({ multiSelectOptions: options });
  },

  // 确认多选
  confirmMultiSelect() {
    const selectedItems = this.data.multiSelectOptions
      .filter(item => item.selected)
      .map(item => item.value);

    const target = this.data.multiSelectTarget;
    const type = this.data.multiSelectType;

    if (type === 'province') {
      this.setData({
        [`${target}Requirements.provincesList`]: selectedItems,
        [`${target}Requirements.provinces`]: selectedItems.join(', '),
        showMultiSelectModal: false
      });
    } else if (type === 'school') {
      this.setData({
        [`${target}Requirements.schoolsList`]: selectedItems,
        [`${target}Requirements.schools`]: selectedItems.join(', '),
        showMultiSelectModal: false
      });
    }
  },

  // 移除考研省份
  removeKaoyanProvince(e) {
    const value = e.currentTarget.dataset.value;
    const list = this.data.kaoyanRequirements.provincesList.filter(p => p !== value);
    this.setData({
      'kaoyanRequirements.provincesList': list,
      'kaoyanRequirements.provinces': list.join(', ')
    });
  },

  // 移除考研学校
  removeKaoyanSchool(e) {
    const value = e.currentTarget.dataset.value;
    const list = this.data.kaoyanRequirements.schoolsList.filter(s => s !== value);
    this.setData({
      'kaoyanRequirements.schoolsList': list,
      'kaoyanRequirements.schools': list.join(', ')
    });
  },

  // 移除考公省份
  removeKaogongProvince(e) {
    const value = e.currentTarget.dataset.value;
    const list = this.data.kaogongRequirements.provincesList.filter(p => p !== value);
    this.setData({
      'kaogongRequirements.provincesList': list,
      'kaogongRequirements.provinces': list.join(', ')
    });
  },

  // 获取省份列表
  async getProvinces() {
    try {
      const app = getApp();
      const response = await app.request({
        url: '/utils/provinces',
        method: 'GET'
      });
      
      if (response.success) {
        this.setData({
          provinceOptions: response.data
        });
      } else {
        this.setData({
          provinceOptions: [
            '上海', '云南', '内蒙古', '北京', '吉林', '四川', '天津', 
            '宁夏', '安徽', '山东', '山西', '广东', '广西', '新疆', 
            '江苏', '江西', '河北', '河南', '浙江', '海南', '湖北', 
            '湖南', '甘肃', '福建', '西藏', '贵州', '辽宁', '重庆', 
            '陕西', '青海', '黑龙江'
          ]
        });
      }
      // 获取所有学校
      this.getAllSchools();
    } catch (error) {
      console.error('获取省份列表失败:', error);
      this.setData({
        provinceOptions: [
          '上海', '云南', '内蒙古', '北京', '吉林', '四川', '天津', 
          '宁夏', '安徽', '山东', '山西', '广东', '广西', '新疆', 
          '江苏', '江西', '河北', '河南', '浙江', '海南', '湖北', 
          '湖南', '甘肃', '福建', '西藏', '贵州', '辽宁', '重庆', 
          '陕西', '青海', '黑龙江'
        ]
      });
      this.getAllSchools();
    }
  },

  // 获取所有学校
  async getAllSchools() {
    try {
      const app = getApp();
      const response = await app.request({
        url: '/utils/all-schools',
        method: 'GET'
      });
      
      if (response.success && response.data) {
        this.setData({ allSchools: response.data });
      } else {
        this.setDefaultSchools();
      }
    } catch (error) {
      console.error('获取学校列表失败:', error);
      this.setDefaultSchools();
    }
  },

  setDefaultSchools() {
    const defaultSchools = [
      { name: '北京大学', province: '北京' },
      { name: '清华大学', province: '北京' },
      { name: '复旦大学', province: '上海' },
      { name: '上海交通大学', province: '上海' },
      { name: '中山大学', province: '广东' },
      { name: '华南理工大学', province: '广东' },
      { name: '浙江大学', province: '浙江' },
      { name: '南京大学', province: '江苏' },
      { name: '武汉大学', province: '湖北' },
      { name: '华中科技大学', province: '湖北' }
    ];
    this.setData({ allSchools: defaultSchools });
  },

  // 根据省份获取学校列表
  async getSchoolsByProvince(province) {
    try {
      const app = getApp();
      const response = await app.request({
        url: `/utils/schools?province=${encodeURIComponent(province)}`,
        method: 'GET'
      });
      
      if (response.success) {
        this.setData({
          schoolOptions: response.data
        });
      } else {
        this.setData({
          schoolOptions: ['中山大学', '华南理工大学', '暨南大学', '华南师范大学', '华南农业大学']
        });
      }
    } catch (error) {
      console.error('获取学校列表失败:', error);
      this.setData({
        schoolOptions: ['中山大学', '华南理工大学', '暨南大学', '华南师范大学', '华南农业大学']
      });
    }
  },

  // 添加选中状态样式
  addSelectedStyle(field) {
    // 这里可以根据需要添加选中状态的样式
    // 例如，给对应的picker添加selected类名
    console.log('选中字段:', field);
  },

  pay() {
    this.setData({ showPayModal: true });
  },

  closePayModal() {
    this.setData({ showPayModal: false });
  },

  selectPayMethod(e) {
    this.setData({ selectedPayMethod: e.currentTarget.dataset.method });
  },

  async confirmPay() {
    const app = getApp();
    const product = this.data.products.find(p => p.id === this.data.selectedPlan);
    if (!product) return;

    // 验证用户基本信息
    if (!this.data.userInfoForm.real_name.trim()) {
      wx.showToast({ title: '请输入真实姓名', icon: 'none' });
      return;
    }
    if (!this.data.userInfoForm.email.trim()) {
      wx.showToast({ title: '请输入邮箱地址', icon: 'none' });
      return;
    }
    if (!this.data.userInfoForm.phone.trim()) {
      wx.showToast({ title: '请输入手机号', icon: 'none' });
      return;
    }
    if (!this.data.userInfoForm.birthdate) {
      wx.showToast({ title: '请选择出生日期', icon: 'none' });
      return;
    }

    const userRequirements = {
      username: this.data.userInfoForm.real_name,
      email: this.data.userInfoForm.email,
      phone: this.data.userInfoForm.phone,
      real_name: this.data.userInfoForm.real_name,
      gender: this.data.userInfoForm.gender,
      birthdate: this.data.userInfoForm.birthdate
    };
    if (product.type === 1 || product.type === 3) {
      userRequirements.kaoyan_requirements = {
        provinces: this.data.kaoyanRequirements.provincesList,
        schools: this.data.kaoyanRequirements.schoolsList,
        majors: this.data.kaoyanRequirements.majors,
        types: this.data.kaoyanRequirements.types,
        keywords: this.data.kaoyanRequirements.keywords
      };
    }
    if (product.type === 2 || product.type === 3) {
      userRequirements.kaogong_requirements = {
        provinces: this.data.kaogongRequirements.provincesList,
        position_types: this.data.kaogongRequirements.position_types,
        majors: this.data.kaogongRequirements.majors,
        education: this.data.educationOptions[this.data.kaogongRequirements.education],
        is_fresh_graduate: this.data.freshGraduateOptions[this.data.kaogongRequirements.is_fresh_graduate],
        keywords: this.data.kaogongRequirements.keywords
      };
    }

    try {
      wx.showLoading({ title: '创建订单...' });

      const createResponse = await app.request({
        url: '/payments/orders',
        method: 'POST',
        data: {
          product_id: this.data.selectedPlan,
          payment_method: this.data.selectedPayMethod === 'wechat' ? 1 : 2,
          user_requirements: userRequirements
        }
      });

      wx.hideLoading();

      if (!createResponse.success) {
        wx.showToast({ title: createResponse.message || '创建订单失败', icon: 'none' });
        return;
      }

      const orderId = createResponse.data.order_id || createResponse.data.id;

      wx.showLoading({ title: '支付中...' });

      const payResponse = await app.request({
        url: `/payments/orders/${orderId}/pay`,
        method: 'POST',
        data: {
          pay_method: this.data.selectedPayMethod,
          mock_payment: true
        }
      });

      wx.hideLoading();

      if (payResponse.success) {
        if (payResponse.data && payResponse.data.mock) {
          wx.showToast({ title: '支付成功', icon: 'success' });
          this.closePayModal();
          this.getUserInfo();

          setTimeout(() => {
            wx.switchTab({ url: '/pages/user/user' });
          }, 1500);
        } else if (payResponse.data && payResponse.data.timeStamp) {
          // 微信支付
          wx.requestPayment({
            timeStamp: payResponse.data.timeStamp,
            nonceStr: payResponse.data.nonceStr,
            package: payResponse.data.package,
            signType: payResponse.data.signType,
            paySign: payResponse.data.paySign,
            success: () => {
              wx.showToast({ title: '支付成功', icon: 'success' });
              this.closePayModal();
              this.getUserInfo();
              setTimeout(() => {
                wx.switchTab({ url: '/pages/user/user' });
              }, 1500);
            },
            fail: () => {
              wx.showToast({ title: '支付取消', icon: 'none' });
            }
          });
        } else if (payResponse.data && payResponse.data.alipay_trade_no) {
          // 支付宝支付
          wx.showToast({ title: '支付成功', icon: 'success' });
          this.closePayModal();
          this.getUserInfo();
          setTimeout(() => {
            wx.switchTab({ url: '/pages/user/user' });
          }, 1500);
        }
      } else {
        // 如果需要确认模拟支付
        if (payResponse.data && payResponse.data.need_confirmation) {
          wx.showModal({
            title: '提示',
            content: payResponse.message || '支付配置未完成，是否使用模拟支付？',
            success: (res) => {
              if (res.confirm) {
                this.confirmPayWithMock();
              }
            }
          });
        } else {
          wx.showToast({ title: payResponse.message || '支付失败', icon: 'none' });
        }
      }
    } catch (error) {
      wx.hideLoading();
      console.error('支付失败:', error);
      wx.showToast({ title: '支付失败，请重试', icon: 'none' });
    }
  },

  async confirmPayWithMock() {
    const app = getApp();
    const product = this.data.products.find(p => p.id === this.data.selectedPlan);
    if (!product) return;

    const userRequirements = {
      username: this.data.userInfoForm.real_name,
      email: this.data.userInfoForm.email,
      phone: this.data.userInfoForm.phone,
      real_name: this.data.userInfoForm.real_name,
      gender: this.data.userInfoForm.gender,
      birthdate: this.data.userInfoForm.birthdate
    };
    if (product.type === 1 || product.type === 3) {
      userRequirements.kaoyan_requirements = {
        provinces: this.data.kaoyanRequirements.provincesList,
        schools: this.data.kaoyanRequirements.schoolsList,
        majors: this.data.kaoyanRequirements.majors,
        types: this.data.kaoyanRequirements.types,
        keywords: this.data.kaoyanRequirements.keywords
      };
    }
    if (product.type === 2 || product.type === 3) {
      userRequirements.kaogong_requirements = {
        provinces: this.data.kaogongRequirements.provincesList,
        position_types: this.data.kaogongRequirements.position_types,
        majors: this.data.kaogongRequirements.majors,
        education: this.data.educationOptions[this.data.kaogongRequirements.education],
        is_fresh_graduate: this.data.freshGraduateOptions[this.data.kaogongRequirements.is_fresh_graduate],
        keywords: this.data.kaogongRequirements.keywords
      };
    }

    try {
      wx.showLoading({ title: '创建订单...' });

      const createResponse = await app.request({
        url: '/payments/orders',
        method: 'POST',
        data: {
          product_id: this.data.selectedPlan,
          payment_method: this.data.selectedPayMethod === 'wechat' ? 1 : 2,
          user_requirements: userRequirements
        }
      });

      wx.hideLoading();

      if (!createResponse.success) {
        wx.showToast({ title: createResponse.message || '创建订单失败', icon: 'none' });
        return;
      }

      const orderId = createResponse.data.order_id || createResponse.data.id;

      wx.showLoading({ title: '支付中...' });

      const payResponse = await app.request({
        url: `/payments/orders/${orderId}/pay`,
        method: 'POST',
        data: {
          pay_method: this.data.selectedPayMethod,
          mock_payment: true
        }
      });

      wx.hideLoading();

      if (payResponse.success) {
        wx.showToast({ title: '支付成功', icon: 'success' });
        this.closePayModal();
        this.getUserInfo();
        setTimeout(() => {
          wx.switchTab({ url: '/pages/user/user' });
        }, 1500);
      } else {
        wx.showToast({ title: payResponse.message || '支付失败', icon: 'none' });
      }
    } catch (error) {
      wx.hideLoading();
      console.error('支付失败:', error);
      wx.showToast({ title: '支付失败，请重试', icon: 'none' });
    }
  },

  // VIP用户保存需求配置
  async saveRequirements() {
    const app = getApp();
    const userInfo = this.data.userInfo;
    
    if (!this.data.userInfoForm.real_name.trim()) {
      wx.showToast({ title: '请输入真实姓名', icon: 'none' });
      return;
    }
    if (!this.data.userInfoForm.email.trim()) {
      wx.showToast({ title: '请输入邮箱地址', icon: 'none' });
      return;
    }
    if (!this.data.userInfoForm.phone.trim()) {
      wx.showToast({ title: '请输入手机号', icon: 'none' });
      return;
    }

    const userRequirements = {
      username: this.data.userInfoForm.real_name,
      email: this.data.userInfoForm.email,
      phone: this.data.userInfoForm.phone,
      real_name: this.data.userInfoForm.real_name,
      gender: this.data.userInfoForm.gender,
      birthdate: this.data.userInfoForm.birthdate
    };

    if (userInfo.vip_type === 1 || userInfo.vip_type === 3) {
      userRequirements.kaoyan_requirements = {
        provinces: this.data.kaoyanRequirements.provincesList,
        schools: this.data.kaoyanRequirements.schoolsList,
        majors: this.data.kaoyanRequirements.majors,
        types: this.data.kaoyanRequirements.types,
        keywords: this.data.kaoyanRequirements.keywords
      };
    }
    if (userInfo.vip_type === 2 || userInfo.vip_type === 3) {
      userRequirements.kaogong_requirements = {
        provinces: this.data.kaogongRequirements.provincesList,
        position_types: this.data.kaogongRequirements.position_types,
        majors: this.data.kaogongRequirements.majors,
        education: this.data.educationOptions[this.data.kaogongRequirements.education],
        is_fresh_graduate: this.data.freshGraduateOptions[this.data.kaogongRequirements.is_fresh_graduate],
        keywords: this.data.kaogongRequirements.keywords
      };
    }

    try {
      wx.showLoading({ title: '保存中...' });

      const response = await app.request({
        url: '/users/subscription',
        method: 'PUT',
        data: {
          subscribe_type: userInfo.vip_type,
          config: {
            kaoyan: userRequirements.kaoyan_requirements || {},
            kaogong: userRequirements.kaogong_requirements || {}
          }
        }
      });

      wx.hideLoading();

      if (response.success) {
        wx.showToast({ title: '保存成功', icon: 'success' });
        setTimeout(() => {
          wx.switchTab({ url: '/pages/user/user' });
        }, 1500);
      } else {
        wx.showToast({ title: response.message || '保存失败', icon: 'none' });
      }
    } catch (error) {
      wx.hideLoading();
      console.error('保存失败:', error);
      wx.showToast({ title: '保存失败，请重试', icon: 'none' });
    }
  }
});
