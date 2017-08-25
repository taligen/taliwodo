#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import json
import os
import datetime


def doIt( environ, start_response ) :
  response_headers = [('Content-type','text/html')]
  start_response( '200 OK', response_headers)

  return '<p>This is the update page</p>'

def parse_arguments():
    argparser = argparse.ArgumentParser(description="taligen: update json file from html POST")
    argparser.add_argument("json_file", type=str, help=".json (generated json task list) file to be updated")
    argparser.add_argument("post_file", type=str, help=".json file of the POST contents to update the json file with")
    return argparser.parse_args()

def update_tasklist(tasklist, postlist):
    tasklist["updated"] = str(datetime.datetime.now())

    tasklist["steps"] = update_steps("", tasklist["steps"], postlist)

    return tasklist

def update_steps(parent_id, steps, postlist):
    print("  parent: "+ parent_id)
    for step in steps:
        print("    step: "+ step["id"])
        for part in step:
            if "result"+parent_id+"."+step["id"]+"."+part in postlist:
               print("      result: "+ "result"+parent_id+"."+step["id"]+"."+part)
               step[part]["result"]= postlist["result"+parent_id+"."+step["id"]+"."+part]
        if "call" in step:
            print("      call: "+ parent_id+"."+step["id"])
            step["steps"] = update_steps(parent_id+"."+step["id"], step["steps"], postlist)
    return steps


def xxxxmain():
    args = parse_arguments()

    with open(args.json_file, "r") as jfile, open(args.post_file, "r") as pfile:
        tasklist = json.load(jfile)
        postlist = json.load(pfile)

    # resultlist = (x for x in postlist if x.startswith("result."))

    # for x in resultlist:
    #     print x + ": " + postlist[x]

    tasklist = update_tasklist(tasklist, postlist)

    with open(args.json_file+".json", "w") as jofile:
        json.dump(tasklist, jofile, indent=4)

