const axios = require('axios');
const https = require('https');

module.exports = {
  putRequest: function(req) {
    const agent = new https.Agent({ rejectUnauthorized: false });
    let data = axios({
      method: 'PUT',
      url: '',
      httsAgent: agent,
      data: {test : 'hello PUT'}
    })
    .then(res => {
      console.log('success put');
      console.log(res.data);
      return res.data;
    })
    .catch(error => {
      console.error('error put');
      console.error(error.response.data);
      return error.response.data;
    });
    return data;
  }
};
