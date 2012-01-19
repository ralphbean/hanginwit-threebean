globals = exports ? this
globals.appID = "285982901458261"

globals.logged_in_callback = (obj) ->
    console.log(obj)
    if obj.error?
        alert("Some auth problem with facebook.  Failing.");
    else
        window.location = '/do_login?' + $.param({
            name: obj.name,
            access_token: globals.access_token,
        })

act_on_login = (access_token) ->
    globals.access_token = access_token
    path = "https://graph.facebook.com/me?"
    console.log(access_token)
    query = $.param({
        access_token: access_token,
        callback: 'logged_in_callback',
    })
    url = path + query

    # use jsonp to call the graph
    script = document.createElement('script')
    script.src = url
    document.body.appendChild(script)    

force_login = () ->
    path = 'https://www.facebook.com/dialog/oauth?'
    query = $.param({
        client_id: globals.appID,
        redirect_uri: window.location.href,
        response_type: 'token',
    })
    url = path + query
    window.location = url

check_auth = () ->
    if window.location.href.indexOf('waiting') != -1
        return

    if window.location.hash.length == 0
        force_login()
    else
        access_token = window.location.hash.substring(14).split('&')[0]
        act_on_login(access_token)

# Start with check_auth on page load.
$(document).ready(check_auth);
