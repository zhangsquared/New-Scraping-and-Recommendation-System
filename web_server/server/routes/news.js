var express = require('express');
var router = express.Router();
var logger = require('../logger');
var rpc_client = require('../rpc_client/rpc_client')

/* GET users listing. */
router.get('/userId=:userId&pageNum=:pageNum', function(req, res, next) {
  user_id = req.params['userId'];
  page_num = req.params['pageNum'];

  logger.info('get news: user_id: ' + user_id + " page_num: "+ page_num);

  rpc_client.getNewsSummariesForUser(user_id, page_num, function(response) {
    res.json(response);
  });
});

// log news click event
router.post('/userId=:userId&newsId=:newsId', function(req, res, next) {
  console.log('logging news click...');
  var user_id = req.params['userId'];
  var news_id = req.params['newsId'];

  rpc_client.logNewsClickForUser(user_id, news_id);
  // just send the status code to the front end.
  // no need to send other reponse
  res.status(200);
});

module.exports = router;
