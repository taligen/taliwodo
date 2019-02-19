#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import cgi
import cgitb

from handlers.CreateWorkdownHandler import CreateWorkdownHandler
from handlers.DeleteWorkdownHandler import DeleteWorkdownHandler
from handlers.UpdateWorkdownHandler import UpdateWorkdownHandler
from model.TaskList import TaskList
from model.Workdown import Workdown
from pages.ErrorPage import ErrorPage
from pages.NotFoundPage import NotFoundPage
from pages.OverviewPage import OverviewPage
from pages.WorkdownPage import WorkdownPage

# All routing, other than for static files, is done here.

def application( environ, start_response ) :
    cgitb.enable()

    path   = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']

    handler = None
    form = cgi.FieldStorage(
            fp                = environ['wsgi.input'],
            environ           = environ,
            keep_blank_values = True )

    verb = form.getvalue( 'verb' )

    if path == '/':
       handler = OverviewPage( environ )

    else:
        tl   = TaskList.loadFromUrlIfExists( path )
        wodo = Workdown.loadFromUrlIfExists( path )

        # print( "XXX tl=" + str(tl) + ", wodo=" + str(wodo) + ", path=" + path )

        if tl:
            if method == 'POST':
                if verb == 'createworkdown':
                    handler = CreateWorkdownHandler( environ, form, tl )

        elif wodo:
            if method == 'POST':
                if verb == 'deleteworkdown':
                    handler = DeleteWorkdownHandler( environ, form, wodo )
                elif verb == 'updateworkdown':
                    handler = UpdateWorkdownHandler( environ, form, wodo )
            else:
                handler = WorkdownPage( environ, wodo )

    if handler == None:
        handler = NotFoundPage( environ )

    content = handler.handle( start_response )
    return content
