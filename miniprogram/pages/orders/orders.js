const api = require('../../utils/api');
const auth = require('../../utils/auth');
const format = require('../../utils/format');

const TABS = [
  { label: '全部', status: '' },
  { label: '待就诊', status: '1,2' },
  { label: '已完成', status: '3' },
  { label: '已取消', status: '4' }
];

const PAGE_SIZE = 10;

function decorate(item) {
  return {
    id: item.id,
    departmentName: item.departmentName || '门诊',
    doctorName: item.doctorName || '',
    title: item.title || '',
    patientName: item.patientName || '',
    status: item.status,
    statusText: format.statusText(item.status),
    dateText: format.dateText(item.workDate),
    timeText: item.timeSlot,
    fee: format.money(item.fee),
    canCancel: item.status === 1
  };
}

Page({
  data: {
    tabs: TABS,
    currentTab: 0,
    orders: [],
    loading: true,
    loadingMore: false,
    hasMore: false,
    page: 1,
    loggedIn: false
  },

  onShow() {
    if (typeof this.getTabBar === 'function') {
      const bar = this.getTabBar();
      if (bar) {
        bar.setData({ selected: 2 });
      }
    }
    this.setData({ loggedIn: auth.isLoggedIn() });
    this.reload();
  },

  onPullDownRefresh() {
    this.reload(true);
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.loadingMore) {
      this.loadMore();
    }
  },

  switchTab(e) {
    const index = Number(e.currentTarget.dataset.index);
    if (index === this.data.currentTab) {
      return;
    }
    this.setData({ currentTab: index });
    this.reload();
  },

  async reload(refresh) {
    if (!auth.isLoggedIn()) {
      this.setData({ orders: [], loading: false, hasMore: false });
      if (refresh) {
        wx.stopPullDownRefresh();
      }
      return;
    }
    this.setData({ loading: true });
    try {
      const data = await api.registrations({
        status: TABS[this.data.currentTab].status,
        page: 1,
        size: PAGE_SIZE
      });
      this.setData({
        orders: (data.records || []).map(decorate),
        hasMore: !!data.hasMore,
        page: 1
      });
    } catch (err) {
      this.setData({ orders: [], hasMore: false });
    } finally {
      this.setData({ loading: false });
      if (refresh) {
        wx.stopPullDownRefresh();
      }
    }
  },

  async loadMore() {
    this.setData({ loadingMore: true });
    try {
      const next = this.data.page + 1;
      const data = await api.registrations({
        status: TABS[this.data.currentTab].status,
        page: next,
        size: PAGE_SIZE
      });
      this.setData({
        orders: this.data.orders.concat((data.records || []).map(decorate)),
        hasMore: !!data.hasMore,
        page: next
      });
    } catch (err) {
      // 请求层已提示
    } finally {
      this.setData({ loadingMore: false });
    }
  },

  cancel(e) {
    const id = e.currentTarget.dataset.id;
    const that = this;
    wx.showModal({
      title: '取消预约',
      content: '确定取消这次挂号吗？号源将释放给其他患者。',
      confirmText: '取消挂号',
      confirmColor: '#9C342A',
      success: async function (res) {
        if (!res.confirm) {
          return;
        }
        try {
          await api.cancelRegistration(id, '用户主动取消');
          wx.showToast({ title: '已取消', icon: 'none' });
          that.reload();
        } catch (err) {
          // 请求层已提示
        }
      }
    });
  },

  goLogin() {
    wx.navigateTo({ url: '/pages/login/login' });
  }
});
