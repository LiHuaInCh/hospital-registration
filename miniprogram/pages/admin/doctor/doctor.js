const api = require('../../../utils/api');
const auth = require('../../../utils/auth');
const format = require('../../../utils/format');

const TITLES = ['主任医师', '副主任医师', '主治医师', '住院医师'];

const EMPTY = {
  name: '',
  departmentId: null,
  title: '主治医师',
  gender: 1,
  consultationFee: '',
  specialty: '',
  description: ''
};

Page({
  data: {
    doctors: [],
    departments: [],
    loading: true,
    showDialog: false,
    isEdit: false,
    saving: false,
    form: EMPTY,
    titles: TITLES,
    titleIndex: 2,
    deptIndex: 0
  },

  onLoad() {
    if (!auth.requireAdmin()) {
      return;
    }
    this.load();
  },

  async load() {
    try {
      const results = await Promise.all([api.doctors(), api.departments()]);
      const doctors = (results[0] || []).map(function (item) {
        return {
          id: item.id,
          name: item.name,
          title: item.title,
          departmentId: item.departmentId,
          departmentName: item.departmentName,
          specialty: item.specialty,
          description: item.description || '',
          gender: item.gender,
          status: item.status,
          consultationFee: item.consultationFee,
          fee: format.money(item.consultationFee),
          initial: format.initial(item.name)
        };
      });
      this.setData({ doctors: doctors, departments: results[1] || [] });
    } catch (err) {
      // 请求层已提示
    } finally {
      this.setData({ loading: false });
    }
  },

  showAdd() {
    const department = this.data.departments[0];
    this.setData({
      showDialog: true,
      isEdit: false,
      titleIndex: 2,
      deptIndex: 0,
      form: Object.assign({}, EMPTY, {
        title: TITLES[2],
        departmentId: department ? department.id : null
      })
    });
  },

  showEdit(e) {
    const id = Number(e.currentTarget.dataset.id);
    const item = this.data.doctors.filter(function (row) {
      return row.id === id;
    })[0];
    if (!item) {
      return;
    }
    const titleIndex = Math.max(0, TITLES.indexOf(item.title));
    let deptIndex = 0;
    this.data.departments.forEach(function (department, index) {
      if (department.id === item.departmentId) {
        deptIndex = index;
      }
    });
    this.setData({
      showDialog: true,
      isEdit: true,
      titleIndex: titleIndex,
      deptIndex: deptIndex,
      form: {
        id: item.id,
        name: item.name,
        departmentId: item.departmentId,
        title: item.title || TITLES[titleIndex],
        gender: item.gender || 1,
        consultationFee: format.money(item.consultationFee),
        specialty: item.specialty || '',
        description: item.description || ''
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

  onDeptChange(e) {
    const index = Number(e.detail.value);
    this.setData({
      deptIndex: index,
      'form.departmentId': this.data.departments[index].id
    });
  },

  onTitleChange(e) {
    const index = Number(e.detail.value);
    this.setData({ titleIndex: index, 'form.title': TITLES[index] });
  },

  onGender(e) {
    this.setData({ 'form.gender': Number(e.currentTarget.dataset.gender) });
  },

  async save() {
    const form = this.data.form;
    if (!form.name || !form.name.trim()) {
      wx.showToast({ title: '请填写医生姓名', icon: 'none' });
      return;
    }
    if (!form.departmentId) {
      wx.showToast({ title: '请选择所属科室', icon: 'none' });
      return;
    }
    const fee = Number(form.consultationFee);
    if (isNaN(fee) || fee < 0) {
      wx.showToast({ title: '请填写正确的挂号费', icon: 'none' });
      return;
    }
    if (this.data.saving) {
      return;
    }
    this.setData({ saving: true });
    try {
      const payload = {
        name: form.name.trim(),
        departmentId: form.departmentId,
        title: form.title,
        gender: form.gender,
        consultationFee: fee,
        specialty: form.specialty,
        description: form.description
      };
      if (this.data.isEdit) {
        payload.id = form.id;
        await api.updateDoctor(payload);
      } else {
        await api.addDoctor(payload);
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
      title: '删除医生',
      content: '删除后其排班一并移除，已有挂号记录的医生无法删除。',
      confirmColor: '#9C342A',
      success: async function (res) {
        if (!res.confirm) {
          return;
        }
        try {
          await api.deleteDoctor(id);
          wx.showToast({ title: '已删除', icon: 'none' });
          that.load();
        } catch (err) {
          // 请求层已提示
        }
      }
    });
  }
});
