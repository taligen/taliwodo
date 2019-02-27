

import datetime
from enum import Enum
from model.Step import Step

class CheckboxStep(Step):
    class Status(Enum):
        NOT_DONE = 'NotDone'
        STARTED  = 'Started'
        PASSED   = 'Passed'
        FAILED   = 'Failed'
        SKIPPED  = 'Skipped'

        def __str__(self):
            return str(self.value)


        def fromString( s ):
            s = s.lower()
            if s == CheckboxStep.Status.NOT_DONE.value.lower():
                return CheckboxStep.Status.NOT_DONE
            if s == CheckboxStep.Status.STARTED.value.lower():
                return CheckboxStep.Status.STARTED
            if s == CheckboxStep.Status.PASSED.value.lower():
                return CheckboxStep.Status.PASSED
            if s == CheckboxStep.Status.FAILED.value.lower():
                return CheckboxStep.Status.FAILED
            if s == CheckboxStep.Status.SKIPPED.value.lower():
                return CheckboxStep.Status.SKIPPED
            return None


    def __init__( self, wodo, step_id, step_type, content, lastupdated, status = Status.NOT_DONE ) :
        super().__init__( wodo, step_id, step_type, content )

        self.lastupdated = lastupdated
        self.status      = status


    def get_lastupdated( self ):
        return self.lastupdated


    def get_status( self ):
        return self.status


    def set_status( self, status ):
        status = status.lower()

        if status == 'started':
            status = CheckboxStep.Status.STARTED

        elif status == 'passed':
            status = CheckboxStep.Status.PASSED

        elif status == 'failed':
            status = CheckboxStep.Status.FAILED

        elif status == 'skipped':
            status = CheckboxStep.Status.SKIPPED

        if status != self.status:
            now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

            self.status      = status
            self.lastupdated = now
            self.wodo.set_is_modified( now )


    def showCheckboxes( self ):
        return True


    def as_json( self ):
        ret = super().as_json()

        if self.status:
            ret['status'] = str(self.status)
        if self.lastupdated:
            ret['lastupdated'] = self.lastupdated

        return ret
