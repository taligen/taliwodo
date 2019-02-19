#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import config
from handlers.Handler import Handler

class RedirectHandler(Handler):
    def __init__( self, environ, form ):
        super().__init__( environ )
        self.form = form

    def handle( self, start_response ):
        location = self.process()

        response_headers = [
            ( 'Location', location )
        ]
        start_response( '303 See Other', response_headers )

        content = "<p>Redirecting to " + location + "</p>\n"

        return [ content.encode('utf-8') ]

    def process( self ):
        return config.DEFAULTURL
