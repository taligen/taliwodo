#!/usr/bin/python
#
# Copyright (C) 2017 and later, taligen project.
# All rights reserved. License: see package.
#

import abc
import config
import datetime
import json
import os
from model.Workdown import Workdown

class TaskList:
    """
    Represents a TaskList
    """
    def __init__( self, tl_id, loaded_from, lastupdated, json_data ):
        self.id          = tl_id
        self.loaded_from = loaded_from
        self.lastupdated = lastupdated
        self.json_data   = json_data


    def get_id( self ):
        return self.id


    def get_name( self ):
        """
        Its name is the name of the first item.
        """
        if 'name' in self.json_data:
            return self.json_data['name']
        else:
            return self.id


    def get_lastupdated( self ):
        return self.lastupdated


    def get_parameters( self ):
        return self.json_data['parameters']


    def loadIfExists( tl_id ):
        """
        Factory method: create this TaskList by loading from a file,
        or return None if does not exist
        """
        tl_file = TaskList.filenameFromId( tl_id )

        if not os.path.isfile( tl_file ):
            return None

        lastupdated = os.path.getmtime( tl_file )
        lastupdated = datetime.datetime.utcfromtimestamp( lastupdated ).strftime("%Y%m%d-%H%M%S")

        with open( tl_file ) as tl_fh:
            json_data = json.load( tl_fh )

        return TaskList( tl_id, tl_file, lastupdated, json_data )


    def loadFromUrlIfExists( path ):
        """
        Factory method: create this TaskList by loading from a URL
        (relative to the context path) or return None if does not exist
        """
        tl_id = TaskList.idFromUrl( path )
        if tl_id :
            return TaskList.loadIfExists( tl_id )
        else:
            return None


    def loadAll() :
        """
        Mass factory method: returns a dict() of all TaskLists that can
        be found, keyed by tl_id
        """

        def tlFilt(c):
            if not os.path.isfile( config.TALIDIR + '/' + c ):
                return False
            if not c.endswith( '.tl-json' ):
                return False
            return True

        ret = {}
        for tl_id in map( lambda f: f[ : -len('.lt-json') ], filter( tlFilt, os.listdir( config.TALIDIR ))) :
            tl = TaskList.loadIfExists( tl_id )
            ret[tl_id] = tl

        return ret


    def createWorkdown( self ):
        wodo_id = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        wodo_file = Workdown.filenameFromId( self.id, wodo_id )
        wodo_json = dict( self.json_data )

        wodo_json['created']     = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        wodo_json['lastupdated'] = wodo_json['created']

        wodo = Workdown( self.id, wodo_id, wodo_file, wodo_json, True )
        wodo.saveIfNeeded()
        return wodo


    def delete( self ):
        """
        Delete this TaskList
        """
        os.remove( self.loaded_from )


    def filenameFromId( tlId ):
        """
        The mapping from TaskList id to the location of the TaskList
        JSON file in the filesystem
        """
        tlFile  = config.TALIDIR + '/' + tlId + '.tl-json'
        return tlFile

    def idFromUrl( path ):
        """
        The mapping from URL space (relative to the app's context path)
        to the TaskList id, or None if it isn't.
        """
        if path.startswith( '/tl/' ):
            return path[ len( '/tl/' ) : ]
        else:
            return None

    def toUrl( self ):
        return '/tl/' + self.id
