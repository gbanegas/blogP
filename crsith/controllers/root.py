# -*- coding: utf-8 -*-
"""Main Controller"""

import re
from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg import predicates
from crsith import model
from crsith.controllers.secure import SecureController
from crsith.model import DBSession, metadata
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from crsith.lib.base import BaseController
from crsith.controllers.error import ErrorController
from crsith.model.page import Page
from docutils.core import publish_parts

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the crsith application.

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

    def _before(self, *args, **kw):
        tmpl_context.project_name = "CrSith"

    @expose('crsith.templates.index')
    def index(self):
        """Handle the front-page."""
        pages = DBSession.query(Page).order_by(Page.title)
        return dict(page='index',pages=pages)

    @expose('crsith.templates.page')
    def page(self, pagename):
        from sqlalchemy.exc import InvalidRequestError
        try:
            page = DBSession.query(Page).filter_by(pagename=pagename).one()
        except InvalidRequestError:
            raise redirect("notfound", pagename=pagename)
        content = publish_parts(page.data, writer_name="html")["html_body"]
        root = url('/')
        content = wikiwords.sub(r'<a href="%s\1">\1</a>' % root, content)
        return dict(content=content, wikipage=page)


    @expose("crsith.templates.pagelist")
    def pagelist(self):
        pages = [page.pagename for page in DBSession.query(Page).order_by(Page.pagename)]
        return dict(pages=pages)
    
    @expose(template="crsith.templates.edit")
    @require(predicates.is_user('manager', msg=l_('Only for the editor')))
    def edit(self, pagename):
        page = DBSession.query(Page).filter_by(pagename=pagename).one()
        return dict(wikipage=page)

    @expose(template="crsith.templates.add")
    @require(predicates.is_user('manager', msg=l_('Only for the editor')))
    def add(self):
        page = Page()
        return dict(wikipage=page)

    @expose()
    @require(predicates.is_user('manager', msg=l_('Only for the editor')))
    def save_new(self, pagename, data, title, submit):
        page = Page()
        page.pagename = title
        page.data = data
        page.title = title
        DBSession.add(page)
        redirect("/" + pagename)


    @expose()
    @require(predicates.is_user('manager', msg=l_('Only for the editor')))
    def save(self, pagename, data, title, submit):
        page = DBSession.query(Page).filter_by(pagename=pagename).one()
        page.data = data
        page.title = title
        redirect("/" + pagename)

    @expose('crsith.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')


    @expose('crsith.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(page='data', params=kw)
    @expose('crsith.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))




    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('crsith.templates.index')
    @require(predicates.is_user('manager', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('crsith.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ.get('repoze.who.logins', 0)
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login', params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
