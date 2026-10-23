const WEEKDAYS = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];

const STATUS_TEXT = {
  1: '待就诊',
  2: '已签到',
  3: '已完成',
  4: '已取消'
};

/** iOS 不认 2026-10-24 这种写法，统一替换成斜杠 */
function toDate(value) {
  if (!value) {
    return null;
  }
  const text = String(value)
    .replace(/-/g, '/')
    .replace('T', ' ')
    .replace(/\.\d+$/, '');
  const date = new Date(text);
  return isNaN(date.getTime()) ? null : date;
}

function weekday(value) {
  const date = toDate(value);
  return date ? WEEKDAYS[date.getDay()] : '';
}

function dayNumber(value) {
  return String(value || '').slice(8, 10);
}

function shortDate(value) {
  return String(value || '').slice(5, 10);
}

function dateText(value) {
  if (!value) {
    return '';
  }
  const day = weekday(value);
  return day ? String(value).slice(0, 10) + ' ' + day : String(value).slice(0, 10);
}

function hhmm(value) {
  return value ? String(value).slice(0, 5) : '';
}

function timeRange(start, end) {
  const from = hhmm(start);
  const to = hhmm(end);
  return from && to ? from + ' - ' + to : '';
}

function money(value) {
  const number = Number(value || 0);
  return number.toFixed(2).replace(/\.00$/, '');
}

function maskIdCard(idCard) {
  if (!idCard || idCard.length < 10) {
    return idCard || '';
  }
  return idCard.slice(0, 6) + '********' + idCard.slice(-4);
}

function genderText(gender) {
  return Number(gender) === 2 ? '女' : '男';
}

function statusText(status) {
  return STATUS_TEXT[status] || '未知';
}

function initial(name) {
  return name ? String(name).slice(0, 1) : '患';
}

module.exports = {
  toDate,
  weekday,
  dayNumber,
  shortDate,
  dateText,
  hhmm,
  timeRange,
  money,
  maskIdCard,
  genderText,
  statusText,
  initial
};
