(function() {
  var act_on_login, check_auth, force_login, globals;

  globals = typeof exports !== "undefined" && exports !== null ? exports : this;

  globals.appID = "285982901458261";

  globals.logged_in_callback = function(obj) {
    console.log(obj);
    if (obj.error != null) {
      return alert("Some auth problem with facebook.  Failing.");
    } else {
      return window.location = '/do_login?' + $.param({
        id: obj.id,
        name: obj.name,
        access_token: globals.access_token
      });
    }
  };

  act_on_login = function(access_token) {
    var path, query, script, url;
    globals.access_token = access_token;
    path = "https://graph.facebook.com/me?";
    console.log(access_token);
    query = $.param({
      access_token: access_token,
      callback: 'logged_in_callback'
    });
    url = path + query;
    script = document.createElement('script');
    script.src = url;
    return document.body.appendChild(script);
  };

  force_login = function() {
    var path, query, url;
    path = 'https://www.facebook.com/dialog/oauth?';
    query = $.param({
      client_id: globals.appID,
      redirect_uri: window.location.href,
      response_type: 'token'
    });
    url = path + query;
    return window.location = url;
  };

  check_auth = function() {
    var access_token;
    if (window.location.href.indexOf('waiting') !== -1) {
      access_token = window.location.hash.substring(14).split('&')[0];
      return spider(access_token, 'me');
    }
    if (window.location.hash.length === 0) {
      return force_login();
    } else {
      access_token = window.location.hash.substring(14).split('&')[0];
      return act_on_login(access_token);
    }
  };

  spider = function(token, id) {
          console.log("Spidering on: " + id);
          // TODO -- first thing, save id
          var url = "https://graph.facebook.com/" + id + "/friends"
          $.ajax({
                  url: url,
                  data: $.param({
                          access_token: token,
                  }),
                  error: function(err) {
                          console.log("error on id: " + id);
                          console.log(err);
                  },
                  success: function(json) {
                          console.log("success on id: " + id);
                          console.log(json);
                          $.each(json.data, function(i, value) {
                                  console.log(i);
                                  console.log(value);
                                  spider(token, value.id);
                          });
                  },
          });
  };

  $(document).ready(check_auth);

}).call(this);
