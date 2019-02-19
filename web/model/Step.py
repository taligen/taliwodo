class Step:
    def __init__( self, wodo, step_id, step_type, content ) :
        self.wodo    = wodo
        self.id      = step_id
        self.type    = step_type
        self.content = content

        self.source_file = None
        self.source_line = None

    def get_id( self ):
        return self.id


    def get_name( self ):
        return None


    def get_type( self ):
        return self.type


    def get_content( self ):
        return self.content


    def set_source_location( self, source_file, source_line ):
        self.source_file = source_file
        self.source_line = source_line


    def showCheckboxes( self ):
        return False


    def as_json( self ):
        ret = {}

        if self.id:
            ret['id'] = self.id
        if self.type:
            ret['type'] = self.type
        if self.content:
            ret['content'] = self.content
        if self.source_file:
            ret['source_file'] = self.source_file
        if self.source_line:
            ret['source_file'] = self.source_line

        return ret
