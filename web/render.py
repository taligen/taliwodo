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
import error

def doIt( tlId, environ, start_response ) :
    response_headers = [('Content-type','text/html; charset=utf-8')]
    filename = config.WODODIR+"/"+tlId+".json"
    
    if not os.path.isfile(filename):
        start_response( '404 Not Found', response_headers)
        # content = error.doIt( '404 Not Found', environ, start_response )
        # content += "<p>File not found: " + environ['PATH_INFO'] + "</p>\n"
        content = "<p>File not found: " + environ['PATH_INFO'] + "</p>\n"
        return content
        
    start_response( '200 OK', response_headers)
  
    # msg = 'This is the render page: tlId=' + tlId + ' dir is '+ config.TALIDIR
    msg = generate_html_from_json(tlId, filename).encode('utf-8')
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
    html_body += generate_menubar()
    html_body += generate_html_form(tlId, filename, d)
    html_body += '</body>\n'
    return html_body
    
def generate_menubar():
    html_menubar = '<a href="'+config.CONTEXT+'/">Taliwodo</a>\n'
    return html_menubar

def generate_html_form(tlId, filename, d):
    html_form = '<form id="tasklist_form" action="'+config.CONTEXT+'/render/'+tlId+'" method="post">\n'
    html_form += '<script> function sendUpdate(button_name) {\n'
    html_form += 'document.getElementById("button_changed").value = button_name;\n'
    html_form += 'document.getElementById("tasklist_form").submit();\n'
    html_form += '}\n'
    html_form += '</script>\n'
    html_form += '<h1>'+tlId+'</h1>\n'
    # html_form += '<div style="width: 400px; height: 30px;"><div class="pass" style="width: 20%; height: 100%;"></div></div>'
    html_form += '<table class="context">'
    html_form += '<tr><td>TL name</td><td>'+str(d.get("name", "&mdash;"))+'</td></tr>\n'
    html_form += '<tr><td>Generated</td><td>'+d.get("generated", "&mdash;")+'</td></tr>\n'
    html_form += '<tr><td>Workdown Created</td><td>'+d.get("workdown_created", "&mdash;")+'</td></tr>\n'
    html_form += '<tr><td>Last Updated</td><td>'+d.get("workdown_last_updated", "&mdash;")+'</td></tr>\n'
    plist = generate_parameter_list(d.get("parameters", {}))
    html_form += '<tr><td>Parameters</td><td>'+ plist +'</td></tr>\n'
    html_form += '<tr><td>Steps Count</td><td>'+str(d.get("step_count", "&mdash;"))+'</td></tr>\n'
    html_form += generate_result_count_row("Passed", "pass", "pass_count", d)
    html_form += generate_result_count_row("Failed", "fail", "fail_count", d)
    html_form += generate_result_count_row("Not Done", "not_done", "not_done_count", d)
    # html_form += '<tr><td>Steps Passed Count</td><td class="pass">'+str(d.get("pass_count", "&mdash;"))+'</td></tr>\n'
    # html_form += '<tr><td>% Steps Passed</td><td class="pass">'+str(100*d.get("pass_count", 0)/d.get("step_count", 1))+'%</td></tr>\n'
    # html_form += '<tr><td>Steps Failed Count</td><td class="fail">'+str(d.get("fail_count", "&mdash;"))+'</td></tr>\n'
    # html_form += '<tr><td>% Steps Failed</td><td class="fail">'+str(100*d.get("fail_count", 0)/d.get("step_count", 1))+'%</td></tr>\n'
    # html_form += '<tr><td>Steps Not Done Count</td><td class="not_done">'+str(d.get("not_done_count", "&mdash;")+'</td></tr>\n'
    # html_form += '<tr><td>% Steps Not Done</td><td class="not_done">'+str(100*d.get("not_done_count", 0)/d.get("step_count", 1))+'%</td></tr>\n'
    html_form += generate_result_graphic_row(d)
    html_form += '</table>'
    html_form += '<br>\n<br>\n'
    html_form += '<input type="hidden" name="json_filename" value="' + filename + '">\n'
    html_form += '<input type="hidden" name="tl_filename" value="' + d.get("name", "&mdash;") + '">\n'
    html_form += '<input type="hidden" name="generated" value="' + d.get("generated", "&mdash;") + '">\n'
    html_form += '<input type="hidden" name="workdown_created" value="' + d.get("workdown_created", "&mdash;") + '">\n'
    html_form += '<input type="hidden" name="parameters" value="' + html_escape(plist) + '">\n'
    html_form += '<input type="hidden" name="button_changed" id="button_changed">\n'
    html_form += '<br>\n'
    html_form += generate_html_table(d.get("steps", []))
    html_form += '</form>\n'
    return html_form
    
