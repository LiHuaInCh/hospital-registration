const api = require('../../../utils/api');
const auth = require('../../../utils/auth');

const RELATIONSHIPS = ['本人', '配偶', '子女', '父母', '其他'];

Page({
  data: {
    id: null,
    isEdit: false,
    form: {
      name: '',
      idCard: '',
      phone: '',
      gender: 1,
      age: '',
      relationship: '本人',
      isDefault: false
    },
    relationships: RELATIONSHIPS,
    relationshipIndex: 0,
    submitting: false
  },

  onLoad(options) {
    if (!auth.requireLogin()) {
      return;
    }
    if (options.id) {
      this.setData({ id: Number(options.id), isEdit: true });
      wx.setNavigationBarTitle({ title: '编辑就诊人' });
      this.loadPatient(options.id);
    }
  },

  async loadPatient(id) {
    try {
      const patient = await api.patientDetail(id);
      const index = RELATIONSHIPS.indexOf(patient.relationship || '本人');
      this.setData({
        form: {
          name: patient.name || '',
          idCard: patient.idCard || '',
          phone: patient.phone || '',
          gender: patient.gender || 1,
          age: patient.age === null || patient.age === undefined ? '' : String(patient.age),
          relationship: patient.relationship || '本人',
          isDefault: patient.isDefault === 1
        },
        relationshipIndex: index < 0 ? 0 : index
      });
    } catch (err) {
      // 请求层已提示
    }
  },

  onInput(e) {
    const field = e.currentTarget.dataset.field;
    const patch = {};
    patch['form.' + field] = e.detail.value;
    this.setData(patch);
  },

  setGender(e) {
    this.setData({ 'form.gender': Number(e.currentTarget.dataset.gender) });
  },

  onRelationship(e) {
    const index = Number(e.detail.value);
    this.setData({
      relationshipIndex: index,
      'form.relationship': RELATIONSHIPS[index]
    });
  },

  onDefault(e) {
    this.setData({ 'form.isDefault': e.detail.value });
  },

  validate() {
    const form = this.data.form;
    if (!form.name.trim()) {
      wx.showToast({ title: '请填写就诊人姓名', icon: 'none' });
      return false;
    }
    if (!/^\d{17}[\dXx]$/.test(form.idCard.trim())) {
      wx.showToast({ title: '身份证号应为 18 位', icon: 'none' });
      return false;
    }
    if (!/^1[3-9]\d{9}$/.test(form.phone.trim())) {
      wx.showToast({ title: '手机号格式不正确', icon: 'none' });
      return false;
    }
    return true;
  },

  async submit() {
    if (this.data.submitting || !this.validate()) {
      return;
    }
    const form = this.data.form;
    const payload = {
      name: form.name.trim(),
      idCard: form.idCard.trim(),
      phone: form.phone.trim(),
      gender: form.gender,
      age: form.age === '' ? null : Number(form.age),
      relationship: form.relationship,
      isDefault: form.isDefault ? 1 : 0
    };
    this.setData({ submitting: true });
    try {
      if (this.data.isEdit) {
        payload.id = this.data.id;
        await api.updatePatient(payload);
      } else {
        await api.addPatient(payload);
      }
      wx.showToast({ title: this.data.isEdit ? '已保存' : '已添加', icon: 'none' });
      setTimeout(function () {
        wx.navigateBack();
      }, 500);
    } catch (err) {
      this.setData({ submitting: false });
    }
  }
});
