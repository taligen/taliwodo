#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

from pages.HtmlPage import HtmlPage

class ErrorPage(HtmlPage):
    def __init__( self, status, environ, title, msg ):
        super().__init__( status, environ )

        self.title   = title
        self.msg = msg

    def htmlTitle( self ):
        return self.title

    def htmlContent( self ):
        return f"""
<h5>Error:</h5>
<h1 class="error">{self.title}</h1>
<p>{self.msg}</p>
"""
