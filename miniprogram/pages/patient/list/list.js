const api = require('../../../utils/api');
const auth = require('../../../utils/auth');
const format = require('../../../utils/format');

Page({
  data: {
    patients: [],
    loading: true
  },

  onShow() {
    if (!auth.isLoggedIn()) {
      wx.redirectTo({ url: '/pages/login/login' });
      return;
    }
    this.loadPatients();
  },

  async loadPatients() {
    try {
      const list = await api.patients();
      this.setData({
        patients: (list || []).map(function (item) {
          return {
            id: item.id,
            name: item.name,
            relationship: item.relationship || '本人',
            genderText: format.genderText(item.gender),
            idCardMasked: format.maskIdCard(item.idCard),
            phone: item.phone,
            isDefault: item.isDefault
          };
        })
      });
    } catch (err) {
      // 请求层已提示
    } finally {
      this.setData({ loading: false });
    }
  },

  add() {
    wx.navigateTo({ url: '/pages/patient/edit/edit' });
  },

  goEdit(e) {
    wx.navigateTo({ url: '/pages/patient/edit/edit?id=' + e.currentTarget.dataset.id });
  },

  remove(e) {
    const id = e.currentTarget.dataset.id;
    const that = this;
    wx.showModal({
      title: '删除就诊人',
      content: '删除后历史挂号记录仍会保留，确定删除吗？',
      confirmColor: '#9C342A',
      success: async function (res) {
        if (!res.confirm) {
          return;
        }
        try {
          await api.deletePatient(id);
          wx.showToast({ title: '已删除', icon: 'none' });
          that.loadPatients();
        } catch (err) {
          // 请求层已提示
        }
      }
    });
  }
});
