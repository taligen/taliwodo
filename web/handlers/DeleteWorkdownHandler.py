#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import config
from handlers.RedirectHandler import RedirectHandler

class DeleteWorkdownHandler(RedirectHandler):
    def __init__( self, environ, form, wodo ):
        super().__init__( environ, form )

        self.wodo = wodo

    def process( self ):
        self.wodo.delete()

        return config.CONTEXT + '/'
