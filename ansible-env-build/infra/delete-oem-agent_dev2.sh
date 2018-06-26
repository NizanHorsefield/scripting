#!/usr/bin/env bash

ENVIRONMENT=performance
export EC2_INI_PATH='./inventory/config/dev2/ec2.ini'

chmod +x ./inventory/ec2.py

eval `ssh-agent -s -t 4000`

ssh-add ~/.ssh/id_rsa

ssh-add ~/.ssh/infra-temp


echo ""
echo "Configuring software on $ENVIRONMENT environment using Ansible"
echo ""


ansible-playbook \
	-e "ansible_ssh_user=ec2-user" \
	--private-key ~/.ssh/infra-temp \
	-i ./inventory/ec2.py \
	./delete-agent-playbook.yml


#rm ansible-ec2*
