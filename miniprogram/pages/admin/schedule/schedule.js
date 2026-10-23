const api = require('../../../utils/api');
const auth = require('../../../utils/auth');
const format = require('../../../utils/format');

const SLOTS = ['上午', '下午', '晚上'];

Page({
  data: {
    dates: [],
    selectedDate: '',
    schedules: [],
    doctors: [],
    loading: true,
    showDialog: false,
    saving: false,
    slots: SLOTS,
    slotIndex: 0,
    doctorIndex: 0,
    today: '',
    form: {
      doctorId: null,
      workDate: '',
      timeSlot: SLOTS[0],
      totalCount: 30
    }
  },

  onLoad() {
    if (!auth.requireAdmin()) {
      return;
    }
    this.init();
  },

  async init() {
    try {
      const results = await Promise.all([api.dates(), api.doctors()]);
      const dates = (results[0] || []).map(function (item) {
        return {
          date: item.date,
          label: (item.today ? '今天 ' : '') + format.shortDate(item.date),
          weekday: item.today ? '今天' : item.weekday
        };
      });
      this.setData({
        dates: dates,
        doctors: results[1] || [],
        selectedDate: dates.length ? dates[0].date : '',
        today: dates.length ? dates[0].date : ''
      });
      await this.loadSchedules();
    } catch (err) {
      // 请求层已提示
    } finally {
      this.setData({ loading: false });
    }
  },

  async loadSchedules() {
    if (!this.data.selectedDate) {
      return;
    }
    try {
      const list = await api.adminSchedules({ date: this.data.selectedDate });
      const schedules = (list || []).map(function (item) {
        return {
          id: item.id,
          doctorName: item.doctorName,
          departmentName: item.departmentName,
          timeSlot: item.timeSlot,
          range: format.timeRange(item.startTime, item.endTime),
          remainCount: item.remainCount,
          totalCount: item.totalCount,
          status: item.status,
          statusText: item.status === 2 ? '停诊' : '正常'
        };
      });
      this.setData({ schedules: schedules });
    } catch (err) {
      this.setData({ schedules: [] });
    }
  },

  selectDate(e) {
    const date = e.currentTarget.dataset.date;
    if (date === this.data.selectedDate) {
      return;
    }
    this.setData({ selectedDate: date });
    this.loadSchedules();
  },

  showAdd() {
    const doctor = this.data.doctors[0];
    const slotIndex = 0;
    this.setData({
      showDialog: true,
      slotIndex: slotIndex,
      doctorIndex: 0,
      form: {
        doctorId: doctor ? doctor.id : null,
        workDate: this.data.selectedDate,
        timeSlot: SLOTS[slotIndex],
        totalCount: 30
      }
    });
  },

  close() {
    if (this.data.saving) {
      return;
    }
    this.setData({ showDialog: false });
  },

  onDoctorChange(e) {
    const index = Number(e.detail.value);
    this.setData({
      doctorIndex: index,
      'form.doctorId': this.data.doctors[index].id
    });
  },

  onSlotChange(e) {
    const index = Number(e.detail.value);
    this.setData({ slotIndex: index, 'form.timeSlot': SLOTS[index] });
  },

  onDateChange(e) {
    this.setData({ 'form.workDate': e.detail.value });
  },

  onField(e) {
    const patch = {};
    patch['form.' + e.currentTarget.dataset.field] = e.detail.value;
    this.setData(patch);
  },

  async save() {
    const form = this.data.form;
    if (!form.doctorId) {
      wx.showToast({ title: '请选择医生', icon: 'none' });
      return;
    }
    if (!form.workDate) {
      wx.showToast({ title: '请选择出诊日期', icon: 'none' });
      return;
    }
    const total = Number(form.totalCount);
    if (isNaN(total) || total < 1) {
      wx.showToast({ title: '请填写号源数量', icon: 'none' });
      return;
    }
    if (this.data.saving) {
      return;
    }
    this.setData({ saving: true });
    try {
      await api.addSchedule({
        doctorId: form.doctorId,
        workDate: form.workDate,
        timeSlot: form.timeSlot,
        totalCount: total
      });
      this.setData({ showDialog: false, saving: false });
      wx.showToast({ title: '已排班', icon: 'none' });
      this.setData({ selectedDate: form.workDate });
      this.loadSchedules();
    } catch (err) {
      this.setData({ saving: false });
    }
  },

  remove(e) {
    const id = e.currentTarget.dataset.id;
    const that = this;
    wx.showModal({
      title: '删除排班',
      content: '已有未完成挂号的排班无法删除，确定继续吗？',
      confirmColor: '#9C342A',
      success: async function (res) {
        if (!res.confirm) {
          return;
        }
        try {
          await api.deleteSchedule(id);
          wx.showToast({ title: '已删除', icon: 'none' });
          that.loadSchedules();
        } catch (err) {
          // 请求层已提示
        }
      }
    });
  }
});
