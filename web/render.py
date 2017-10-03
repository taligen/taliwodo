#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Render a task list
#

import argparse
from datetime import datetime
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
    gen_html = generate_html_head(tlId)
    gen_html += generate_html_body(tlId, filename, d)
    return gen_html

def generate_html_head(tlId):
    return '<!DOCTYPE html>\n\
\n\
<html lang="en-US">\n\
    <head>\n\
        <title>'+tlId+'</title>\n\
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
    html_form = '<form id="tasklist_form" action="'+config.CONTEXT+'/render/'+tlId+'" method="post">\n'
    html_form += '<script> function sendUpdate(button_name) {\n'
    html_form += 'document.getElementById("button_changed").value = button_name;\n'
    html_form += 'document.getElementById("tasklist_form").submit();\n'
    html_form += '}\n'
    html_form += '</script>\n'
    html_form += '<h1>'+tlId+'</h1>\n'
    html_form += '<table class="context">'
    html_form += '<tr><td>TL name</td><td>'+d["name"]+'</td></tr>\n'
    html_form += '<tr><td>Generated</td><td>'+d["generated"]+'</td></tr>\n'
    html_form += '<tr><td>Workdown Created</td><td>'+d["workdown_created"]+'</td></tr>\n'
    # workdown_time = datetime.strptime(d["workdown_created"], '%Y/%m/%d %H-%M-%S')
    plist = generate_parameter_list(d["parameters"])
    html_form += '<tr><td>Parameters</td><td>'+ plist +'</td></tr>\n'
    html_form += '</table>'
    html_form += '<br>\n<br>\n'
    html_form += '<input type="hidden" name="json_filename" value="' + filename + '">\n'
    html_form += '<input type="hidden" name="tl_filename" value="' + d.get("name", "") + '">\n'
    html_form += '<input type="hidden" name="generated" value="' + d["generated"] + '">\n'
    html_form += '<input type="hidden" name="workdown_created" value="' + d["workdown_created"] + '">\n'
    html_form += '<input type="hidden" name="parameters" value="' + html_escape(plist) + '">\n'
    html_form += '<input type="hidden" name="button_changed" id="button_changed">\n'
    html_form += '<br>\n'
    html_form += generate_html_table(d["steps"])
    html_form += '<br>\n'
    html_form += '<input type="submit" value="Submit">\n'
    html_form += '</form>\n'
    return html_form

def generate_html_table(steps):
    html_table = '<table class="steps">\n'
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
<theader><tr><th>ID</th><th>Description</th><th>Pass</th><th>Fail</th><th>Not Done</th></tr></theader>\n'

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
    html_table_row += '<td>' + step_part_id
    if "result_time" in step[part]:
         html_table_row += '&emsp;&emsp;<span class="timespan">(' + str(datetime.now() - datetime.strptime(step[part]["result_time"], '%Y/%m/%d %H-%M-%S')).split(".")[0] + ')</span>'
    html_table_row += '</td>\n'    #id
    html_table_row += '<td>' + process_markup( step[part]['description'] ) + '</td>\n'    #description
    result = step[part].get('result',"")
    html_table_row += '<td>'+generate_html_radio_button(step_part_id, "passed", result)+'</td>\n'
    html_table_row += '<td>'+generate_html_radio_button(step_part_id, "failed", result)+'</td>\n'
    html_table_row += '<td>'+generate_html_radio_button(step_part_id, "not done", result)+'</td>\n'
    html_table_row += '</tr>\n'
    return html_table_row
    
def generate_html_radio_button(step_part_id, value, result):
    html_radio_button = '<input type="radio" onChange="sendUpdate(this.name);" name="result'+ step_part_id + '" value="'+value+'" '
    if value == result:
        html_radio_button += 'checked="checked"'
    html_radio_button += '>'
    # print ("html_radio_button: " + html_radio_button + ", result:" + result)
    html_radio_button += '<input type="hidden" name="result'+step_part_id+'_timestamp">'
    return html_radio_button

def generate_parameter_list(parameters):
    plist = ""
    for key, value in parameters.iteritems():
        plist += '"' + key + '": "' + value + '", '
    if plist != "":
        plist = plist[:-2]
    else:
        plist = "-"
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
