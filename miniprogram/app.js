const auth = require('./utils/auth');
const api = require('./utils/api');

App({
  globalData: {
    // 通过 ngrok 内网穿透把本机 8080 暴露到公网，真机、体验版、其他电脑都能访问；
    // 只在本机模拟器调试时可以改成 http://127.0.0.1:8080/api 或内网地址 http://10.178.32.109:8080/api
    baseUrl: wx.getStorageSync('apiBaseUrl') || 'https://campsite-recount-floss.ngrok-free.dev/api',
    // 排班页 -> 确认页之间传递的预约草稿，避免把中文塞进 URL 参数
    draft: null,
    // 最近一次挂号结果，用于成功页展示
    lastOrder: null,
    // 从首页点「智能导诊」时预填的症状
    presetSymptom: ''
  },

  onLaunch() {
    auth.reload();
  },

  onShow() {
    auth.reload();
  }
});
