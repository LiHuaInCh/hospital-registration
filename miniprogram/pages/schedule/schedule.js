const api = require('../../utils/api');
const auth = require('../../utils/auth');
const format = require('../../utils/format');

Page({
  data: {
    doctorId: null,
    doctor: null,
    initial: '',
    fee: '0',
    dates: [],
    selectedDate: '',
    slots: [],
    loading: true
  },

  async onLoad(options) {
    if (!options.doctorId) {
      wx.navigateBack();
      return;
    }
    this.setData({ doctorId: options.doctorId });
    try {
      const results = await Promise.all([api.doctorDetail(options.doctorId), api.dates()]);
      const doctor = results[0];
      const dates = (results[1] || []).map(function (item) {
        return {
          date: item.date,
          weekday: item.today ? '今天' : item.weekday,
          day: format.dayNumber(item.date),
          today: !!item.today
        };
      });
      this.setData({
        doctor: doctor,
        initial: format.initial(doctor.name),
        fee: format.money(doctor.consultationFee),
        dates: dates,
        selectedDate: dates.length ? dates[0].date : ''
      });
      await this.loadSlots();
    } catch (err) {
      // 请求层已提示
    } finally {
      this.setData({ loading: false });
    }
  },

  async loadSlots() {
    const date = this.data.selectedDate;
    if (!date) {
      this.setData({ slots: [] });
      return;
    }
    this.setData({ loading: true });
    try {
      const list = await api.schedules(this.data.doctorId);
      const slots = (list || [])
        .filter(function (item) {
          return item.workDate === date;
        })
        .map(function (item) {
          return {
            id: item.id,
            timeSlot: item.timeSlot,
            range: format.timeRange(item.startTime, item.endTime),
            remainCount: item.remainCount,
            full: item.remainCount <= 0
          };
        });
      this.setData({ slots: slots });
    } catch (err) {
      this.setData({ slots: [] });
    } finally {
      this.setData({ loading: false });
    }
  },

  selectDate(e) {
    const date = e.currentTarget.dataset.date;
    if (date === this.data.selectedDate) {
      return;
    }
    this.setData({ selectedDate: date });
    this.loadSlots();
  },

  goConfirm(e) {
    const id = Number(e.currentTarget.dataset.id);
    const slot = this.data.slots.filter(function (item) {
      return item.id === id;
    })[0];
    if (!slot || slot.full) {
      return;
    }
    if (!auth.requireLogin()) {
      return;
    }
    const app = getApp();
    app.globalData.draft = {
      doctor: this.data.doctor,
      schedule: slot,
      workDate: this.data.selectedDate
    };
    wx.navigateTo({ url: '/pages/booking/confirm' });
  }
});
