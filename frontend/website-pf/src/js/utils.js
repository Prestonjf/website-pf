export const name = 'utils';

function formatTimeStamp(str) {
    let time = '';
    var options = {year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', 
    minute:'2-digit', hour12: false};
    if (str) {
      time = new Date(str);
      return time.toLocaleTimeString('en-US', options) + ' EST';
    }
    return time;
  }

function getContentFileUrl(filePath, postPath) {
  const normalizedFilePath = (filePath || '').replace(/^\/+/, '');
  const normalizedPostPath = (postPath || '').replace(/^\/+/, '');
  const hasSpecialPrefix = ['media', 'config', 'posts'].some((segment) => normalizedFilePath.startsWith(segment + '/'));
  const prefix = hasSpecialPrefix ? '' : `posts/${normalizedPostPath}`;
  const separator = prefix ? '/' : '';
  const p = `${process.env.REACT_APP_WEB_URL}/${prefix}${separator}${normalizedFilePath}`;
  return p;
}


function getPostPath(path) {
  let p = '/post/' + path;
  return p;
}

export { formatTimeStamp, getContentFileUrl, getPostPath }
