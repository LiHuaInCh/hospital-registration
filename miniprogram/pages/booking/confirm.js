const api = require('../../utils/api');
const auth = require('../../utils/auth');
const format = require('../../utils/format');

Page({
  data: {
    doctor: null,
    schedule: null,
    workDate: '',
    dateText: '',
    timeText: '',
    fee: '0',
    patients: [],
    selectedPatient: null,
    showPicker: false,
    submitting: false
  },

  onLoad() {
    const draft = getApp().globalData.draft;
    if (!draft || !draft.schedule || !draft.doctor) {
      wx.navigateBack();
      return;
    }
    this.setData({
      doctor: draft.doctor,
      schedule: draft.schedule,
      workDate: draft.workDate,
      dateText: format.dateText(draft.workDate),
      timeText: draft.schedule.timeSlot + (draft.schedule.range ? '  ' + draft.schedule.range : ''),
      fee: format.money(draft.doctor.consultationFee)
    });
  },

  onShow() {
    if (this.data.doctor) {
      this.loadPatients();
    }
  },

  async loadPatients() {
    if (!auth.isLoggedIn()) {
      return;
    }
    try {
      const list = await api.patients();
      const patients = (list || []).map(function (item) {
        return {
          id: item.id,
          name: item.name,
          relationship: item.relationship || '本人',
          genderText: format.genderText(item.gender),
          idCardMasked: format.maskIdCard(item.idCard),
          isDefault: item.isDefault
        };
      });
      let selected = null;
      const current = this.data.selectedPatient;
      if (current) {
        selected = patients.filter(function (item) {
          return item.id === current.id;
        })[0] || null;
      }
      if (!selected) {
        selected = patients.filter(function (item) {
          return item.isDefault === 1;
        })[0] || patients[0] || null;
      }
      this.setData({ patients: patients, selectedPatient: selected });
    } catch (err) {
      // 请求层已提示
    }
  },

  openPicker() {
    if (!this.data.patients.length) {
      this.addPatient();
      return;
    }
    this.setData({ showPicker: true });
  },

  closePicker() {
    this.setData({ showPicker: false });
  },

  choosePatient(e) {
    const id = Number(e.currentTarget.dataset.id);
    const patient = this.data.patients.filter(function (item) {
      return item.id === id;
    })[0];
    this.setData({ selectedPatient: patient || null, showPicker: false });
  },

  addPatient() {
    this.setData({ showPicker: false });
    wx.navigateTo({ url: '/pages/patient/edit/edit' });
  },

  async submit() {
    if (!this.data.selectedPatient) {
      wx.showToast({ title: '请选择就诊人', icon: 'none' });
      return;
    }
    if (this.data.submitting) {
      return;
    }
    this.setData({ submitting: true });
    try {
      const order = await api.createRegistration({
        patientId: this.data.selectedPatient.id,
        scheduleId: this.data.schedule.id
      });
      const app = getApp();
      app.globalData.lastOrder = order;
      app.globalData.draft = null;
      wx.redirectTo({ url: '/pages/booking/success' });
    } catch (err) {
      this.setData({ submitting: false });
    }
  }
});
