var auth = require('./routes/auth');
var bodyParser = require('body-parser');
var cors = require('cors');
var express = require('express');
var passport = require('passport');
var path = require('path');

// import routes
var index = require('./routes/index');
var news = require('./routes/news');

var app = express();

// TODO: remove this after development is done
app.use(cors());
// TODO: remove this after development is done
app.all('*', function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  next();
});

// login and signup requirest are POST
// server should handle POST request
// bodyParser is used to pass the body of the POST request
// use bodyParser middleware before any handler of POST
app.use(bodyParser.json());

// connect to mlab
var config = require('./config/config.json');
require('./models/main.js').connect(config.mongoDbUri); // json as object
// auth checker has to be after mongo db connection
var authChecker = require('./auth/auth_checker');

// load passport strategies.
app.use(passport.initialize());
passport.use('local-signup', require('./auth/signup_local_strategy'));
passport.use('local-login', require('./auth/login_local_strategy'));

// view engine setup
app.set('views', path.join(__dirname, '../client/build'));
app.set('view engine', 'jade');
// server static files
app.use('/static', express.static(path.join(__dirname, '../client/build/static')));

console.log("Web server started...");

app.use('/', index);
app.use('/auth', auth);
// authChecker must use before news
// we want auth check before sends the news
app.use('/news', authChecker);
app.use('/news', news);
app.use('/login', index);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;

