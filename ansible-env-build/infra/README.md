# Evise Infrastructure

This repository contains the code to instantiate non production environments for Evise. Currently this is focused on creation of the performance environment.

The software uses [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)) scripts which executes [Terraform](https://www.terraform.io) commands to build and demolish the compute in [AWS](https://aws.amazon.com/) and [Ansible](http://www.ansible.com) to install and configure the software.

There is a [Jenkins pipeline](http://perf-jenkins.evise-cloud.com:8080/view/rap-evise-oracle/) for building, testing and then demolishing the performance environment. The job and steps this software is responsible for is described in the [Jenkinsfile](Jenkinsfile).

## Dependencies

In order to build out the environment the following tools need to be installed on the build server. 

- [Terraform installation](https://www.terraform.io/intro/getting-started/install.html) (0.9.11)
- [Ansible installation](http://docs.ansible.com/ansible/latest/intro_installation.html) (latest)
- [GIT](https://about.gitlab.com/installation/) (latest)
- [boto] (https://github.com/boto/boto) (latest)

## Setup

### Terraform

```
$ wget https://releases.hashicorp.com/terraform/0.9.11/terraform_0.9.11_linux_amd64.zip
$ unzip terraform_0.9.11_linux_amd64.zip
$ sudo mv terraform /usr/bin
```
 
### Ansible

```
$ sudo apt-get install ansible
```

### GIT

```
$ sudo apt-get install git
```

### boto

```
$ sudo apt-get install python-pip
$ sudo pip install boto
```

## Terraform Modules

To maintain the integrity of the infrastructure, modules are sourced from the [TIO RAP Terraform Control repository for Evise](https://gitlab.et-scm.com/tio-rap-london/rap-terraformcontrol-evise) 

The Dev2 (performance environment) Terraform modules are held in the sub-folder [885289476053/dev2-perf/](https://gitlab.et-scm.com/tio-rap-london/rap-terraformcontrol-evise/tree/master/885289476053/dev2-perf)

### Immutable

The [immutable folder](https://gitlab.et-scm.com/tio-rap-london/rap-terraformcontrol-evise/tree/master/885289476053/dev2-perf/immutable) contains the Terraform modules for the infrastructure that is to remain up, in that there is no need to tear them down with the _demolish_ process.

#### Oracle

The [oracle folder](https://gitlab.et-scm.com/tio-rap-london/rap-terraformcontrol-evise/tree/master/885289476053/dev2-perf/oracle) contains the Terraform modules for the infrastructure that is volatile, in that they will be torn down with the _demolish_ process and created again with the _build_ process. 

