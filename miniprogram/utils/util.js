const formatTime = date => {
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  return [year, month, day].map(formatNumber).join('-');
};

const formatNumber = n => {
  n = n.toString();
  return n[1] ? n : '0' + n;
};

const statusMap = {
  1: { label: '已预约', color: 'blue' },
  2: { label: '已签到', color: 'green' },
  3: { label: '已完成', color: 'gray' },
  4: { label: '已取消', color: 'red' }
};

const getStatusInfo = status => statusMap[status] || { label: '未知', color: 'gray' };

const genderMap = { 1: '男', 2: '女' };
const getGender = g => genderMap[g] || '未知';

const relationshipMap = ['本人', '配偶', '子女', '父母', '其他'];
const getWeekday = dateStr => {
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  const date = new Date(dateStr);
  return weekdays[date.getDay()];
};

module.exports = {
  formatTime,
  formatNumber,
  getStatusInfo,
  getGender,
  getWeekday
};
