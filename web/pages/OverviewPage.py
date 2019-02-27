#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import config

from pages.OkHtmlPage import OkHtmlPage
from model.TaskList import TaskList
from model.Workdown import Workdown
import datetime
from utils import formatTaligenString

class OverviewPage(OkHtmlPage):

    def htmlTitle( self ):
        return 'Overview'

    def htmlContent( self ):
        tls   = TaskList.loadAll()
        wodos = Workdown.loadAll()

        # We add empty values for TaskList ids into tls that have
        # Wodos, but whose TaskLists don't exist any more
        for wodo_tl_id in wodos:
            if not wodo_tl_id in tls:
                tls[ wodo_tl_id ] = None


        ret = """
<h1>Tasklists and Workdowns</h1>

<table class="overview">
 <thead>
  <tr>
   <th class="tasklist">Task List</th>
   <th class="workdown">Workdown</th>
   <th>Status</th>
  </tr>
 </thead>
 <tbody>
"""

        def tlOrder(tlIndex):
            tl = tls[tlIndex]
            if tl:
                return tl.get_lastupdated()
            else:
                return ''

        for haveTl in [ 1, 0 ]: # first the Tls we have, then Wodos withoutu Tls

            for tl_id in sorted( tls, reverse=True, key=tlOrder ):
                tl = tls[ tl_id ]

                if ( haveTl == 1 and tl ) or ( haveTl == 0 and not tl ) :
                    if tl_id in wodos:
                        wodos_for_tl = wodos[ tl_id ]
                    else:
                        wodos_for_tl = dict()

                    if len(wodos_for_tl) > 1:
                        span = ' rowspan="' + str( len( wodos_for_tl )) + '"'
                    else:
                        span = ''

                    ret += f"""
  <tr>
   <td{ span }>
"""
                    if tl:
                        ret += f"""
    <div class="slide-in">
     <form method="post" action="{ config.CONTEXT + tl.toUrl() }">
      <input type="hidden" name="verb" value="createworkdown">
      <button type="submit">new workdown</button>
     </form>
    </div>
    <h2 class="tasklist">{ formatTaligenString( tl.get_name() ) }</h2>
"""
                        pars = tl.get_parameters()
                        if pars:
                            ret += "     <ol class=\"parameters\">\n";
                            for p in pars:
                                ret += f"      <li>{p} = {pars[p]}</li>\n";
                            ret += "     </ol>\n";

                    else:
                        ret += "Not available any more"

                    ret += f"""
   </td>
"""
                    if wodos_for_tl:
                        sep = ''
                        for wodo_id in sorted( wodos_for_tl, reverse=True, key = lambda i : wodos_for_tl[i].get_lastupdated() ):

                            wodo  = wodos_for_tl[ wodo_id ]
                            stats = wodo.calc_checkbox_steps_stats()

                            ret += sep
                            ret += f"""
   <td>
    <div class="slide-in">
     <form method="post" action="{ config.CONTEXT + wodo.toUrl() }">
      <input type="hidden" name="verb" value="deleteworkdown">
      <button type="submit">delete</button>
     </form>
    </div>
    <h2><a href="{ config.CONTEXT + wodo.toUrl() }">{wodo.get_created()}</a></h2>
   </td>
   <td class="wodo-progress" data-total="{ stats['Total'] }" data-passed="{ stats['Passed'] }" data-failed="{ stats['Failed'] }" data-skipped="{ stats['Skipped'] }" data-completed="{ stats['Completed'] }"></td>
   </td>
"""
                            sep = """
  </tr>
  <tr>
"""

                    else:
                        ret += f"""
   <td>&ndash;</td>
   <td>&ndash;</td>
"""
                ret += """
  </tr>
"""

        ret += """
 </tbody>
</table>
"""
        return ret
