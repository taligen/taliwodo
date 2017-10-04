
import cgi
import cgitb

import config
import error
import overview
import create
import render
import update
import delete

# All invocations, other than for static files, end up here

def application( environ, start_response ) :
  cgitb.enable()

  # print ("config.CONTEXT: " + config.CONTEXT + ", PATH_INFO: " + environ['PATH_INFO'])
  
  if environ['PATH_INFO'] == '/' or environ['PATH_INFO'] == '':
    content = overview.doIt( environ, start_response )
    
  elif environ['PATH_INFO'].startswith( '/create/' ) and environ['REQUEST_METHOD'] == 'POST':
    tlId = environ['PATH_INFO'][len('/create/'):]
    content = create.doIt( tlId, environ, start_response )
    
  elif environ['PATH_INFO'].startswith( '/delete/' ) and environ['REQUEST_METHOD'] == 'POST':
    tlId = environ['PATH_INFO'][len('/delete/'):]
    content = delete.doIt( tlId, environ, start_response )

  elif environ['PATH_INFO'].startswith( '/render/' ) :
    tlId = environ['PATH_INFO'][len('/render/'):]
    if environ['REQUEST_METHOD'] == 'POST' :
      content = update.doIt( tlId, environ, start_response )
    else :
      content = render.doIt( tlId, environ, start_response )
  else :
    content = error.doIt( '404 Not Found', environ, start_response )
    content += "<p>File not found: " + environ['PATH_INFO'] + "</p>\n"

  return content