def generate_result_count_row(result_name, class_name, count_name, workdown_data):
    html_row = '<tr><td>Steps ' + result_name + '</td>'
    html_row += '<td class="' + class_name + '">'
    html_row += str(100*workdown_data.get(count_name, 0)/workdown_data.get("step_count", 1))+'%&emsp;&emsp;'
    html_row += str(workdown_data.get(count_name, 0)) + " out of " + str(workdown_data.get("step_count", 0))
    html_row += '</td></tr>\n'
    return html_row
    
def generate_result_graphic_row(workdown_data):
    html_row = '<tr><td>Results </td>'
    html_row += '<td>'
    html_row += generate_result_graphic_div(workdown_data)
    html_row += '</td>'
    html_row += '</tr>'
    return html_row
    
def generate_result_graphic_div(workdown_data):
    html_div = '<div style="width: 100px; height: 10px; border: solid black 1px;">'
    html_div += generate_result_div("pass", "pass_count", workdown_data)
    html_div += generate_result_div("fail", "fail_count", workdown_data)
    html_div += generate_result_div("not_done", "not_done_count", workdown_data)
    html_div += '</div>'
    return html_div
	
    
def generate_result_div(class_name, count_name, workdown_data):
    html_div = '<div class="'+ class_name + '" style="width: '
    html_div += str(100*workdown_data.get(count_name, 0)/workdown_data.get("step_count", 1))
    html_div += '%; height: 100%; float: left;"></div>'
    return html_div

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
    <col class="age" />\n\
  </colgroup>\n\
<theader><tr><th>ID</th><th>Description</th><th>Pass</th><th>Fail</th><th>Not Done</th><th>Age</th></tr></theader>\n'

def generate_html_table_bodies(parent_id, steps):
    print("generate_html_table_bodies:: parent_id: "+str(parent_id)+", steps: "+str(steps))
    html_table_bodies = ""
    for step in steps:
        if "a" in step:
            html_table_bodies += generate_html_table_body(parent_id, step)
        elif "call" in step:
            html_table_bodies += generate_html_table_bodies(generate_sub_id(parent_id,step.get("id", "-")),step.get("steps", "[]"))
    print("... len(steps): " + str(len(steps)))
    if len(steps) == 0:
        html_table_bodies = '<tr><td></td><td></td><td></td><td></td><td></td><td></td></tr>'
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
    part_data = step.get(part, "{}")
    step_part_id = generate_sub_id(parent_id, step.get("id", "-")) + '.' + part
    html_table_row += '<td>' + step_part_id
    html_table_row += '</td>\n'    #id
    html_table_row += '<td>' + process_markup( part_data.get('description', "&mdash;") ) + '</td>\n'    #description
    result = step[part].get('result',"")
    html_table_row += '<td>'+generate_html_radio_button(step_part_id, "passed", result)+'</td>\n'
    html_table_row += '<td>'+generate_html_radio_button(step_part_id, "failed", result)+'</td>\n'
    html_table_row += '<td>'+generate_html_radio_button(step_part_id, "not done", result)+'</td>\n'
    html_table_row += '<td>'
    if "result_time" in part_data:
        html_table_row += str(datetime.now() - datetime.strptime(part_data["result_time"], '%Y/%m/%d %H-%M-%S')).split(".")[0]+ " ago"
    html_table_row += '</td>\n'
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
        plist = "&mdash;"
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
