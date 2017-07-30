#
# Test boot on EC2
#

A: Follow the EC2 instance wizard starting with URL: xxx
   Specify keypair foobar
   Start the EC2 instance
   Wait up to 5min
O: EC2 website says that the instance is up and running

A: Note IP address of instance, call it IP

A: ssh shepherd@IP -i foobar.pem

A: Wait up to 10sec
O: Login prompt on the console

