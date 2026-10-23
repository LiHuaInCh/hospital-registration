const KEY_USER = 'user';
const KEY_TOKEN = 'token';
const KEY_ADMIN_TOKEN = 'adminToken';
const KEY_ADMIN_NAME = 'adminName';

let user = null;
let token = null;

function reload() {
  user = wx.getStorageSync(KEY_USER) || null;
  token = wx.getStorageSync(KEY_TOKEN) || '';
  return user;
}

function currentUser() {
  if (user === null) {
    reload();
  }
  return user;
}

function userToken() {
  if (!token) {
    token = wx.getStorageSync(KEY_TOKEN) || '';
  }
  return token;
}

function isLoggedIn() {
  return !!userToken();
}

function save(login) {
  token = login.token;
  user = {
    userId: login.userId,
    nickname: login.nickname,
    avatarUrl: login.avatarUrl
  };
  wx.setStorageSync(KEY_TOKEN, token);
  wx.setStorageSync(KEY_USER, user);
  return user;
}

function clear() {
  user = null;
  token = '';
  wx.removeStorageSync(KEY_TOKEN);
  wx.removeStorageSync(KEY_USER);
}

function requireLogin() {
  if (isLoggedIn()) {
    return true;
  }
  wx.navigateTo({ url: '/pages/login/login' });
  return false;
}

function requireAdmin() {
  if (adminToken()) {
    return true;
  }
  wx.redirectTo({ url: '/pages/admin/login/login' });
  return false;
}

function adminToken() {
  return wx.getStorageSync(KEY_ADMIN_TOKEN) || '';
}

function adminName() {
  return wx.getStorageSync(KEY_ADMIN_NAME) || '';
}

function saveAdmin(login) {
  wx.setStorageSync(KEY_ADMIN_TOKEN, login.token);
  wx.setStorageSync(KEY_ADMIN_NAME, login.nickname || '管理员');
}

function clearAdmin() {
  wx.removeStorageSync(KEY_ADMIN_TOKEN);
  wx.removeStorageSync(KEY_ADMIN_NAME);
}

module.exports = {
  reload,
  currentUser,
  userToken,
  isLoggedIn,
  save,
  clear,
  requireLogin,
  requireAdmin,
  adminToken,
  adminName,
  saveAdmin,
  clearAdmin
};
