#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import config
from handlers.RedirectHandler import RedirectHandler

class CreateWorkdownHandler(RedirectHandler):
    def __init__( self, environ, form, tl ):
        super().__init__( environ, form )

        self.tl = tl

    def process( self ):
        workdown   = self.tl.createWorkdown()
        return config.CONTEXT + workdown.toUrl()
