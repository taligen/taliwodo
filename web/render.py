#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Render a task list
#

import argparse
import json
import os
import config

def doIt( tlId, environ, start_response ) :
  response_headers = [('Content-type','text/html; charset=utf-8')]
  start_response( '200 OK', response_headers)
  # msg = 'This is the render page: tlId=' + tlId + ' dir is '+ config.JSONDIR
  msg = generate_html_from_json(config.JSONDIR+"/"+tlId+".json").encode('utf-8')
  return [msg]

def generate_html_from_json(filename):
    print("generating html from " + filename)

#    gen_html = 'This is the page genereated from ' + filename
    with open(filename) as json_data:
        d = json.load(json_data)
    gen_html = generate_html_head()
    gen_html += generate_html_body(filename, d)
#    gen_html += '<body><p>This is the page generated from ' + filename + '</p>'
    return gen_html

def generate_html_head():
    return '<!DOCTYPE html>\n\
\n\
<html lang="en-US">\n\
    <head>\n\
        <title>full taligen script</title>\n\
        <meta name="viewport" content="width=device-width, initial-scale=1.0">\n\
\n\
        <link rel="stylesheet" href="'+config.CONTEXT+'/css/default.css">\n\
    </head>'
    
#        <meta charset="UTF-8">\n\


def generate_html_body(filename, d):
    html_body = '<body>\n'
    html_body += generate_html_form(filename, d)
#    html_body += '<p>In generate_html_body</p>'
    html_body += '</body>\n'
    return html_body

def generate_html_form(filename, d):
    html_form = '<form action="http://localhost:9000/taligen" method="post">\n'
    print(d["name"])
    html_form += '<h1>'+d["name"]+'</h1>\n'
    html_form += '<h3>generated: "'+d["generated"]+'"</h3>\n'
    plist = generate_parameter_list(d["parameters"])
    html_form += '<h3>parameters: '+ plist +'</h3>\n'
    html_form += '<input type="hidden" name="json_filename" value="' + filename + '">\n'
    html_form += '<input type="hidden" name="tl_filename" value="' + d.get("name", "") + '">\n'
    html_form += '<input type="hidden" name="generated" value="' + d["generated"] + '">\n'
    html_form += '<input type="hidden" name="parameters" value="' + html_escape(plist) + '">\n'
    html_form += '<br>\n'
    html_form += generate_html_table(d["steps"])
    html_form += '<br>\n'
    html_form += '<input type="submit" value="Submit">\n'
    html_form += '</form>\n'
    return html_form

def generate_html_table(steps):
    html_table = '<table>\n'
    html_table += generate_html_table_header()
    html_table += generate_html_table_bodies("", steps)
    html_table += '</table>\n'
    return html_table

def generate_html_table_header():
    return '  <colgroup>\n\
    <col class="id" />\n\
    <col class="description" />\n\
    <col class="pass" />\n\
    <col class="fail" />\n\
    <col class="not_done" />\n\
  </colgroup>\n\
<theader><tr><td>ID</td><td>Description</td><td>Pass</td><td>Fail</td><td>Not Done</td></tr></theader>\n'

def generate_html_table_bodies(parent_id, steps):
    html_table_bodies = ""
    for step in steps:
        if "a" in step:
            html_table_bodies += generate_html_table_body(parent_id, step)
        elif "call" in step:
            html_table_bodies += generate_html_table_bodies(parent_id+"."+step["id"], step["steps"])
    return html_table_bodies

def generate_html_table_body(parent_id, step):
    html_table_body = '<tbody>\n'
    html_table_body += generate_html_table_row(parent_id, step, "a")
    if "o" in step:
        html_table_body += generate_html_table_row(parent_id, step, "o")
    html_table_body += '</tbody>\n'
    return html_table_body

def generate_html_table_row(parent_id, step, part):
    html_table_row = '<tr class=' + part + '>\n'
    step_part_id = parent_id + '.' + step["id"]+ '.' + part
    html_table_row += '<td>' + step_part_id + '</td>\n'    #id
    html_table_row += '<td>' + step[part]["description"] + '</td>\n'    #description
    html_table_row += '<td><input type="radio" name="result'+ step_part_id + '" value="passed"></td>\n'
    html_table_row += '<td><input type="radio" name="result'+ step_part_id + '" value="failed"></td>\n'
    html_table_row += '<td><input type="radio" name="result'+ step_part_id + '" value="not done"></td>\n'
    html_table_row += '</tr>\n'
    return html_table_row

def generate_parameter_list(parameters):
    plist = ""
    for key, value in parameters.iteritems():
        plist += '"' + key + '": "' + value + '", '
    if plist != "":
        plist = plist[:-2]
    return plist

def parse_arguments():
    argparser = argparse.ArgumentParser(description="taligen: generate html file from json file")
    argparser.add_argument("json_file", type=str, help=".json (generated json task list) file to generate html from")
    return argparser.parse_args()

def html_escape(text):
    html_escape_table = {
         "&": "&amp;",
         '"': "&quot;",
         "'": "&apos;",
         ">": "&gt;",
         "<": "&lt;",
         }
    return "".join(html_escape_table.get(c,c) for c in text)
