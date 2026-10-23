const api = require('../../utils/api');
const format = require('../../utils/format');

Page({
  data: {
    doctor: null,
    initial: '',
    fee: '0',
    loading: true
  },

  async onLoad(options) {
    if (!options.id) {
      wx.navigateBack();
      return;
    }
    try {
      const doctor = await api.doctorDetail(options.id);
      this.setData({
        doctor: doctor,
        initial: format.initial(doctor.name),
        fee: format.money(doctor.consultationFee)
      });
    } catch (err) {
      // 请求层已提示
    } finally {
      this.setData({ loading: false });
    }
  },

  goSchedule() {
    wx.navigateTo({ url: '/pages/schedule/schedule?doctorId=' + this.data.doctor.id });
  }
});
