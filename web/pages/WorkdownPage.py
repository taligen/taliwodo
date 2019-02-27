#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import config
import re
from model.CheckboxStep import CheckboxStep
from pages.OkHtmlPage import OkHtmlPage
from utils import formatTaligenString

class WorkdownPage(OkHtmlPage):
    def __init__( self, environ, wodo ):
        super().__init__( environ )

        self.wodo = wodo

    def htmlTitle( self ):
        return 'Workdown ' + str( self.wodo.get_name() )

    def htmlContent( self ):

        wodo = self.wodo

        ret = f"""
<div class="nav"><a href="{ config.CONTEXT }/">Front page</a></div>
<form id="workdown_form" method="post">
 <input type="hidden" name="verb" value="update">
 <input type="hidden" name="wodo_id" value="{ wodo.get_wodo_id() }">

 <div class="wodo-summary">
  <table id="wodo-summary">
   <tr>
    <th>From task list:</th>
    <td class="tl-name">{ formatTaligenString( wodo.get_name()) }</td>
    <th>Created on:</th>
    <td>{ wodo.get_created() }</td>
   </tr>
   <tr>
    <th>With parameters:</th>
    <td>
"""
        pars = wodo.get_parameters()
        if pars:
            ret += "     <ol class=\"parameters\">\n";
            for p in pars:
                ret += f"      <li>{p} = {pars[p]}</li>\n";
            ret += "     </ol>\n";

        stats = wodo.calc_checkbox_steps_stats()

        ret += f"""
    </td>
    <th>Last updated:</th>
    <td data-lastupdated="{ wodo.get_lastupdated() }"></td>
   </tr>
   <tr>
    <th>Status:</th>
    <td colspan="3" class="wodo-progress" data-total="{ stats['Total'] }" data-passed="{ stats['Passed'] }" data-failed="{ stats['Failed'] }" data-skipped="{ stats['Skipped'] }" data-completed="{ stats['Completed'] }"></td>
   </tr>
  </table>
 </div>

 <h1>Workdown: { formatTaligenString( wodo.get_name() ) } &ndash; { wodo.get_created() }</h1>

 <table id="wodo-steps">
  <colgroup>
   <col class="id" />
   <col class="description" />
   <col class="started" />
   <col class="passed" />
   <col class="failed" />
   <col class="skipped" />
   <col class="age" />
  </colgroup>
  <tr>
   <th>ID</th>
   <th>Description</th>
   <th>Started</th>
   <th>Pass</th>
   <th>Fail</th>
   <th>Skipped</th>
   <th>When</th>
  </tr>
"""
        for step in wodo.get_steps() :
            tag = step.get_type()

            ret += f"""
  <tr class="{ tag }" id="wodo-step-status-{ step.get_id() }">
   <td><a href="#wodo-step-status-{ step.get_id() }">{ step.get_id() }</a></td>
"""

            if step.showCheckboxes() :
                lastupdated = step.get_lastupdated()
                if lastupdated == None:
                    lastupdated = '-' # empty string may not work reliable vs does not exist

                ret += f"""
   <td>{ formatTaligenString( step.get_content()) }</td>
"""

                for value in ( CheckboxStep.Status.STARTED,
                               CheckboxStep.Status.PASSED,
                               CheckboxStep.Status.FAILED,
                               CheckboxStep.Status.SKIPPED ):
                    if step.get_status().value == value.value :
                        checked = ' checked'
                    else:
                        checked = ''

                    ret += f"""
   <td>
    <input type="radio" onchange="workdownStepUpdated(this.name)" name="wodo-step-status-{ step.get_id() }" value="{value.value}"{ checked }>
   </td>
"""

                ret += f"""
   <td data-lastupdated="{ lastupdated }"></td>
"""
            else:
                ret += f"""
   <td colspan="5">{ formatTaligenString( step.get_content()) }</td>
"""

            ret += f"""
  </tr>
"""

        ret += """
 </table>
</form>
"""
        return ret
