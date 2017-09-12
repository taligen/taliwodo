import os
import config

def doIt( environ, start_response ) :
    response_headers = [('Content-type','text/html')]
    start_response( '200 OK', response_headers)
  
    page_content = '<!DOCTYPE html>\n\
\n\
<html lang="en-US">\n\
    <head>\n\
        <title>Taligen script</title>\n\
        <meta name="viewport" content="width=device-width, initial-scale=1.0">\n\
\n\
        <link rel="stylesheet" href="'+config.CONTEXT+'/css/default.css">\n\
    </head>'
    
    page_content += '<body>'
    page_content += "<h1>Task list list</h1>\n"
    # f = []
    for (dirpath, dirnames, filenames) in os.walk(config.JSONDIR):
        # f.extend(filenames)
        reldir = dirpath[len(config.JSONDIR):]
        page_content += "<h2>"+reldir+"</h2>"
        page_content += "<ol>"
        # print ("dirpath: " + dirpath + ", dirnames: " + str(dirnames) + ", filenames: " + str(filenames))
        for filename in filenames:
			basefname = os.path.splitext(filename)[0]
			page_content += '<li><a href="'+config.CONTEXT+'/render'+reldir+'/'+basefname+'">'+basefname+'</a></li>'
        page_content += "</ol>"
    page_content += '</body>'

    return page_content
