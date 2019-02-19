#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

from pages.ErrorPage import ErrorPage

class NotFoundPage(ErrorPage):
    def __init__( self, environ ) :
        super().__init__( '404 Not Found', environ, '404 Not Found', '<p>File not found.</p>' )
