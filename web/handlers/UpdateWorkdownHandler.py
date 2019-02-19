#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import config
from handlers.Handler import Handler

class UpdateWorkdownHandler(Handler):
    def __init__( self, environ, form, wodo ):
        super().__init__( environ )

        self.form = form
        self.wodo = wodo


    def handle( self, start_response ):
        name  = self.form['name'].value
        value = self.form['value'].value

        if name.startswith( 'wodo-step-status-' ):
            stepId = name[ len( 'wodo-step-status-' ) : ]
            step   = self.wodo.get_step_by_id( stepId )
            if step:
                step.set_status( value )
                self.wodo.saveIfNeeded()

            content = 'lastupdated=' + step.get_lastupdated()
        else:
            content = ''

        start_response( '200 OK', [] )

        return [ content.encode('utf-8') ]
