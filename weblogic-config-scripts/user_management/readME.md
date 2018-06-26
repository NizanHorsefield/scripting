# Authentication Provider

The scripts in this repo create the WebLogic LDAP Authentication Provider **EIDMA**. The scripts can be run from any WebLogic installation that has access to **wlst.sh**, but this approach focuses on the use of a Docker container. 

# WLST Environment Property Files  [ENV_PROP]

Ensure sure that the environment property files have been updated with the correct passwords before executing the WLST script.

```/tmp/work/scripts/weblogic-config-scripts/user_management```

```
dev2.properties
sit2.properties
cert.properties
prod.properties
```
Update the values for *ADF_adminPassword*, *SOA_adminPassword*, *BPM_adminPassword*

# WL TYPE
There are only three: ADF, BPM and SOA. These control what values are read from the Environment Property file. The value **is case sensitive**.

# Docker

A prerequisite is the creation of the  **weblogic:10.3.6 Docker Container**. The steps on how to create this can be found here - https://gitlab.et-scm.com/tio-rap-evise/docker

Once the weblogic:10.3.6 image has been created run the following docker command to create a container that has a folder mapping to a a local clone of this repo.

```docker run -v LOCAL_GIT_CLONE_FOLDER:/tmp/work/scripts/weblogic-config-scripts -p HOST_PORT:CONTAINER_PORT -u 0 -i -t IMAGE_ID /bin/bash```

Example:
```docker run -v /tmp/work/scripts/tio-rap-evise-repo/weblogic-config-scripts:/tmp/work/scripts/weblogic-config-scripts -p 7003:7001 -u 0 -i -t bcf852afc9d0 /bin/bash```

## Script Execution
The above docker run command will drop you straight into a **bash shell** on the container. 

Execute the following:

```cd /tmp/work/scripts/weblogic-config-scripts/user_management```

The WLST script takes two parameters: **ENV_PROPERTY_FILE** and **WL_TYPE**

```/u01/oracle/weblogic/wlserver_10.3/common/bin/wlst.sh create_ldap_provider.py ENV_PROP WL_TYPE```

Example:
*```/u01/oracle/weblogic/wlserver_10.3/common/bin/wlst.sh create_ldap_provider.py dev2.properties ADF```*





