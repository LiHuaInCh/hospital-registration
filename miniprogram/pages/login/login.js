const api = require('../../utils/api');
const auth = require('../../utils/auth');

const DEVICE_KEY = 'deviceCode';

function deviceCode() {
  let code = wx.getStorageSync(DEVICE_KEY);
  if (!code) {
    code = 'dev_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
    wx.setStorageSync(DEVICE_KEY, code);
  }
  return code;
}

Page({
  data: {
    loading: false
  },

  onLoad() {
    if (auth.isLoggedIn()) {
      this.back();
    }
  },

  async handleLogin() {
    if (this.data.loading) {
      return;
    }
    this.setData({ loading: true });
    try {
      const login = await api.login({
        code: deviceCode(),
        nickname: '微信用户'
      });
      auth.save(login);
      wx.showToast({ title: '登录成功', icon: 'none' });
      setTimeout(this.back.bind(this), 400);
    } catch (err) {
      this.setData({ loading: false });
    }
  },

  back() {
    const pages = getCurrentPages();
    if (pages.length > 1) {
      wx.navigateBack();
    } else {
      wx.switchTab({ url: '/pages/index/index' });
    }
  }
});
