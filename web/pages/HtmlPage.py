#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import config
from handlers.Handler import Handler

class HtmlPage(Handler):
    def __init__( self, status, environ ):
        super().__init__( environ )

        self.status = status

    def handle( self, start_response ):
        response_headers = [
                ('Content-type','text/html; charset=utf-8')
        ]
        start_response( self.status, response_headers)

        content  = "<!DOCTYPE html>\n"
        content += "<html>\n"
        content += " <head>\n"
        content += self.htmlHeader()
        content += " </head>\n"
        content += " <body>\n"
        content += self.htmlContent()
        content += " </body>\n"
        content += "</html>\n"

        return [ content.encode('utf-8') ]

    def htmlHeader( self ):
        title   = self.htmlTitle()
        context = self.environ['PATH_INFO']

        return f"""
<title>{title}</title>
<link rel="stylesheet" href="{config.CONTEXT}/assets/default.css">
<script src="{config.CONTEXT}/assets/taliwodo.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
"""

    def htmlTitle( self ):
        return "My title"

    def htmlContent( self ):
        return "<p>Some great text will go here.</p>"
