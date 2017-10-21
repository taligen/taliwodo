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
      body= environ['wsgi.input'].read(length).decode('utf-8')
  # postlist = parse_qs(body)
  # postlist = json.loads(body)
  postlist = key_value_array_to_dict(json.loads(body))
  
  # print("update body is "+body+" and postilst is "+str(postlist) + " content type is "+environ.get('CONTENT_TYPE', 'NA'))
  # for k in body:
  #    print("   body.get("+k+") is "+str(body.get(k), "NA"))
  
  json_file = config.WODODIR+"/"+tlId+".json"
  
  print("Updating workdown "+tlId+" with "+str(postlist)+" filename is "+json_file)
  
  tasklist = "{}"
  with open(json_file) as json_data:
      tasklist = json.load(json_data)

  tasklist["workdown_last_updated"] = datetime.datetime.now().strftime('%Y/%m/%d %H-%M-%S')

  tasklist = update_tasklist(tasklist, postlist)
  tasklist = count_results(tasklist)
  
  with open(json_file, "w") as jofile:
      json.dump(tasklist, jofile, indent=4)
      
  # msg += '<p>body: ' + str(postlist) + '</p>'
  # print ('postlist: ' + str(postlist))

  start_response('303 See Other', [('Location',config.CONTEXT+'/render/'+tlId)])

  return [b'1']
  
  
def key_value_array_to_dict(input_data):
    parsed_dict = {}
    for sub_dict in input_data:
        key = sub_dict[ "name" ]
        value = sub_dict[ "value" ]
        if key in parsed_dict:
            parsed_dict[ key ].append( value )
        else:
            parsed_dict[ key ] = [ value ]
    return parsed_dict
  
  
def count_results(tasklist):
    counts = {"step_count":0, "pass_count":0, "fail_count":0, "not_done_count":0}
    
    counts = count_step_results(tasklist["steps"], counts)
    
    for count in counts:
        tasklist[count] = counts[count]
    
    return tasklist
    
    
def count_step_results(steps, counts):
    for step in steps:
        if "a" in step:
            counts["step_count"] += 1
            if "result" in step["a"]:
                counts = add_result(step["a"]["result"], counts)
        if "o" in step:
            counts["step_count"] += 1
            if "result" in step["o"]:
                counts = add_result(step["o"]["result"], counts)
        if "call" in step:
            counts = count_step_results(step["steps"], counts)
    return counts
    
    
def add_result(result, counts):
    results_to_countnames = {'passed': "pass_count", 'failed': "fail_count", "not done": "not_done_count"}
    countname = results_to_countnames.get(result, 'unknown')
    counts[countname] = 1 + counts.get(countname, 0)
    return counts


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


