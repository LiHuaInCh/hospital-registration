const auth = require('../../utils/auth');
const format = require('../../utils/format');

Page({
  data: {
    user: null,
    initial: '患'
  },

  onShow() {
    if (typeof this.getTabBar === 'function') {
      const bar = this.getTabBar();
      if (bar) {
        bar.setData({ selected: 3 });
      }
    }
    const user = auth.currentUser();
    this.setData({
      user: user,
      initial: format.initial(user && user.nickname)
    });
  },

  goLogin() {
    wx.navigateTo({ url: '/pages/login/login' });
  },

  goPatients() {
    if (!auth.requireLogin()) {
      return;
    }
    wx.navigateTo({ url: '/pages/patient/list/list' });
  },

  goOrders() {
    if (!auth.requireLogin()) {
      return;
    }
    wx.switchTab({ url: '/pages/orders/orders' });
  },

  callHospital() {
    wx.makePhoneCall({ phoneNumber: '057188000010' });
  },

  goAdmin() {
    const url = auth.adminToken()
      ? '/pages/admin/department/department'
      : '/pages/admin/login/login';
    wx.navigateTo({ url: url });
  },

  logout() {
    const that = this;
    wx.showModal({
      title: '退出登录',
      content: '退出后将无法查看挂号记录，确定继续吗？',
      success: function (res) {
        if (!res.confirm) {
          return;
        }
        auth.clear();
        that.setData({ user: null, initial: '患' });
        wx.showToast({ title: '已退出', icon: 'none' });
      }
    });
  }
});
