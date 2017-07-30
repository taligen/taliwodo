#
# Full test plan for a particular device
#

call inc.boot()
call inc.login()
call inc.daemons()
call inc.networking()
call inc.app( app=wordpress )
call inc.app( app=nextcloud )
call inc.backup()
call inc.upgrade()
