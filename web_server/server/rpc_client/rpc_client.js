var logger = require('../logger');
// https://www.npmjs.com/package/jayson
var jayson = require('jayson');

var HOSTNAME = 'localhost'
var PORT = 4040

// create a client
var client = jayson.client.http({
  port: PORT,
  hostname: HOSTNAME
});
 
// Test method
function add(a, b, callback) {
  client.request('add', [a, b], function(err, response) {
    if(err) throw err;
    logger.info(response.result);
    callback(response.result);
  });
}

//  get news summaries for a user
function getNewsSummariesForUser(user_id, page_num, callback){
  client.request('getNewsSummariesForUser', [user_id, page_num], function(err, response) {
    if(err) {
      throw err;
    }
    logger.info(response.result);
    callback(response.result);
  });
}

// log a news click event for a user
function logNewsClickForUser(user_id, news_id){
  client.request('logNewsClickForUser', [user_id, news_id], function(err, response){
    if(err) throw err;
    console.log(response);
  });
}

module.exports = {
  add: add,
  getNewsSummariesForUser: getNewsSummariesForUser,
  logNewsClickForUser: logNewsClickForUser
}
