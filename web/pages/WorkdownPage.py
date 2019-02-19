#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import re
from model.CheckboxStep import CheckboxStep
from pages.OkHtmlPage import OkHtmlPage

class WorkdownPage(OkHtmlPage):
    def __init__( self, environ, wodo ):
        super().__init__( environ )

        self.wodo = wodo

    def htmlTitle( self ):
        return 'Workdown ' + str( self.wodo.get_name() )

    def htmlContent( self ):

        wodo = self.wodo

        ret = f"""
<form id="workdown_form" method="post">
 <input type="hidden" name="verb" value="update">
 <input type="hidden" name="wodo_id" value="{ wodo.get_wodo_id() }">

 <table class="wodo-summary">
  <tr>
   <th>Created from task list:</th>
   <td class="tl-name">{ wodo.get_name() }</td>
   <th>Created on:</th>
   <td>{ wodo.get_created() }</td>
  </tr>
  <tr>
   <th>With parameters:</th>
   <td>
"""
        pars = wodo.get_parameters()
        if pars:
            ret += "    <ol class=\"parameters\">\n";
            for p in pars:
                ret += f"     <li>{p} = {pars[p]}</li>\n";
            ret += "    </ol>\n";

        stats = wodo.calc_checkbox_steps_stats()

        ret += f"""
   </td>
   <th>Last updated:</th>
   <td>{ wodo.get_lastupdated() }</td>
  </tr>
  <tr>
   <th>Steps:</th>
   <td colspan="3" class="wodo-progress">
    { self.sliderHtml( stats ) }
    { stats['Passed']  } passed,
    { stats['Failed']  } failed,
    { stats['Skipped'] } skipped
    (of { stats['Total'] })
   </td>
  </tr>
 </table>

 <h1>Workdown</h1>

 <table class="wodo-steps">
  <colgroup>
   <col class="id" />
   <col class="description" />
   <col class="passed" />
   <col class="failed" />
   <col class="skipped" />
   <col class="age" />
  </colgroup>
  <tr>
   <th>ID</th>
   <th>Description</th>
   <th>Pass</th>
   <th>Fail</th>
   <th>Skipped</th>
   <th>Age</th>
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
   <td>{ self.format( step.get_content()) }</td>
"""

                for value in ( CheckboxStep.Status.PASSED, CheckboxStep.Status.FAILED, CheckboxStep.Status.SKIPPED ):
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
   <td colspan="5">{ self.format( step.get_content()) }</td>
"""

            ret += f"""
  </tr>
"""

        ret += """
 </table>
</form>
"""
        return ret


    def format( self, s ):
        """
        Format a Taligen-formatted string in HTML
        """
        ret = s

        for ( key, value ) in {
                "&": "&amp;",
                '"': "&quot;",
                "'": "&apos;",
                ">": "&gt;",
                "<": "&lt;" }.items() :
            ret = ret.replace( key, value )

        ret = re.sub( '``([^`]*)``', '<pre>\\1</pre>', ret ) # Double-`` means <pre> with linebreaks
        ret = re.sub( '`([^`]*)`', '<code>\\1</code>', ret ) # Single-` means <code> without linebreaks


        return ret


    def sliderHtml( self, stats ):
        ret  = "    <div class=\"wodo-progress\">\n"
        ret += "     <div class=\"wodo-progress-passed\" style=\"width: "  + str( 100.0 * stats['Passed']  / stats['Total'] ) + "%\"></div>\n";
        ret += "     <div class=\"wodo-progress-failed\" style=\"width: "  + str( 100.0 * stats['Failed']  / stats['Total'] ) + "%\"></div>\n";
        ret += "     <div class=\"wodo-progress-skipped\" style=\"width: " + str( 100.0 * stats['Skipped'] / stats['Total'] ) + "%\"></div>\n";
        ret += "    </div>\n"
        return ret
