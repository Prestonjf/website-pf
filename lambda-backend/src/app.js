const serverless = require('serverless-http');
const express = require('express');
const app = express();
const dc = require('./modules/workermodule');
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0;
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(function(req, res, next) {
  console.log(req);
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header('Content-Type', 'application/json');
  next();
});

app.get('/init', async (req, res, next) => {
	console.log('GET /init');

  let welcome = {};
  welcome.name = "hello";
  welcome.date = new Date();
  res.send(welcome);
});

app.post('/init', async (req, res, next) => {
	console.log('POST /');
  res.send();
});

app.put('/init', async (req, res, next) => {
	console.log('PUT /');
  const ret = await dc.putRequest(req);
  res.send(ret);
});

module.exports.handler = serverless(app);
//app.listen(3000, () => console.log(`Example app listening on port 3000!`))
