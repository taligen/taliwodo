#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

class Handler:
    def __init__( self, environ ):
        self.environ = environ

    def handle( self, start_response ):
        """
        Override this.
        """

        response_headers = [
                ('Content-type','text/html')
        ]
        start_response( '200 OK', response_headers )

        content = "<p>Placeholder content</p>\n"

        return [ content.encode('utf-8') ]
