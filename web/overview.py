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
    print ("TALIDIR: "+config.TALIDIR+", WODODIR: "+config.WODODIR)
    # f = []
    for (talidirpath, talidirnames, talifilenames) in os.walk(config.TALIDIR):
        talifilenames.sort()
        wododirpath = ""
        wododirnames = []
        wodofilenames = []
        print ("... also looking in "+config.WODODIR+talidirpath[len(config.TALIDIR):])
        for (dirpath, dirnames, filenames) in os.walk(config.WODODIR+talidirpath[len(config.TALIDIR):]):
            wodofilenames = filenames
            # f.extend(filenames)
            wododirpath = dirpath
            wododirnames = dirnames
            break
        wodofilenames.sort()
        talireldir = talidirpath[len(config.TALIDIR):]
        page_content += "<h2>"+talireldir+"</h2>"
        page_content += '<form method="post">'
        page_content += "<ol>"
        print ("talidirpath: " + talidirpath + ", talidirnames: " + str(talidirnames) + ", talifilenames: " + str(talifilenames))
        print ("wododirpath: " + wododirpath + ", wododirnames: " + str(wododirnames) + ", wodofilenames: " + str(wodofilenames))
        tali_i = 0
        wodo_i = 0
        talibasefname = ""
        wodobasefname = ""
        if len(talifilenames) > 0:
            talibasefname = os.path.splitext(talifilenames[tali_i])[0]
        if len(wodofilenames) > 0:
            wodobasefname = os.path.splitext(wodofilenames[wodo_i])[0]
        print("   talibasefiname: "+talibasefname+", wodobasefname: "+wodobasefname)
        while tali_i < len(talifilenames) or wodo_i < len(wodofilenames):
            if talibasefname < wodobasefname[:-16] or wodobasefname == "":
                print("      talibasefname ("+talibasefname+") < wodobasefname "+ wodobasefname[:-16])
                # page_content += '<li>'+talibasefname+' (<a href="'+config.CONTEXT+'/create'+talireldir+'/'+talibasefname+'">new workdown</a>)</li>'
                page_content += '<li>'+talibasefname+' <button type="submit" formaction="'+config.CONTEXT+'/create'+talireldir+'/'+talibasefname+'">new workdown</button></li>'
                tali_i += 1
                talibasefilename = ""
                if tali_i < len(talifilenames):
                    talibasefname = os.path.splitext(talifilenames[tali_i])[0]
            elif talibasefname == wodobasefname[:-16]:
                print("      talibasefname ("+talibasefname+") == wodobasefname ("+ wodobasefname[:-16]+")")
                # page_content += '<li>'+talibasefname+' (<a href="'+config.CONTEXT+'/create'+talireldir+'/'+talibasefname+'">new workdown</a>)</li>'
                page_content += '<li>'+talibasefname+' <button type="submit" formaction="'+config.CONTEXT+'/create'+talireldir+'/'+talibasefname+'">new workdown</button></li>'
                page_content += "<ol>"
                while wodobasefname != "" and talibasefname == wodobasefname[:-16]:
                    page_content += '<li><a href="'+config.CONTEXT+'/render'+talireldir+'/'+wodobasefname+'">'+wodobasefname+'</a></li>'
                    wodo_i += 1
                    wodobasefname = ""
                    if wodo_i < len(wodofilenames):
                        wodobasefname = os.path.splitext(wodofilenames[wodo_i])[0]
                page_content += "</ol>"
                tali_i += 1
                talibasefilename = ""
                if tali_i < len(talifilenames):
                    talibasefname = os.path.splitext(talifilenames[tali_i])[0]
            elif talibasefname > wodobasefname[:-16] or talibasefname == "":
                print("      talibasefname ("+talibasefname+") > wodobasefname ("+ wodobasefname[:-16]+")")
                placeholdertalibasefname = wodobasefname[:-16]
                page_content += '<li>'+wodobasefname[:-16]+'</li>'
                page_content += "<ol>"
                while wodobasefname != "" and placeholdertalibasefname == wodobasefname[:-16]:
                    page_content += '<li><a href="'+config.CONTEXT+'/render'+talireldir+'/'+wodobasefname+'">'+wodobasefname+'</a></li>'
                    wodo_i += 1
                    wodobasefname = ""
                    if wodo_i < len(wodofilenames):
                        wodobasefname = os.path.splitext(wodofilenames[wodo_i])[0]
                page_content += "</ol>"
        # for talifilename in talifilenames:
            # talibasefname = os.path.splitext(talifilename)[0]
            # page_content += '<li><a href="'+config.CONTEXT+'/render'+talireldir+'/'+talibasefname+'">'+talibasefname+'</a></li>'
        page_content += "</ol>"
        page_content += "</form>"
    page_content += '</body>'

    return page_content
