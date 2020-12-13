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

export { formatTimeStamp }
