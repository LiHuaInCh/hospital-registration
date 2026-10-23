const api = require('../../../utils/api');
const auth = require('../../../utils/auth');
const format = require('../../../utils/format');

const TABS = [
  { label: '全部', status: '' },
  { label: '待就诊', status: '1,2' },
  { label: '已完成', status: '3' },
  { label: '已取消', status: '4' }
];

const PAGE_SIZE = 10;

const ACTIONS = {
  checkin: { status: 2, label: '已签到' },
  finish: { status: 3, label: '已完成' },
  cancel: { status: 4, label: '已取消' }
};

function decorate(item) {
  return {
    id: item.id,
    patientName: item.patientName || '未知就诊人',
    departmentName: item.departmentName || '门诊',
    doctorName: item.doctorName || '',
    title: item.title || '',
    status: item.status,
    statusText: format.statusText(item.status),
    dateText: format.dateText(item.workDate),
    timeText: item.timeSlot,
    fee: format.money(item.fee),
    canCheckIn: item.status === 1,
    canFinish: item.status === 2,
    canCancel: item.status === 1 || item.status === 2
  };
}

Page({
  data: {
    tabs: TABS,
    currentTab: 0,
    date: '',
    orders: [],
    total: 0,
    loading: true,
    loadingMore: false,
    hasMore: false,
    page: 1
  },

  onLoad() {
    auth.requireAdmin();
  },

  onShow() {
    if (auth.adminToken()) {
      this.reload();
    }
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

  onDateChange(e) {
    this.setData({ date: e.detail.value });
    this.reload();
  },

  clearDate() {
    this.setData({ date: '' });
    this.reload();
  },

  async reload(refresh) {
    this.setData({ loading: true });
    try {
      const data = await api.adminRegistrations({
        status: TABS[this.data.currentTab].status,
        date: this.data.date,
        page: 1,
        size: PAGE_SIZE
      });
      this.setData({
        orders: (data.records || []).map(decorate),
        total: data.total || 0,
        hasMore: !!data.hasMore,
        page: 1
      });
    } catch (err) {
      this.setData({ orders: [], total: 0, hasMore: false });
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
      const data = await api.adminRegistrations({
        status: TABS[this.data.currentTab].status,
        date: this.data.date,
        page: next,
        size: PAGE_SIZE
      });
      this.setData({
        orders: this.data.orders.concat((data.records || []).map(decorate)),
        total: data.total || 0,
        hasMore: !!data.hasMore,
        page: next
      });
    } catch (err) {
      // 请求层已提示
    } finally {
      this.setData({ loadingMore: false });
    }
  },

  act(e) {
    const dataset = e.currentTarget.dataset;
    const action = ACTIONS[dataset.act];
    if (!action) {
      return;
    }
    const that = this;
    wx.showModal({
      title: '更新挂号状态',
      content: '将挂号单标记为「' + action.label + '」？',
      success: async function (res) {
        if (!res.confirm) {
          return;
        }
        try {
          await api.adminChangeStatus(dataset.id, action.status);
          wx.showToast({ title: action.label, icon: 'none' });
          that.reload();
        } catch (err) {
          // 请求层已提示
        }
      }
    });
  }
});
