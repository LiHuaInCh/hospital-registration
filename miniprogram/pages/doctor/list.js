const api = require('../../utils/api');
const format = require('../../utils/format');

function decorate(item) {
  return {
    id: item.id,
    name: item.name,
    title: item.title,
    departmentName: item.departmentName,
    specialty: item.specialty,
    consultationFee: item.consultationFee,
    fee: format.money(item.consultationFee),
    initial: format.initial(item.name)
  };
}

Page({
  data: {
    departmentId: null,
    departmentName: '',
    keyword: '',
    doctors: [],
    loading: true
  },

  onLoad(options) {
    let departmentName = options.departmentName || '';
    try {
      departmentName = decodeURIComponent(departmentName);
    } catch (err) {
      // 微信通常已解码，重复解码失败时按原样使用
    }
    this.setData({
      departmentId: options.departmentId || null,
      departmentName: departmentName
    });
    if (departmentName) {
      wx.setNavigationBarTitle({ title: departmentName });
    }
    this.loadDoctors();
  },

  async loadDoctors() {
    this.setData({ loading: true });
    try {
      const keyword = this.data.keyword.trim();
      const list = keyword
        ? await api.searchDoctors(keyword)
        : await api.doctors(this.data.departmentId);
      this.setData({ doctors: (list || []).map(decorate) });
    } catch (err) {
      this.setData({ doctors: [] });
    } finally {
      this.setData({ loading: false });
    }
  },

  onKeyword(e) {
    this.setData({ keyword: e.detail.value });
  },

  onSearch() {
    this.loadDoctors();
  },

  clearKeyword() {
    this.setData({ keyword: '' });
    this.loadDoctors();
  },

  goDetail(e) {
    wx.navigateTo({ url: '/pages/doctor/detail?id=' + e.currentTarget.dataset.id });
  }
});
