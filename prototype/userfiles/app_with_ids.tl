#
# Test an app
#

ID: create
A: sudo ubos-admin createsite
   Specify * as the site, $app as the app, and fill out the rest of the questions
O: UBOS thinks for a while, prints a URL (note as URL) and returns to shell prompt

# check site in list
ID: list
A: ubos-admin listsites
# don't need sudo for this ubos-admin call
O: prints out the site you just created

ID: Tammy's addition
A: try out $app and see if you like it

ID: app
A: With a web browser, visit URL
O: The app's front page comes up

A: Log into the app with admin/admin
O: Login successful

A: sudo ubos-admin undeploy -a
O: UBOS thinks for a while, returns to shell prompt

ID: listagain
A: ubos-admin listsites
O: the site is not printed any more
