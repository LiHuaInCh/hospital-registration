const api = require('../../utils/api');
const auth = require('../../utils/auth');

Page({
  data: {
    departments: [],
    total: 0,
    loading: true
  },

  onShow() {
    this.syncTabBar();
    if (!this.data.departments.length) {
      this.loadDepartments();
    }
  },

  onPullDownRefresh() {
    this.loadDepartments(true);
  },

  syncTabBar() {
    if (typeof this.getTabBar === 'function') {
      const bar = this.getTabBar();
      if (bar) {
        bar.setData({ selected: 0 });
      }
    }
  },

  async loadDepartments(refresh) {
    try {
      const list = await api.departments();
      const departments = (list || []).slice(0, 8).map(function (item, index) {
        return {
          id: item.id,
          name: item.name,
          doctorCount: item.doctorCount || 0,
          no: ('0' + (index + 1)).slice(-2)
        };
      });
      this.setData({ departments: departments, total: (list || []).length });
    } catch (err) {
      // 错误提示已在请求层统一处理
    } finally {
      this.setData({ loading: false });
      if (refresh) {
        wx.stopPullDownRefresh();
      }
    }
  },

  goSearch() {
    wx.navigateTo({ url: '/pages/doctor/list' });
  },

  goDepartments() {
    wx.navigateTo({ url: '/pages/department/department' });
  },

  goDepartment(e) {
    const dataset = e.currentTarget.dataset;
    wx.navigateTo({
      url: '/pages/doctor/list?departmentId=' + dataset.id + '&departmentName=' + encodeURIComponent(dataset.name)
    });
  },

  goTriage() {
    wx.switchTab({ url: '/pages/guidance/guidance' });
  },

  goOrders() {
    if (!auth.requireLogin()) {
      return;
    }
    wx.switchTab({ url: '/pages/orders/orders' });
  }
});
