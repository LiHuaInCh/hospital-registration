const api = require('../../utils/api');

Page({
  data: {
    departments: [],
    loading: true
  },

  onLoad() {
    this.loadDepartments();
  },

  async loadDepartments() {
    try {
      const list = await api.departments();
      const departments = (list || []).map(function (item, index) {
        return {
          id: item.id,
          name: item.name,
          description: item.description,
          location: item.location,
          doctorCount: item.doctorCount || 0,
          no: ('0' + (index + 1)).slice(-2)
        };
      });
      this.setData({ departments: departments });
    } catch (err) {
      // 请求层已提示
    } finally {
      this.setData({ loading: false });
    }
  },

  goDoctors(e) {
    const dataset = e.currentTarget.dataset;
    wx.navigateTo({
      url: '/pages/doctor/list?departmentId=' + dataset.id + '&departmentName=' + encodeURIComponent(dataset.name)
    });
  }
});
