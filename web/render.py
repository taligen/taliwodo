#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Render a task list
#

import argparse
import json
import os
import re
import config

def doIt( tlId, environ, start_response ) :
  response_headers = [('Content-type','text/html; charset=utf-8')]
  start_response( '200 OK', response_headers)
  # msg = 'This is the render page: tlId=' + tlId + ' dir is '+ config.TALIDIR
  msg = generate_html_from_json(tlId, config.WODODIR+"/"+tlId+".json").encode('utf-8')
  return [msg]

def generate_html_from_json(tlId, filename):
    print("Rendering as html from " + filename)

    with open(filename) as json_data:
        d = json.load(json_data)
    gen_html = generate_html_head()
    gen_html += generate_html_body(tlId, filename, d)
    return gen_html

def generate_html_head():
    return '<!DOCTYPE html>\n\
\n\
<html lang="en-US">\n\
    <head>\n\
        <title>Taligen script</title>\n\
        <meta name="viewport" content="width=device-width, initial-scale=1.0">\n\
\n\
        <link rel="stylesheet" href="'+config.CONTEXT+'/css/default.css">\n\
    </head>'
    

def generate_html_body(tlId, filename, d):
    html_body = '<body>\n'
    html_body += generate_html_form(tlId, filename, d)
    html_body += '</body>\n'
    return html_body

def generate_html_form(tlId, filename, d):
    html_form = '<form action="'+config.CONTEXT+'/render/'+tlId+'" method="post">\n'
    html_form += '<h1>'+tlId+'</h1>\n'
    html_form += '<h3>TL name: '+d["name"]+'</h3>\n'
    html_form += '<h3>Generated: '+d["generated"]+'</h3>\n'
    html_form += '<h3>Workdown Created: '+d["workdown_created"]+'</h3>\n'
    plist = generate_parameter_list(d["parameters"])
    html_form += '<h3>Parameters: '+ plist +'</h3>\n'
    html_form += '<input type="hidden" name="json_filename" value="' + filename + '">\n'
    html_form += '<input type="hidden" name="tl_filename" value="' + d.get("name", "") + '">\n'
    html_form += '<input type="hidden" name="generated" value="' + d["generated"] + '">\n'
    html_form += '<input type="hidden" name="workdown_created" value="' + d["workdown_created"] + '">\n'
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
    html_table += generate_html_table_bodies(None, steps)
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
            html_table_bodies += generate_html_table_bodies(generate_sub_id(parent_id,step["id"]), step["steps"])
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
    step_part_id = generate_sub_id(parent_id, step["id"]) + '.' + part
    html_table_row += '<td>' + step_part_id + '</td>\n'    #id
    html_table_row += '<td>' + process_markup( step[part]['description'] ) + '</td>\n'    #description
    result = step[part].get('result',"")
    html_table_row += '<td>'+generate_html_radio_button(step_part_id, "passed", result)+'</td>\n'
    html_table_row += '<td>'+generate_html_radio_button(step_part_id, "failed", result)+'</td>\n'
    html_table_row += '<td>'+generate_html_radio_button(step_part_id, "not done", result)+'</td>\n'
    html_table_row += '</tr>\n'
    return html_table_row
    
def generate_html_radio_button(step_part_id, value, result):
    html_radio_button = '<input type="radio" name="result'+ step_part_id + '" value="'+value+'" '
    if value == result:
        html_radio_button += 'checked="checked"'
    html_radio_button += '>'
    # print ("html_radio_button: " + html_radio_button + ", result:" + result)
    return html_radio_button

def generate_parameter_list(parameters):
    plist = ""
    for key, value in parameters.iteritems():
        plist += '"' + key + '": "' + value + '", '
    if plist != "":
        plist = plist[:-2]
    return plist

def html_escape(text):
    html_escape_table = {
         "&": "&amp;",
         '"': "&quot;",
         "'": "&apos;",
         ">": "&gt;",
         "<": "&lt;",
         }
    return "".join(html_escape_table.get(c,c) for c in text)

def process_markup(markup):
    ret = re.sub( r'`([^`]*)`', '<code>\\1</code>', markup );
    return ret

def generate_sub_id(parent_id, local_id):
    if parent_id is None:
        ret = local_id
    else:
        ret = parent_id + '.' + local_id
    return ret
