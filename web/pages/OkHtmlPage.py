#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

from pages.HtmlPage import HtmlPage

class OkHtmlPage(HtmlPage):
    def __init__( self, environ ):
        super().__init__( '200 OK', environ )
