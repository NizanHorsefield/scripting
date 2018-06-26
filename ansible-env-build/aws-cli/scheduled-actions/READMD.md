#set, delete ASG scheduled acctions

##Two scripts in this folder:

###./set_asg_scheduled_action.sh

This scripts creates ASG scheduled actions for peak times.

It searches for all of the ASGs based the user's choice then runs 'put-scheduled-update-group-action' on them.

###./delete_asg_scheduled_action.sh

This scripts creates ASG scheduled actions for off-peak times.

It searches for all of the ASGs based the user's choice then runs 'delete-scheduled-action' on them. 

##USAGE:
./set_asg_scheduled_action.sh

##EXAMPLE:
./delete_asg_scheduled_action.sh

### Menu:
1) dev
2) dev2
3) sit1
4) sit2
5) cert
6) quit
Please choose the environment you wish to change: