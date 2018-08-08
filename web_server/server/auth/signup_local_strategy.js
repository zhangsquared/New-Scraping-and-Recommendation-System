const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;

module.exports = new PassportLocalStrategy({
  usernameField: 'email',
  passwordField: 'password',
  passReqToCallback: true
}, (req, email, password, done) => {
  const userData = {
    email: email.trim(),
    password: password
  };

  const newUser = new User(userData);
  // when store user data into mogodb,
  // mongodb will make sure the user email is uique
  // if the same user mail already exist, it returns error
  newUser.save((err) => {
    console.log('Save new user!');
    if (err) return done(err);

    return done(null);
  });
});
