#!/bin/bash
yum update -y
wget http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -ivh epel-release-6-8.noarch.rpm
sudo yum install ansible -y
mkdir /home/vagrant/work
cd /home/vagrant/work
ansible-galaxy init adf
ansible-galaxy init soa
ansible-galaxy init bpm
ansible-galaxy init ohs
ansible-galaxy init oid
ansible-galaxy init db
