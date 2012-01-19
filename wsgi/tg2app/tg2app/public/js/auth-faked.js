(function() {
  var check_auth, globals;

  globals = typeof exports !== "undefined" && exports !== null ? exports : this;

  globals.logged_in_callback = function(user) {
    return window.location = '/do_login?' + $.param({
      name: user.name,
      access_token: globals.access_token
    });
  };

  check_auth = function() {
    var faked_user;
    if (window.location.href.indexOf('waiting') !== -1) return;
    globals.access_token = "foobarlol";
    faked_user = {
      name: 'shmeegle D.'
    };
    return globals.logged_in_callback(faked_user);
  };

  $(document).ready(check_auth);

}).call(this);
