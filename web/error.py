

def doIt( status, environ, start_response ) :
  response_headers = [('Content-type','text/html')]
  start_response( status, response_headers)

  return [b'']
