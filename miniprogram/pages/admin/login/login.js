const api = require('../../../utils/api');
const auth = require('../../../utils/auth');

Page({
  data: {
    username: 'admin',
    password: '',
    loading: false
  },

  onLoad() {
    if (auth.adminToken()) {
      wx.redirectTo({ url: '/pages/admin/department/department' });
    }
  },

  onUsername(e) {
    this.setData({ username: e.detail.value });
  },

  onPassword(e) {
    this.setData({ password: e.detail.value });
  },

  async submit() {
    if (this.data.loading) {
      return;
    }
    const username = this.data.username.trim();
    const password = this.data.password;
    if (!username || !password) {
      wx.showToast({ title: '请输入账号和密码', icon: 'none' });
      return;
    }
    this.setData({ loading: true });
    try {
      const login = await api.adminLogin({ username: username, password: password });
      auth.saveAdmin(login);
      wx.redirectTo({ url: '/pages/admin/department/department' });
    } catch (err) {
      this.setData({ loading: false });
    }
  }
});
