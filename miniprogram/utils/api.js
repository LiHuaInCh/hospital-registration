const auth = require('./auth');

function toast(message) {
  wx.showToast({ title: message, icon: 'none', duration: 2200 });
}

function compact(params) {
  const result = {};
  Object.keys(params || {}).forEach(function (key) {
    const value = params[key];
    if (value !== undefined && value !== null && value !== '') {
      result[key] = value;
    }
  });
  return result;
}

function currentRoute() {
  const pages = getCurrentPages();
  if (!pages.length) {
    return '';
  }
  return pages[pages.length - 1].route || '';
}

function handleUnauthorized(admin) {
  if (admin) {
    auth.clearAdmin();
  } else {
    auth.clear();
  }
  const target = admin ? 'pages/admin/login/login' : 'pages/login/login';
  if (currentRoute() !== target) {
    wx.navigateTo({ url: '/' + target });
  }
}

function send(method, url, data, options) {
  options = options || {};
  const app = getApp();
  const admin = !!options.admin;
  const token = admin ? auth.adminToken() : auth.userToken();

  return new Promise(function (resolve, reject) {
    const header = {
      'Content-Type': 'application/json',
      // ngrok 免费版会给疑似浏览器的请求返回拦截页，加这个头直接放行
      'ngrok-skip-browser-warning': 'true'
    };
    if (token) {
      header.Authorization = 'Bearer ' + token;
    }

    wx.request({
      url: app.globalData.baseUrl + url,
      method: method,
      data: data || {},
      timeout: 15000,
      header: header,
      success: function (res) {
        const body = res.data || {};
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(body.data === undefined ? null : body.data);
          return;
        }
        const message = body.message || '请求失败（' + res.statusCode + '）';
        if (res.statusCode === 401) {
          handleUnauthorized(admin);
        }
        if (!options.silent) {
          toast(message);
        }
        reject(new Error(message));
      },
      fail: function () {
        const message = '网络异常，请检查后端服务是否已启动';
        if (!options.silent) {
          toast(message);
        }
        reject(new Error(message));
      }
    });
  });
}

function get(url, params, options) {
  return send('GET', url, compact(params), options);
}

function post(url, body, options) {
  return send('POST', url, body, options);
}

function put(url, body, options) {
  return send('PUT', url, body, options);
}

/**
 * DELETE 的参数必须放在 query 上：wx.request 只在 GET 时把 data 拼到 URL，
 * 其他方法会放进请求体，后端的 @RequestParam 取不到。
 */
function remove(url, params, options) {
  const pairs = [];
  const values = compact(params);
  Object.keys(values).forEach(function (key) {
    pairs.push(encodeURIComponent(key) + '=' + encodeURIComponent(values[key]));
  });
  const target = pairs.length ? url + '?' + pairs.join('&') : url;
  return send('DELETE', target, null, options);
}

module.exports = {
  // ---- 登录 ----
  login: function (payload) {
    return post('/user/login', payload);
  },
  me: function () {
    return get('/user/me', null, { silent: true });
  },
  adminLogin: function (payload) {
    return post('/admin/login', payload);
  },

  // ---- 科室 ----
  departments: function () {
    return get('/department/list');
  },
  addDepartment: function (payload) {
    return post('/department/add', payload, { admin: true });
  },
  updateDepartment: function (payload) {
    return put('/department/update', payload, { admin: true });
  },
  deleteDepartment: function (id) {
    return remove('/department/delete', { id: id }, { admin: true });
  },

  // ---- 医生 ----
  doctors: function (departmentId) {
    return get('/doctor/list', { departmentId: departmentId });
  },
  searchDoctors: function (keyword) {
    return get('/doctor/search', { keyword: keyword });
  },
  doctorDetail: function (id) {
    return get('/doctor/detail', { id: id });
  },
  addDoctor: function (payload) {
    return post('/doctor/add', payload, { admin: true });
  },
  updateDoctor: function (payload) {
    return put('/doctor/update', payload, { admin: true });
  },
  deleteDoctor: function (id) {
    return remove('/doctor/delete', { id: id }, { admin: true });
  },

  // ---- 排班 ----
  dates: function () {
    return get('/schedule/dates');
  },
  schedules: function (doctorId) {
    return get('/schedule/list', { doctorId: doctorId });
  },
  addSchedule: function (payload) {
    return post('/schedule/add', payload, { admin: true });
  },
  updateSchedule: function (payload) {
    return put('/schedule/update', payload, { admin: true });
  },
  deleteSchedule: function (id) {
    return remove('/schedule/delete', { id: id }, { admin: true });
  },

  // ---- 挂号 ----
  createRegistration: function (payload) {
    return post('/registration/create', payload);
  },
  registrations: function (params) {
    return get('/registration/list', params);
  },
  registrationDetail: function (id) {
    return get('/registration/detail', { id: id });
  },
  cancelRegistration: function (id, reason) {
    return post('/registration/cancel', { id: id, reason: reason || '用户取消' });
  },

  // ---- 就诊人 ----
  patients: function () {
    return get('/patient/list');
  },
  patientDetail: function (id) {
    return get('/patient/detail', { id: id });
  },
  addPatient: function (payload) {
    return post('/patient/add', payload);
  },
  updatePatient: function (payload) {
    return put('/patient/update', payload);
  },
  deletePatient: function (id) {
    return remove('/patient/delete', { id: id });
  },

  // ---- 导诊 ----
  triage: function (symptoms) {
    return post('/guidance/triage', { symptoms: symptoms });
  },

  // ---- 管理端 ----
  adminRegistrations: function (params) {
    return get('/admin/registration/list', params, { admin: true });
  },
  adminChangeStatus: function (id, status) {
    return put('/admin/registration/status', { id: id, status: status }, { admin: true });
  },
  adminSchedules: function (params) {
    return get('/admin/schedule/list', params, { admin: true });
  }
};
