# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from repoze.what import predicates

from tg2app.lib.base import BaseController
from tg2app.model import DBSession, metadata
from tg2app import model
from tg2app.controllers.secure import SecureController

from tg2app.controllers.error import ErrorController

from sqlalchemy import desc
from datetime import datetime, timedelta
import random

__all__ = ['RootController']

def log_message(msg):
    model.DBSession.add(model.Message(msg=msg))

class RootController(BaseController):
    """
    The root controller for the tg2app application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()

    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    @expose('tg2app.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict()

    @expose('json')
    def get_users(self):
        users = DBSession.query(model.User).all()
        return {
            'users': [
                user.to_json() for user in users
            ],
        }

    @expose()
    def add_user(self, username):
        # http://typhon.csh.rit.edu:9000/add_user?username=foo

        if len(username) != 7:
            redirect('/')

        my_user = model.User(
            user_name=username,
            email_address=username + "@typhon.com",
            display_name='no display name',
        )
        DBSession.add(my_user)

        # Last thing.. redirect to another URL
        redirect('/get_users')


    @expose()
    def do_logout(self, name):
        query = model.Login.query.filter_by(name=name)

        if query.count() == 0:
            # wtf...  when would this happen?
            log_message("'%s' (who DNE) tried to logout." % name)
            redirect('http://ritfloss.rtfd.org/')

        user = query.first()
        log_message("'%s' logged out." % user.name)
        model.DBSession.delete(user)
        redirect('http://ritfloss.rtfd.org/')


    @expose()
    def do_save_fb_user(self, referring_id, id, name, access_token):

        query = model.User.query.filter_by(user_id=id)

        if query.count() == 0:
            user = model.User(
                user_id=id,
                display_name=name,
                user_name=name,
                email_address=name+"@threebean.org",
            )
            model.DBSession.add(user)

            log_message('Spidered %s.  Totally awesome.' % unicode(user))

            return "Ok."

        raise ValueError("%s already exists..." % name)


    @expose()
    def do_login(self, name, access_token):

        query = model.Login.query.filter_by(name=name)

        if query.count() == 0:
            user = model.Login(name=name)
            model.DBSession.add(user)
        elif query.count() > 1:
            # wtf...  when would this happen?
            user = query.first()
        else:
            user = query.one()

        user.access_token = access_token
        user.last_seen = datetime.now()

        log_message("%s logged in" % user.name)

        redirect(url('/waiting/{name}#access_token={token}'.format(
            name=user.name, token=user.access_token)))

    @expose('json')
    @expose('tg2app.templates.waiting', content_type='text/html')
    def waiting(self, name):
        users = model.Login.query.all()
        def prune_idle(user):
            if datetime.now() - user.last_seen > timedelta(minutes=10):
                log_message("%s went idle.  Logging out." % user.name)
                model.DBSession.delete(user)
                return False
            return True

        users = filter(prune_idle, users)

        if name not in [user.name for user in users]:
            log_message("'%s' tried unauthorized access." % name)
            redirect('/')

        messages = model.Message.query\
                .order_by(desc(model.Message.created_on))\
                .limit(7).all()

        return {
            'users':[user.__json__() for user in users],
            'messages':[msg.__json__() for msg in messages],
        }

    @expose('tg2app.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('tg2app.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('tg2app.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)

    @expose('tg2app.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('tg2app.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('tg2app.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('tg2app.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from='/'):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
