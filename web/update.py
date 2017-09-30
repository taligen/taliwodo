#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import json
import os
from cgi import parse_qs, escape
import datetime
import config


def doIt( tlId, environ, start_response ) :
  response_headers = [('Content-type','text/html')]
  start_response( '200 OK', response_headers)

  # msg = '<p>This is the update page, tlId=' + tlId + '</p>'
  # msg += '<p>environ: ' + str(environ) + '</p>'
  # msg += '<p>start_response: ' + str(start_response) + '</p>'
  
  body= ''  # b'' for consistency on Python 3.0
  try:
      length= int(environ.get('CONTENT_LENGTH', '0'))
  except ValueError:
      length= 0
  if length!=0:
      body= environ['wsgi.input'].read(length)
  postlist = parse_qs(body)
  
  json_file = config.WODODIR+"/"+tlId+".json"
  
  print("Updating workdown "+tlId+" with "+str(postlist)+" filename is "+json_file)
  
  tasklist = "{}"
  with open(json_file) as json_data:
      tasklist = json.load(json_data)
      
  tasklist = update_tasklist(tasklist, postlist)
  
  with open(json_file, "w") as jofile:
      json.dump(tasklist, jofile, indent=4)
      
  # msg += '<p>body: ' + str(postlist) + '</p>'
  # print ('postlist: ' + str(postlist))

  start_response('303 See Other', [('Location',config.CONTEXT+'/render/'+tlId)])

  return ['1']


def update_tasklist(tasklist, postlist):
    tasklist["updated"] = str(datetime.datetime.now())

    tasklist["steps"] = update_steps("", tasklist["steps"], postlist)
    
    # print(str(tasklist))

    return tasklist

def update_steps(parent_id, steps, postlist):
    # print("  parent: "+ parent_id)
    for step in steps:
        # print("    step: "+ step["id"])
        for part in step:
            if parent_id == "":
                resultid = "result"+step["id"]+"."+part
            else:
                resultid = "result"+parent_id+"."+step["id"]+"."+part
            # print("    looking for: "+ resultid)
            if resultid in postlist:
               # print("      result: "+ postlist[resultid][0])
               step[part]["result"]= postlist[resultid][0]
            if resultid == postlist["button_changed"][0]:
               step[part]["result_time"]= datetime.datetime.now().strftime('%Y/%m/%d %H-%M-%S')
        if "call" in step:
            # print("      call: "+ parent_id+"."+step["id"])
            if parent_id == "":
                step["steps"] = update_steps(step["id"], step["steps"], postlist)
            else:
                step["steps"] = update_steps(parent_id+"."+step["id"], step["steps"], postlist)
    return steps


