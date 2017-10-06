import os
import config
import json
import render
from datetime import datetime

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
    page_content += "<h1>Tasklists and Workdowns</h1>\n"
    print ("Overview:: TALIDIR: "+config.TALIDIR+", WODODIR: "+config.WODODIR)
    for (talidirpath, talidirnames, talifilenames) in os.walk(config.TALIDIR):
        talifilenames.sort()
        wododirpath = ""
        wododirnames = []
        wodofilenames = []
        # print ("... also looking in "+config.WODODIR+talidirpath[len(config.TALIDIR):])
        for (dirpath, dirnames, filenames) in os.walk(config.WODODIR+talidirpath[len(config.TALIDIR):]):
            wodofilenames = filenames
            wododirpath = dirpath
            wododirnames = dirnames
            break
        wodofilenames.sort()
        talireldir = talidirpath[len(config.TALIDIR):]
        page_content += "<h2>"+talireldir+"</h2>"
        page_content += '<form method="post">'
        page_content += "<ol>"
        # print ("talidirpath: " + talidirpath + ", talidirnames: " + str(talidirnames) + ", talifilenames: " + str(talifilenames))
        # print ("wododirpath: " + wododirpath + ", wododirnames: " + str(wododirnames) + ", wodofilenames: " + str(wodofilenames))
        tali_i = 0
        wodo_i = 0
        talibasefname = ""
        wodobasefname = ""
        if len(talifilenames) > 0:
            talibasefname = os.path.splitext(talifilenames[tali_i])[0]
        if len(wodofilenames) > 0:
            wodobasefname = os.path.splitext(wodofilenames[wodo_i])[0]
        # print("   talibasefiname: "+talibasefname+", wodobasefname: "+wodobasefname)
        wodonames = []
        while tali_i < len(talifilenames) or wodo_i < len(wodofilenames):
            if talibasefname < wodobasefname[:-16] or wodobasefname == "":
                # print("      talibasefname ("+talibasefname+") < wodobasefname "+ wodobasefname[:-16])
                page_content += '<li>'+talibasefname+' <button type="submit" formaction="'+config.CONTEXT+'/create'+talireldir+'/'+talibasefname+'">new workdown</button></li>'
                tali_i += 1
                talibasefilename = ""
                if tali_i < len(talifilenames):
                    talibasefname = os.path.splitext(talifilenames[tali_i])[0]
            elif talibasefname == wodobasefname[:-16]:
                # print("      talibasefname ("+talibasefname+") == wodobasefname ("+ wodobasefname[:-16]+")")
                page_content += '<li>'+talibasefname+' <button type="submit" formaction="'+config.CONTEXT+'/create'+talireldir+'/'+talibasefname+'">new workdown</button></li>'
                page_content += "<ol>"
  #              wodonames = []
  #              while wodobasefname != "" and talibasefname == wodobasefname[:-16]:
  #                  wodonames.append(wodobasefname)
  #                  wodo_i += 1
  #                  wodobasefname = ""
  #                  if wodo_i < len(wodofilenames):
  #                      wodobasefname = os.path.splitext(wodofilenames[wodo_i])[0]
  #              wodonames.sort(reverse=True)
  #              for wodoname in wodonames:
  #                  page_content += '<li><a href="'+config.CONTEXT
  #                  page_content += '/render'+talireldir+'/'+wodoname+'">'
  #                  page_content += wodoname+'</a> <button type="submit" formaction="'
  #                  page_content += config.CONTEXT+'/delete'+talireldir+'/'
  #                  page_content += wodoname+'">delete</button>&emsp;'
  #                  page_content += wodo_summary(talireldir+'/'+wodoname)+'</li>'
    
                (wodo_i, page_content) = wodo_list(talireldir, wodobasefname, talibasefname, wodofilenames, wodo_i, page_content)
                wodobasefname = ""
                if wodo_i < len(wodofilenames):
                    wodobasefname = os.path.splitext(wodofilenames[wodo_i])[0]
  
                page_content += "</ol>"
                tali_i += 1
                talibasefilename = ""
                if tali_i < len(talifilenames):
                    talibasefname = os.path.splitext(talifilenames[tali_i])[0]
            elif talibasefname > wodobasefname[:-16] or talibasefname == "":
                # print("      talibasefname ("+talibasefname+") > wodobasefname ("+ wodobasefname[:-16]+")")
                placeholdertalibasefname = wodobasefname[:-16]
                page_content += '<li>'+wodobasefname[:-16]+'</li>'
                page_content += "<ol>"
  #              while wodobasefname != "" and placeholdertalibasefname == wodobasefname[:-16]:
  #                  wodonames.append(wodobasefname)
  #                  wodo_i += 1
  #                  wodobasefname = ""
  #                  if wodo_i < len(wodofilenames):
  #                      wodobasefname = os.path.splitext(wodofilenames[wodo_i])[0]
  #              wodonames.sort(reverse=True)
  #              for wodoname in wodonames:
  #                  page_content += '<li><a href="'+config.CONTEXT+'/render'+talireldir+'/'+wodoname+'">'+wodoname+'</a>  <button type="submit" formaction="'+config.CONTEXT+'/delete'+talireldir+'/'+wodoname+'">delete</button></li>'

                (wodo_i, page_content) = wodo_list(talireldir, wodobasefname, placeholdertalibasefname, wodofilenames, wodo_i, page_content)
                wodobasefname = ""
                if wodo_i < len(wodofilenames):
                    wodobasefname = os.path.splitext(wodofilenames[wodo_i])[0]

                page_content += "</ol>"
        page_content += "</ol>"
        page_content += "</form>"
    page_content += '</body>'

    return page_content
    
    
def wodo_list(talireldir, wodobasefname, talibasefname, wodofilenames, wodo_i, page_content):
                wodonames = []
                while wodobasefname != "" and talibasefname == wodobasefname[:-16]:
                    wodonames.append(wodobasefname)
                    wodo_i += 1
                    wodobasefname = ""
                    if wodo_i < len(wodofilenames):
                        wodobasefname = os.path.splitext(wodofilenames[wodo_i])[0]
                wodonames.sort(reverse=True)
                for wodoname in wodonames:
                    page_content += '<li><a href="'+config.CONTEXT
                    page_content += '/render'+talireldir+'/'+wodoname+'">'
                    page_content += wodoname+'</a> <button type="submit" formaction="'
                    page_content += config.CONTEXT+'/delete'+talireldir+'/'
                    page_content += wodoname+'">delete</button>&emsp;'
                    page_content += wodo_summary(talireldir+'/'+wodoname)+'</li>'
                return (wodo_i, page_content)

    
def wodo_summary(wodofilename):
    with open(config.WODODIR+wodofilename+'.json') as json_data:
        workdown_data = json.load(json_data)
    summary = render.generate_result_graphic_div(workdown_data)
    # summary += "&emsp;last updated " + str(workdown_data.get("workdown_last_updated", ""))
    if "workdown_last_updated" in workdown_data:
        summary += "&emsp;"
        summary += str(datetime.now() - datetime.strptime(workdown_data.get("workdown_last_updated", ""), '%Y/%m/%d %H-%M-%S')).split(".")[0]+ " ago"
    return summary
    
    

