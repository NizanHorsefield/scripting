import re
import os
import pdb

connect(userConfigFile='<%= @user_config_file %>', userKeyFile='<%= @user_key_file %>', url='t3://<%= @admin_address %>:<%= @admin_port %>')

edit()
startEdit()

editService.getConfigurationManager().removeReferencesToBean(getMBean('/Machines/LocalMachine'))
cmo.destroyMachine(getMBean('/Machines/LocalMachine'))

cd('/JDBCSystemResources/AuditDataSource/JDBCResource/AuditDataSource/JDBCConnectionPoolParams/AuditDataSource')
cmo.setMaxCapacity(30)
cmo.setMinCapacity(5)
cmo.setInitialCapacity(5)

cd('/JDBCSystemResources/EDNDataSource/JDBCResource/EDNDataSource/JDBCConnectionPoolParams/EDNDataSource')
cmo.setMaxCapacity(50)
cmo.setMinCapacity(5)
cmo.setInitialCapacity(5)

cd('/JDBCSystemResources/EDNLocalTxDataSource/JDBCResource/EDNLocalTxDataSource/JDBCConnectionPoolParams/EDNLocalTxDataSource')
cmo.setMaxCapacity(50)
cmo.setMinCapacity(5)
cmo.setInitialCapacity(5)

cd('/JDBCSystemResources/JMSDataSource/JDBCResource/JMSDataSource/JDBCConnectionPoolParams/JMSDataSource')
cmo.setMaxCapacity(200)
cmo.setMinCapacity(20)
cmo.setInitialCapacity(20)

cd('/JDBCSystemResources/mds-owsm/JDBCResource/mds-owsm/JDBCConnectionPoolParams/mds-owsm')
cmo.setMaxCapacity(100)
cmo.setMinCapacity(5)
cmo.setInitialCapacity(5)

cd('/JDBCSystemResources/mds-soa/JDBCResource/mds-soa/JDBCConnectionPoolParams/mds-soa')
cmo.setMaxCapacity(100)
cmo.setMinCapacity(5)
cmo.setInitialCapacity(5)

cd('/JDBCSystemResources/opssDataSource/JDBCResource/opssDataSource/JDBCConnectionPoolParams/opssDataSource')
cmo.setMaxCapacity(20)
cmo.setMinCapacity(5)
cmo.setInitialCapacity(5)

cd('/JDBCSystemResources/OraSDPMDataSource/JDBCResource/OraSDPMDataSource/JDBCConnectionPoolParams/OraSDPMDataSource')
cmo.setMaxCapacity(200)
cmo.setMinCapacity(20)
cmo.setInitialCapacity(20)

cd('/JDBCSystemResources/SOADataSource/JDBCResource/SOADataSource/JDBCConnectionPoolParams/SOADataSource')
cmo.setMaxCapacity(200)
cmo.setMinCapacity(50)
cmo.setInitialCapacity(50)

cd('/JDBCSystemResources/SOALocalTxDataSource/JDBCResource/SOALocalTxDataSource/JDBCConnectionPoolParams/SOALocalTxDataSource')
cmo.setMaxCapacity(100)
cmo.setMinCapacity(5)
cmo.setInitialCapacity(5)

cd('/SecurityConfiguration/<%= @domain_name %>/Realms/myrealm/UserLockoutManager/UserLockoutManager')
cmo.setLockoutEnabled(false)

cd('/AppDeployments/AqAdapter')
set('Targets', jarray.array([], ObjectName))

cd('/AppDeployments/b2bui')
set('Targets', jarray.array([], ObjectName))

cd('/AppDeployments/MQSeriesAdapter')
set('Targets', jarray.array([], ObjectName))

cd('/AppDeployments/OracleAppsAdapter')
set('Targets', jarray.array([], ObjectName))

cd('/AppDeployments/OracleBamAdapter')
set('Targets', jarray.array([], ObjectName))

cd('/AppDeployments/SocketAdapter')
set('Targets', jarray.array([], ObjectName))

cd('/AppDeployments/SimpleApprovalTaskFlow')
set('Targets', jarray.array([], ObjectName))

redeploy(appName='DbAdapter', planPath='<%= @adapter_plan_dir %>/Plan_DB.xml')

redeploy(appName='soa-infra', planPath='<%= @adapter_plan_dir %>/Plan_SOA.xml')

save()
activate(block='true')

startEdit()
cd('/')
cmo.createLogFilter('EviseLogFilter')
cd('/LogFilters/EviseLogFilter')
cmo.setFilterExpression('NOT(MESSAGE LIKE \'Closing socket as no data read from it%\')')
save()
activate(block='true')

startEdit()
cd('/Servers')
servers = ls('c', returnMap='true', returnType='c')
for server in servers:
    cd('/Servers/' + server + '/Log/' + server)
    cmo.setLogFileFilter(getMBean('/LogFilters/EviseLogFilter'))
    cmo.setStdoutFilter(getMBean('/LogFilters/EviseLogFilter'))
    cmo.setDomainLogBroadcastFilter(getMBean('/LogFilters/EviseLogFilter'))

save()
activate(block='true')

#serverConfig()

#rm = cmo.getSecurityConfiguration().getDefaultRealm().lookupRoleMapper('XACMLRoleMapper')

#print 'Adding Evise IDM Groups to WebLogic global roles'
#rm.setRoleExpression(None, 'Admin', 'Grp(Administrators)|Grp(IDM Administrators)')
#rm.setRoleExpression(None, 'Deployer', 'Grp(Deployers)|Grp(??)')
#rm.setRoleExpression(None, 'Monitor', 'Grp(Monitors)|Grp(??)')
#rm.setRoleExpression(None, 'Operator', 'Grp(Operators)|Grp(??)')

disconnect()
exit()