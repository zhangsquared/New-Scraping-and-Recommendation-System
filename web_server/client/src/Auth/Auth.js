class Auth {

  // put it in local storage, not cookie
  // localStorage has large space(5MB) than cookie(4k)
  static authenticateUser(token, email){
    localStorage.setItem('token', token);
    localStorage.setItem('email', email); // save email to show on NavBar
  }

  static isUserAuthenticated() {
    // on the client side, it cannot check if the token is sent by server
    // when client send loadMoreNews request, server will check the token
    return localStorage.getItem('token') !== null;
  }

  static deauthenticatedUser(){
    localStorage.removeItem('token');
    localStorage.removeItem('email');
  }

  static getToken(){
    return localStorage.getItem('token');
  }

  static getEmail(){
    return localStorage.getItem('email');
  }

}

export default Auth;