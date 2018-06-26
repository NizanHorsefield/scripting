#!/usr/bin/env bash

ENVIRONMENT=performance
export EC2_INI_PATH='./inventory/config/dev1/ec2.ini'

chmod +x ./inventory/ec2.py
rm -rf .ansible
sudo rm -rf /etc/ansible/roles


eval `ssh-agent -s -t 4000`

ssh-add ~/.ssh/id_rsa

ssh-add ~/.ssh/infra-temp


echo ""
echo "Configuring software on $ENVIRONMENT environment using Ansible"
echo ""

ansible-galaxy install -r ./oem-requirements.yml

ansible-playbook \
	-e "ansible_ssh_user=ec2-user" \
	--private-key ~/.ssh/infra-temp \
	-i ./inventory/ec2.py \
	./playbooks/oem-playbook.yml


#rm ansible-ec2*
