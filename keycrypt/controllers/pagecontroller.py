# -*- coding: utf-8 -*-
"""Page Controller"""

import re
import time
import datetime
from sqlalchemy import desc, asc
from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg import predicates
from keycrypt import model
from keycrypt.controllers.secure import SecureController
from keycrypt.model import DBSession, metadata
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from keycrypt.lib.base import BaseController
from keycrypt.controllers.error import ErrorController
from keycrypt.model.page import Page
from keycrypt.model.auth import User
from docutils.core import publish_parts


class PageController(BaseController):
 	
 	def getPage(self, pagename):
 		from sqlalchemy.exc import InvalidRequestError
 		try:
 			page = DBSession.query(Page).filter_by(pagename=pagename).one()
 			return page
 		except InvalidRequestError:
 			raise redirect("notfound", pagename=pagename)


 	def getAllNamePages(self):
 		pages = [page.pagename for page in DBSession.query(Page).order_by(Page.date)]
 		return pages


 	def getAllPages(self):
 		pages = DBSession.query(Page).order_by(asc(Page.date))
 		return pages
 		
 	def save(self, pagename, title, data, author, tags):
 		page = Page()
 		page.pagename = title
 		page.data = data
 		page.title = title
 		page.date = time.strftime("%c")
 		page.author = DBSession.query(User).filter_by(user_name=author).first().user_id
 		page.tags = tags
 		return page

 	def searchPages(self, tag):
 		pages = DBSession.query(Page).filter_by(Page.tags.contains(tag)).order_by(desc(Page.date))
 		return pages