globals = exports ? this

globals.polling_interval = 3000

poll = () ->
    toks = window.location.href.split('/')
    last = toks[4]
    name = last.split('#')[0]
    $.ajax({
        url: '/waiting/' + name + '.json',
        error: (err) ->
            console.log("Got an error")
            console.log(err)
        success: (json) ->
            $("#users li").remove();
            $(json['users']).each((i, user) ->
                $("#users ul").append("<li>" + user.name + "</li>")
            )
            $("#messages li").remove();
            $(json['messages']).each((i, msg) ->
                $("#messages ul").append("<li>" + msg.msg + "</li>")
            )
            setTimeout(poll, globals.polling_interval)
    })

$(document).ready(setTimeout(poll, globals.polling_interval))

# This 'before-unload' bind doesn't actually work; it never fires!  Oh well!
$(document).bind('before-unload', () ->
    toks = window.location.href.split('/')
    last = toks[4]
    name = last.split('#')[0]
    $.ajax({
        url: '/do_logout/' + name
    })
)
