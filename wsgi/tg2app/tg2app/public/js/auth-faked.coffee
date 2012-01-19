globals = exports ? this

globals.logged_in_callback = (user) ->
    window.location = '/do_login?' + $.param({
        name: user.name,
        access_token: globals.access_token,
    })

check_auth = () ->
    if window.location.href.indexOf('waiting') != -1
        return

    globals.access_token = "foobarlol"
    faked_user = {
        name: 'shmeegle D.',
    }
    globals.logged_in_callback(faked_user)

# Start with check_auth on page load.
$(document).ready(check_auth);
