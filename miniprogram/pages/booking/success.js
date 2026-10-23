const format = require('../../utils/format');

Page({
  data: {
    order: null,
    dateText: '',
    timeText: '',
    fee: '0'
  },

  onLoad() {
    const order = getApp().globalData.lastOrder;
    if (!order) {
      wx.switchTab({ url: '/pages/orders/orders' });
      return;
    }
    this.setData({
      order: order,
      dateText: format.dateText(order.workDate),
      timeText: order.timeSlot + (order.startTime ? '  ' + format.timeRange(order.startTime, order.endTime) : ''),
      fee: format.money(order.fee)
    });
  },

  goOrders() {
    wx.switchTab({ url: '/pages/orders/orders' });
  },

  goHome() {
    wx.switchTab({ url: '/pages/index/index' });
  }
});
