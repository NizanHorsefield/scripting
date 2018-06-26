import re
import os
import pdb

connect(userConfigFile='<%= @user_config_file %>', userKeyFile='<%= @user_key_file %>', url='t3://<%= @admin_address %>:<%= @admin_port %>')

domainRuntime()

setAuditRepository(switchToDB='true')

disconnect()

connect(userConfigFile='<%= @user_config_file %>', userKeyFile='<%= @user_key_file %>', url='t3://<%= @bpm_ms1_address %>:<%= @bpm_ms1_port %>')

custom()

#WorkflowIdentityConfig = ObjectName('oracle.as.soainfra.config:WorkflowIdentityConfig=human-workflow,name=jazn.com,type=WorkflowIdentityConfig.ConfigurationType,Application=soa-infra')
#params = ['myrealm']
#types = ['java.lang.String']
#mbs.invoke(WorkflowIdentityConfig, 'setRealmName', params, types)

SoaInfraConfig = ObjectName('oracle.as.soainfra.config:name=soa-infra,type=SoaInfraConfig,Application=soa-infra')
auditLevel = Attribute('AuditLevel', 'Production')
mbs.setAttribute(SoaInfraConfig, auditLevel)
serverURL = Attribute('ServerURL', 'http://<%= @bpm_cluster_frontendhost %>:<%= @bpm_cluster_frontendhttpport %>')
mbs.setAttribute(SoaInfraConfig, serverURL)

if ("<%= @custom_identity %>" == "true"):
	keystoreLocation = Attribute('KeystoreLocation', '<%= @custom_identity_keystore_filename %>')
	mbs.setAttribute(SoaInfraConfig, keystoreLocation)

cd('/oracle.as.soainfra.config')
cd('oracle.as.soainfra.config:name=bpel,type=BPELConfig,Application=soa-infra')
ls()
BPELConfig = ObjectName('oracle.as.soainfra.config:name=bpel,type=BPELConfig,Application=soa-infra')
#dispatcherSystemThreads = Attribute('DispatcherSystemThreads', int(@bpel_system_threads@))
#mbs.setAttribute(BPELConfig, dispatcherSystemThreads)
#dispatcherInvokeThreads = Attribute('DispatcherInvokeThreads', int(@bpel_invoke_threads@))
#mbs.setAttribute(BPELConfig, dispatcherInvokeThreads)
#dispatcherEngineThreads = Attribute('DispatcherEngineThreads', int(@bpel_engine_threads@))
#mbs.setAttribute(BPELConfig, dispatcherEngineThreads)
syncMaxWaitTime = Attribute('SyncMaxWaitTime', int(150))
mbs.setAttribute(BPELConfig, syncMaxWaitTime)
auditLevel = Attribute('AuditLevel', 'off')
mbs.setAttribute(BPELConfig, auditLevel)
disableSensors = Attribute('DisableSensors', 1)
mbs.setAttribute(BPELConfig, disableSensors)
mbs.invoke(BPELConfig, 'disableRecurringAutoRecovery', None, None)
mbs.invoke(BPELConfig, 'disableStartupAutoRecovery', None, None)

cd('/oracle.as.soainfra.config')
cd('oracle.as.soainfra.config:name=bpmn,type=BPMNConfig,Application=soa-infra')
ls()
BPMNConfig = ObjectName('oracle.as.soainfra.config:name=bpmn,type=BPMNConfig,Application=soa-infra')
#dispatcherSystemThreads = Attribute('DispatcherSystemThreads', int(@bpmn_system_threads@))
#mbs.setAttribute(BPMNConfig, dispatcherSystemThreads)
#dispatcherInvokeThreads = Attribute('DispatcherInvokeThreads', int(@bpmn_invoke_threads@))
#mbs.setAttribute(BPMNConfig, dispatcherInvokeThreads)
#dispatcherEngineThreads = Attribute('DispatcherEngineThreads', int(@bpmn_engine_threads@))
#mbs.setAttribute(BPMNConfig, dispatcherEngineThreads)
auditKeyExtents = Attribute('AuditKeyExtents', int(20000))
mbs.setAttribute(BPMNConfig, auditKeyExtents)
auditLevel = Attribute('AuditLevel', 'off')
mbs.setAttribute(BPMNConfig, auditLevel)
disableSensors = Attribute('DisableSensors', 1)
mbs.setAttribute(BPMNConfig, disableSensors)
mbs.invoke(BPMNConfig, 'disableRecurringAutoRecovery', None, None)
mbs.invoke(BPMNConfig, 'disableStartupAutoRecovery', None, None)

MediatorConfig = ObjectName('oracle.as.soainfra.config:name=mediator,type=MediatorConfig,Application=soa-infra')
metricsLevel = Attribute('MetricsLevel', 'Disabled')
mbs.setAttribute(MediatorConfig, metricsLevel)

B2BConfig = ObjectName('oracle.as.soainfra.config:name=b2b,type=B2BConfig,Application=soa-infra')
params = ['b2b.donot_initialize', 'true', 'Disable B2B server']
types = ['java.lang.String', 'java.lang.String', 'java.lang.String']
mbs.invoke(B2BConfig, 'addProperty', params, types)	

disconnect()
exit()
