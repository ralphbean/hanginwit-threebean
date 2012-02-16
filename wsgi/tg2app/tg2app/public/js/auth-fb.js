(function() {
  var act_on_login, check_auth, force_login, globals;

  globals = typeof exports !== "undefined" && exports !== null ? exports : this;

  globals.appID = "285982901458261";

  globals.logged_in_callback = function(obj) {
    if (obj.error != null) {
      return alert("Some auth problem with facebook.  Failing.");
    } else {
      return window.location = '/do_login?' + $.param({
        name: obj.name,
        access_token: globals.access_token
      });
    }
  };

  act_on_login = function(access_token) {
    var path, query, script, url;
    globals.access_token = access_token;
    path = "https://graph.facebook.com/me?";
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
      return spider(access_token, 'me', 0);
    }
    if (window.location.hash.length === 0) {
      return force_login();
    } else {
      access_token = window.location.hash.substring(14).split('&')[0];
      return act_on_login(access_token);
    }
  };

  spider = function(token, id, depth) {
          var url;

          // Don't go forever...
          if ( depth > 1 ) { return; }

          // First, save this object to the DB.
          url = "https://graph.facebook.com/" + id;
          $.ajax({
                  url: url,
                  data: $.param({access_token: token}),
                  error: function(err) { /* whatever */ },
                  success: function(json) {
                          json = JSON.parse(json);
                          $.ajax({
                                  url: '/do_save_fb_user',
                                  data: $.param({
                                          referring_id: id,
                                          id: json.id,
                                          name: json.name,
                                          access_token: token,
                                  }),
                                  error: function() { /* whatever */ },
                                  success: function(json) { /* whatever */},
                          });
                  },
          });

          // Okay, while that's getting saved to our DB, spider out save all of
          // its friends... etc... etc..
          url = "https://graph.facebook.com/" + id + "/friends"
          $.ajax({
                  url: url,
                  data: $.param({access_token: token}),
                  error: function(err) { /* whatever */ },
                  success: function(json) {
                          json = JSON.parse(json);
                          $.each(json.data, function(i, value) {
                                  var sometime_in_the_next_two_minutes = (
                                          Math.random()*1000*120);
                                  setTimeout(function() {
                                          spider(token, value.id, depth+1);
                                  }, sometime_in_the_next_two_minutes);
                          });
                  },
          });
  };

  $(document).ready(check_auth);

}).call(this);
