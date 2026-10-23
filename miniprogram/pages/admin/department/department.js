const api = require('../../../utils/api');
const auth = require('../../../utils/auth');

const EMPTY = {
  name: '',
  description: '',
  location: '',
  phone: ''
};

Page({
  data: {
    departments: [],
    loading: true,
    showDialog: false,
    isEdit: false,
    saving: false,
    form: EMPTY
  },

  onLoad() {
    if (!auth.requireAdmin()) {
      return;
    }
    this.load();
  },

  async load() {
    try {
      const list = await api.departments();
      this.setData({ departments: list || [] });
    } catch (err) {
      // 请求层已提示
    } finally {
      this.setData({ loading: false });
    }
  },

  showAdd() {
    this.setData({
      showDialog: true,
      isEdit: false,
      form: Object.assign({}, EMPTY)
    });
  },

  showEdit(e) {
    const id = Number(e.currentTarget.dataset.id);
    const item = this.data.departments.filter(function (row) {
      return row.id === id;
    })[0];
    if (!item) {
      return;
    }
    this.setData({
      showDialog: true,
      isEdit: true,
      form: {
        id: item.id,
        name: item.name,
        description: item.description || '',
        location: item.location || '',
        phone: item.phone || ''
      }
    });
  },

  close() {
    if (this.data.saving) {
      return;
    }
    this.setData({ showDialog: false });
  },

  onField(e) {
    const patch = {};
    patch['form.' + e.currentTarget.dataset.field] = e.detail.value;
    this.setData(patch);
  },

  async save() {
    const form = this.data.form;
    if (!form.name || !form.name.trim()) {
      wx.showToast({ title: '请填写科室名称', icon: 'none' });
      return;
    }
    if (this.data.saving) {
      return;
    }
    this.setData({ saving: true });
    try {
      const payload = {
        name: form.name.trim(),
        description: form.description,
        location: form.location,
        phone: form.phone
      };
      if (this.data.isEdit) {
        payload.id = form.id;
        await api.updateDepartment(payload);
      } else {
        await api.addDepartment(payload);
      }
      this.setData({ showDialog: false, saving: false });
      wx.showToast({ title: '已保存', icon: 'none' });
      this.load();
    } catch (err) {
      this.setData({ saving: false });
    }
  },

  remove(e) {
    const id = e.currentTarget.dataset.id;
    const that = this;
    wx.showModal({
      title: '删除科室',
      content: '删除后不可恢复，且该科室下不能存在医生。',
      confirmColor: '#9C342A',
      success: async function (res) {
        if (!res.confirm) {
          return;
        }
        try {
          await api.deleteDepartment(id);
          wx.showToast({ title: '已删除', icon: 'none' });
          that.load();
        } catch (err) {
          // 请求层已提示
        }
      }
    });
  }
});
