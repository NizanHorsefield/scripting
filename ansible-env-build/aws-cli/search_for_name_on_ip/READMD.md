#return Name tag of EC2 based on IP

##One scripts in this folder:

###./get_instance_name_from_ip.sh

This script uses a predefined list of IP address and ec2 describe-instances to return the Name tag, and outputs to a file

It expects the list of IPs to be in a file called list, within the same folder. 