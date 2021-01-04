export const name = 'utils';

function formatTimeStamp(str) {
    let time = '';
    var options = {year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', 
    minute:'2-digit', hour12: false};
    if (str) {
      time = new Date(str);
      return time.toLocaleTimeString('en-US', options) + ' EST';
    }
    return time;
  }

function getPostFileUrl(path, file) {
  let p = process.env.REACT_APP_WEB_URL + '/posts/' + path;
  if (file) p += "/" + file;
  return p;
}


function getPostPath(path) {
  let p = '/post/' + path;
  return p;
}

export { formatTimeStamp, getPostFileUrl, getPostPath }
