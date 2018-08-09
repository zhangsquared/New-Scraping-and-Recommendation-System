const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../config/config.json');

// middleware
// check if the token is valid,
// if valid, call "next" to send the news
// otherwise, return error
module.exports = (req, res, next) => {
  console.log('auth_checker: req: ' + req.headers.authorization);

  if(!req.headers.authorization) {
    return res.status(401).end();
  }

  // get the last part from a authorization header string
  // like "earer token-value"
  const token = req.headers.authorization.split(' ')[1];
  
  // docode the token using s secret key-phrase
  return jwt.verify(token, config.jwtSecret, (err, decoded) => {
    // the 401 code is for unauthorized status
    if(err) return res.status(401).end();

    const id = decoded.sub;

    // check if a user exists
    return User.findById(id, (userErr, user) => {
      if(userErr || !user) {
        return res.status(401).end();
      }
      return next();
    });
  });
};