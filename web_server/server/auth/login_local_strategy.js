const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
const config = require('../config/config.json');

module.exports = new PassportLocalStrategy({
    // email and password should match the lgin form set from client
    usernameField: 'email',
    passwordField: 'password',
    session: false, // default value
    passReqToCallback: true // default value
    // done: callback, the equivilent of next()
  }, (req, email, password, done) => {
    console.log("login strategy for email: " + email);
    const userData = {
      email: email.trim(),
      password: password
    };
    // find a user by email address
    return User.findOne({email: userData.email}, (err, user) => {
      if(err) return done(err);

      // when user not found, return error message
      if(!user){
        const error = new Error('Incorrect email or password');
        error.name = 'IncorrectCredentialsError';
        return done(error);
      }

      // check if a hased password is equal to a value saved in db
      return user.comparePassword(userData.password, (passwordErr, isMatch) => {
        if(passwordErr) return done(passwordErr);

        // if not match, set error message
        if(!isMatch){
          const error = new Error('Incorrect email or password');
          error.name = 'IncorrectCredentialsError';
          return done(error);
        }

        const payload = { sub: user._id}; // mongodb internal id
        // create a token string
        const token = jwt.sign(payload, config.jwtSecret);

        return done(null, token, null);
      })
    })

  }
)