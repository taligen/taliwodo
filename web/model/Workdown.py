#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import config
import datetime
import json
import os.path

from model.CheckboxStep import CheckboxStep
from model.HeaderStep import HeaderStep

class Workdown:
    """
    Represents a Workdown
    """
    def __init__( self, tl_id, wodo_id, loaded_from, json_data, is_modified = False ):
        self.tl_id          = tl_id
        self.wodo_id        = wodo_id
        self.loaded_from    = loaded_from
        self.json_data      = json_data
        self.is_modified    = is_modified
        self.lastupdated    = json_data['lastupdated']
        self.steps          = None # Allocated on demand
        self.checkbox_steps = None # Allocated on demand


    def get_tl_id( self ):
        return self.tl_id


    def get_wodo_id( self ):
        return self.wodo_id


    def get_name( self ):
        steps = self.get_steps()
        if len( steps ) > 0 :
            return steps[0].get_name()
        else:
            return self.id


    def get_created( self ):
        return self.json_data['created']


    def get_lastupdated( self ):
        return self.lastupdated


    def get_parameters( self ):
        return self.json_data['parameters']


    def get_steps( self ):
        if self.steps == None:
            self.steps = []
            if 'steps' in self.json_data:
                for json_step in self.json_data['steps']:
                    step = self._instantiateJsonStep( json_step )
                    if step:
                        self.steps.append( step )
        return self.steps


    def get_checkbox_steps( self ):
        if self.checkbox_steps == None:
            steps = self.get_steps()
            self.checkbox_steps = list( filter( lambda s: s.showCheckboxes(), steps ))
        return self.checkbox_steps


    def calc_checkbox_steps_stats( self ):
        ret = {
            'Total'     : 0,
            'Completed' : 0
        }
        for value in CheckboxStep.Status:
            ret[value.value] = 0

        steps = self.get_checkbox_steps()
        for step in steps:
            ret[step.status.value] += 1
            ret['Total'] += 1

        ret['Completed'] = ret['Passed'] + ret['Failed'] + ret['Skipped']

        return ret


    def get_step_by_id( self, step_id ):
        steps = self.get_steps()
        for step in steps:
            if step_id == step.get_id() :
                return step
        return None

    def set_is_modified( self, timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")):
        self.lastupdated = timestamp
        self.is_modified = True

    def saveIfNeeded( self ):
        if self.is_modified:
            # regenerate JSON
            json_data = {
                'template'    : self.json_data['template'],
                'parameters'  : self.json_data['parameters'],
                'name'        : self.json_data['name'],
                'created'     : self.json_data['created'],
                'lastupdated' : self.lastupdated,
                'steps'       : []
            }
            steps = self.get_steps()
            for step in steps:
                json_data['steps'].append( step.as_json() )

            self.json_data = json_data

            # save
            parentDir = os.path.dirname( self.loaded_from )
            if not os.path.isdir( parentDir ):
                os.makedirs( parentDir )

            with open( self.loaded_from, 'w' ) as wodo_fh:
                json.dump( self.json_data, wodo_fh, indent=2 )


    def toUrl( self ):
        return '/wodo/' + self.tl_id + '/' + self.wodo_id


    def delete( self ):
        """
        Delete this Workdown
        """
        os.remove( self.loaded_from )


    def _instantiateJsonStep( self, json_step ):
        """
        Helper factory method to convert a step in the JSON into the right
        instance of Step. Returns None if it cannot be instantiated.
        """
        ret = None
        if 'id' in json_step and 'type' in json_step and 'content' in json_step:
            if json_step['type'] in ( 'a', 'o' ):
                if 'lastupdated' in json_step:
                    lastupdated = json_step['lastupdated']
                else:
                    lastupdated = None

                if 'status' in json_step:
                    status = CheckboxStep.Status.fromString( json_step['status'] )
                else:
                    status = CheckboxStep.Status.NOT_DONE

                ret = CheckboxStep( self, json_step['id'], json_step['type'], json_step['content'], lastupdated, status )

            elif json_step['type'] in ( 'h' ):
                ret = HeaderStep( self, json_step['id'], json_step['type'], json_step['content'] )

        if ret:
            if 'source_file' in json_step and 'source_line' in json_step:
                ret.set_source_location( json_step['source_file'], json_step['source_line'] )

        return ret


    @staticmethod
    def loadIfExists( tl_id, wodo_id ):
        """
        Factory method: create this Workdown by loading from a file,
        or return None if does not exist
        """
        wodo_file = Workdown.filenameFromId( tl_id, wodo_id )

        if not os.path.isfile( wodo_file ):
            return None

        with open( wodo_file ) as wodo_fh:
            json_data = json.load( wodo_fh )

        return Workdown( tl_id, wodo_id, wodo_file, json_data )


    @staticmethod
    def loadFromUrlIfExists( path ):
        """
        Factory method: create this Workdown by loading from a URL
        (relative to the context path) or return None if does not exist
        """
        ids = Workdown.idFromUrl( path )
        if( ids == None ):
            return None

        ( tl_id, wodo_id ) = ids
        return Workdown.loadIfExists( tl_id, wodo_id )


    @staticmethod
    def loadAll() :
        """
        Mass factory method: returns a dict() of dict() of all Workdowns that
        can be found, first keyed by TaskList id, then by Workdown id
        """

        def tlDirFilt(d):
            if not os.path.isdir( config.WODODIR + '/' + d ):
                return False
            return True

        ret = {}
        for tl_id in filter( tlDirFilt, os.listdir( config.WODODIR )):

            def wodoFilt(c):
                if not os.path.isfile( config.WODODIR + '/' + tl_id + '/' + c ):
                    return False
                if not c.endswith( '.wodo-json' ):
                    return False
                return True

            for wodo_id in map( lambda f: f[ : -len('.wodo-json') ], filter( wodoFilt, os.listdir( config.WODODIR + '/' + tl_id ))) :
                wodo = Workdown.loadIfExists( tl_id, wodo_id )
                if not tl_id in ret:
                    ret[ tl_id ] = {}
                ret[ tl_id ][ wodo_id ] = wodo

        return ret

    @staticmethod
    def filenameFromId( tl_id, wodo_id ):
        """
        The mapping from Workdown id to the location of the Workdown
        JSON file in the filesystem
        """
        wodo_file  = config.WODODIR + '/' + tl_id + '/' + wodo_id + '.wodo-json'
        return wodo_file


    @staticmethod
    def idFromUrl( path ):
        """
        The mapping from URL space (relative to the app's context path)
        to the Workdown id, or None if it isn't.
        """
        try:
            ( prefix, tl_id, wodo_id ) = path[1:].split( '/', 2 )

            if prefix == 'wodo' and wodo_id:
                return ( tl_id, wodo_id )
        except ValueError:
            pass # Not enough / in the path

        return None


