const ROUTES = {
  department: '/pages/admin/department/department',
  doctor: '/pages/admin/doctor/doctor',
  schedule: '/pages/admin/schedule/schedule',
  orders: '/pages/admin/orders/orders'
};

Component({
  properties: {
    active: { type: String, value: 'department' }
  },

  data: {
    items: [
      { key: 'department', label: '科室' },
      { key: 'doctor', label: '医生' },
      { key: 'schedule', label: '排班' },
      { key: 'orders', label: '挂号单' }
    ]
  },

  methods: {
    go(e) {
      const key = e.currentTarget.dataset.key;
      if (key === this.data.active || !ROUTES[key]) {
        return;
      }
      wx.redirectTo({ url: ROUTES[key] });
    }
  }
});
