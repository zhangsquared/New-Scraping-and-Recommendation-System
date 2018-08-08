var client = require('./rpc_client');

// invoke add
client.add(111, 2, function(res){
  console.assert(res == 113);
});

// invoke getNewsSummariesForUser
client.getNewsSummariesForUser('user1', 1, function(res) {
  console.log("test: " + res);
  console.assert(res != null);
})

// invoke logNewsClickForUser
client.logNewsClickForUser('user1', 'news1');
