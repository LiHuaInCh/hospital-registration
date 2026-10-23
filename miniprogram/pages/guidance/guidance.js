const api = require('../../utils/api');

Page({
  data: {
    symptoms: '',
    results: [],
    emergency: false,
    advice: '',
    searched: false,
    searching: false,
    commonSymptoms: [
      '咳嗽三天，伴低烧',
      '胃痛、反酸',
      '腰痛、腿麻',
      '皮肤瘙痒起红疹',
      '牙痛、牙龈出血',
      '胸闷、心慌'
    ]
  },

  onShow() {
    if (typeof this.getTabBar === 'function') {
      const bar = this.getTabBar();
      if (bar) {
        bar.setData({ selected: 1 });
      }
    }
    const app = getApp();
    if (app.globalData.presetSymptom) {
      this.setData({ symptoms: app.globalData.presetSymptom });
      app.globalData.presetSymptom = '';
    }
  },

  onInput(e) {
    this.setData({ symptoms: e.detail.value });
  },

  useSymptom(e) {
    this.setData({ symptoms: e.currentTarget.dataset.text });
  },

  async doTriage() {
    const symptoms = this.data.symptoms.trim();
    if (!symptoms) {
      wx.showToast({ title: '请先描述症状', icon: 'none' });
      return;
    }
    if (this.data.searching) {
      return;
    }
    this.setData({ searching: true });
    try {
      const data = await api.triage(symptoms);
      this.setData({
        results: data.results || [],
        emergency: !!data.emergency,
        advice: data.advice || '',
        searched: true
      });
    } catch (err) {
      this.setData({
        results: [],
        emergency: false,
        advice: '',
        searched: true
      });
    } finally {
      this.setData({ searching: false });
    }
  },

  goDoctors(e) {
    const dataset = e.currentTarget.dataset;
    wx.navigateTo({
      url: '/pages/doctor/list?departmentId=' + dataset.id + '&departmentName=' + encodeURIComponent(dataset.name)
    });
  }
});
