
import cgi
import cgitb

import config
import error
import overview
import render
import update

# All invocations, other than for static files, end up here

def application( environ, start_response ) :
  cgitb.enable()

  if environ['PATH_INFO'] == '/' :
    content = overview.doIt( environ, start_response )

  elif environ['PATH_INFO'].startswith( '/render/' ) :
    if environ['REQUEST_METHOD'] == 'POST' :
      content = update.doIt( environ, start_response )
    else :
      content = render.doIt( environ, start_response )
  else :
    content = error.doIt( '404 Not Found', environ, start_response )
    content += "<p>Not found: " + environ['PATH_INFO'] + "</p>\n"

  return content
