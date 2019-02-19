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
        stepname   = self.form['stepname'].value
        stepstatus = self.form['stepstatus'].value

        if stepname.startswith( 'wodo-step-status-' ):
            stepId = stepname[ len( 'wodo-step-status-' ) : ]
            step   = self.wodo.get_step_by_id( stepId )
            if step:
                step.set_status( stepstatus )
                self.wodo.saveIfNeeded()

            stats = self.wodo.calc_checkbox_steps_stats()

            content = 'steplastupdated='           + step.get_lastupdated()
            content += '&workdownlastupdated='     + self.wodo.get_lastupdated()
            content += '&workdownsstepscompleted=' + str( stats['Completed'] )
            content += '&workdownstepspassed='     + str( stats['Passed']    )
            content += '&workdownstepsfailed='     + str( stats['Failed']    )
            content += '&workdownstepsskipped='    + str( stats['Skipped']   )

        else:
            content = ''

        start_response( '200 OK', [] )

        return [ content.encode('utf-8') ]
