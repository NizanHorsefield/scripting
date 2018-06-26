#http://docs.oracle.com/cd/E28280_01/core.1111/e12036/target_appendix_soa.htm

WLHOME='<%= @weblogic_home_dir %>'
DOMAIN_PATH='<%= @domain_dir %>'

bpmEnabled     = <%= @bpm_enabled %>
bamEnabled     = <%= @bam_enabled %>
soaEnabled     = <%= @soa_enabled %>
osbEnabled     = <%= @osb_enabled %>
oamEnabled     = <%= @oam_enabled %>
oimEnabled     = <%= @oim_enabled %>
odsEnabled     = <%= @ods_enabled %>

SOAClusterName = '<%= @soa_cluster_name %>'
BAMClusterName = '<%= @bam_cluster_name %>'
OSBClusterName = '<%= @osb_cluster_name %>'
OAMClusterName = '<%= @oam_cluster_name %>'
OIMClusterName = '<%= @oim_cluster_name %>'
ODSClusterName = '<%= @ods_cluster_name %>'
SoaOsb         = '<%= @soa_cluster_name %>,<%= @osb_cluster_name %>'
SoaBam         = '<%= @soa_cluster_name %>,<%= @bam_cluster_name %>'
SoaBamAdmin    = '<%= @soa_cluster_name %>,<%= @bam_cluster_name %>,<%= @adminserver_name %>'
SoaAdmin       = '<%= @soa_cluster_name %>,<%= @adminserver_name %>'
BamAdmin       = '<%= @bam_cluster_name %>,<%= @adminserver_name %>'
OsbAdmin       = '<%= @osb_cluster_name %>,<%= @adminserver_name %>'
OamAdmin       = '<%= @oam_cluster_name %>,<%= @adminserver_name %>'
OimAdmin       = '<%= @oim_cluster_name %>,<%= @adminserver_name %>'
OimOamAdmin    = '<%= @oim_cluster_name %>,<%= @oam_cluster_name %>,<%= @adminserver_name %>'
SoaOimCluster  = '<%= @oim_cluster_name %>,<%= @soa_cluster_name %>'
SoaOimAdmin    = '<%= @oim_cluster_name %>,<%= @soa_cluster_name %>,<%= @adminserver_name %>'
SoaBamOimAdmin = '<%= @bam_cluster_name %>,<%= @oim_cluster_name %>,<%= @soa_cluster_name %>,<%= @adminserver_name %>'
SoaOimOamAdmin = '<%= @oam_cluster_name %>,<%= @oim_cluster_name %>,<%= @soa_cluster_name %>,<%= @adminserver_name %>'
Admin          = '<%= @adminserver_name %>'

ofm_version    = int(<%= @ofm_version %>)

AllArray = []
AdapterArray = []

AdapterArray.append('<%= @adminserver_name %>')
AllArray.append('<%= @adminserver_name %>')

if bamEnabled == true:
    AllArray.append('<%= @bam_cluster_name %>')

if soaEnabled == true:
    AdapterArray.append('<%= @soa_cluster_name %>')
    AllArray.append('<%= @soa_cluster_name %>')

if osbEnabled == true:
    AdapterArray.append('<%= @osb_cluster_name %>')
    AllArray.append('<%= @osb_cluster_name %>')

if oamEnabled == true:    
    AllArray.append('<%= @oam_cluster_name %>')

if oimEnabled == true:
    AllArray.append('<%= @oim_cluster_name %>')

if odsEnabled == true:
    AllArray.append('<%= @ods_cluster_name %>')

All       = ','.join(AllArray)
Adapters  = ','.join(AdapterArray)

def getFirstClusterServer(cluster):
    s = ls('/Server')
    clustername = " "
    tokens = s.split("drw-")
    tokens.sort()
    for token in tokens:
        token=token.strip().lstrip().rstrip()
        path="/Server/"+token
        cd(path)
        if not token == Admin and not token == '':
            clustername = get('Cluster')
            searchClusterStr = cluster+":"
            clusterNameStr = str(clustername)
            if not clusterNameStr.find(searchClusterStr) == -1:
                return token    

readDomain(DOMAIN_PATH)

cd('/')
if soaEnabled == true:
    cd('/Servers/soa_server1')
    set('ListenAddress','')

if bamEnabled == true:
    cd('/Servers/bam_server1')
    set('ListenAddress','')

if osbEnabled == true:
    cd('/Servers/osb_server1')
    set('ListenAddress','')

updateDomain()

if osbEnabled == true:
    OSBServer1Name = getFirstClusterServer(OSBClusterName)

if bamEnabled == true:
    BAMServer1Name = getFirstClusterServer(BAMClusterName)

cd('/')

if soaEnabled == true:
    delete('SOAJMSModule'           , 'JMSSystemResource')
    delete('SOAJMSServer'           , 'JMSServer')
    delete('UMSJMSSystemResource'   , 'JMSSystemResource')
    delete('soa_server1'        , 'Server')

    if bamEnabled == true:
        delete('UMSJMSServer_auto_1', 'JMSServer')
    else:
        delete('UMSJMSServer'       , 'JMSServer')

if bamEnabled == true:
    delete('BAMJmsSystemResource'   , 'JMSSystemResource')
    delete('BAMJMSServer'           , 'JMSServer')
    delete('UMSJMSServer_auto_2'    , 'JMSServer')
    delete('bam_server1'            , 'Server')

if osbEnabled == true:
    delete('osb_server1'            , 'Server')

if oimEnabled == true:
    delete('oim_server1'        , 'Server')

if oamEnabled == true:
    delete('oam_server1'        , 'Server')

unassign('StartupClass'           ,'*', 'Target' , All)
unassign('ShutdownClass'          ,'*', 'Target' , All)
unassign('Library'                ,'*', 'Target' , All)
unassign('AppDeployment'          ,'*', 'Target' , All)
unassign('JdbcSystemResource'     ,'*', 'Target' , All)
unassign('WldfSystemResource'     ,'*', 'Target' , All)
unassign('JmsSystemResource'      ,'*', 'Target' , All)
#unassign('SelfTuning.WorkManager' ,'*', 'Target' , All)

# resource adapters
assign('AppDeployment', 'AqAdapter'                  , 'Target', Adapters)
assign('AppDeployment', 'DbAdapter'                  , 'Target', Adapters)
assign('AppDeployment', 'FileAdapter'                , 'Target', Adapters)
assign('AppDeployment', 'FtpAdapter'                 , 'Target', Adapters)
assign('AppDeployment', 'JmsAdapter'                 , 'Target', Adapters)
assign('AppDeployment', 'MQSeriesAdapter'            , 'Target', Adapters)
assign('AppDeployment', 'OracleAppsAdapter'          , 'Target', Adapters)
assign('AppDeployment', 'OracleBamAdapter'           , 'Target', Adapters)
assign('AppDeployment', 'SocketAdapter'              , 'Target', Adapters)

if soaEnabled == true and ofm_version > 1116:
    assign('AppDeployment', 'UMSAdapter' , 'Target', Adapters)
else:
    print "Warning: UMSAdapter Adapter not deployed. This is expected behaviour for versions of OFM 11.1.1.6 and below."

# apps
assign('AppDeployment', 'DMS Application#11.1.1.1.0'             , 'Target', All)
assign('AppDeployment', 'wsil-wls'                               , 'Target', All)
assign('AppDeployment', 'em'                                     , 'Target', Admin)
assign('AppDeployment', 'FMW Welcome Page Application#11.1.0.0.0', 'Target', Admin)

if soaEnabled == true:
    assign('AppDeployment', 'b2bui'                      , 'Target', SOAClusterName)
    assign('AppDeployment', 'composer'                   , 'Target', SOAClusterName)
    assign('AppDeployment', 'DefaultToDoTaskFlow'        , 'Target', SOAClusterName)
    assign('AppDeployment', 'soa-infra'                  , 'Target', SOAClusterName)
    assign('AppDeployment', 'worklistapp'                , 'Target', SOAClusterName)

#bpm
if bpmEnabled == true:
    assign('AppDeployment', 'BPMComposer'                , 'Target', SOAClusterName)
    assign('AppDeployment', 'OracleBPMComposerRolesApp'  , 'Target', SOAClusterName)
    assign('AppDeployment', 'OracleBPMProcessRolesApp'   , 'Target', SOAClusterName)
    assign('AppDeployment', 'OracleBPMWorkspace'         , 'Target', SOAClusterName)
    assign('AppDeployment', 'SimpleApprovalTaskFlow'     , 'Target', SOAClusterName)
    
    if ofm_version > 1116:
        assign('AppDeployment', 'frevvo'                     , 'Target', SOAClusterName)
    else:
        print "Warning: frevvo not deployed. This is expected behaviour for versions of OFM 11.1.1.6 and below."

if bamEnabled == true:
    assign('AppDeployment', 'usermessagingdriver-email'  , 'Target', SoaBam)
    assign('AppDeployment', 'usermessagingserver'        , 'Target', SoaBam)
    assign('AppDeployment', 'wsm-pm'                     , 'Target', SoaBam)
elif oimEnabled:
    assign('AppDeployment', 'usermessagingdriver-email'  , 'Target', SOAClusterName)
    assign('AppDeployment', 'TaskDetails'                , 'Target', SOAClusterName)
    assign('AppDeployment', 'usermessagingserver'        , 'Target', SOAClusterName)
    assign('AppDeployment', 'wsm-pm'                     , 'Target', SoaOimCluster)    
elif soaEnabled == true:
    assign('AppDeployment', 'usermessagingdriver-email'  , 'Target', SOAClusterName)
    assign('AppDeployment', 'usermessagingserver'        , 'Target', SOAClusterName)
    assign('AppDeployment', 'wsm-pm'                     , 'Target', SOAClusterName)

# advanced target
if bamEnabled == true:
    assign('AppDeployment',              'oracle-bam#11.1.1'                                     , 'Target', BAMClusterName)
    #assign('AppDeployment.SubDeployment','oracle-bam#11.1.1.*'                                  , 'Target', BAMServer1Name)
    #assign('AppDeployment.SubDeployment','oracle-bam#11.1.1./oracle/bam'                        , 'Target', BAMServer1Name)
    #assign('AppDeployment.SubDeployment','oracle-bam#11.1.1.oracle-bam-adc-ejb.jar'             , 'Target', BAMServer1Name)
    #assign('AppDeployment.SubDeployment','oracle-bam#11.1.1.oracle-bam-ems-ejb.jar'             , 'Target', BAMServer1Name)
    #assign('AppDeployment.SubDeployment','oracle-bam#11.1.1.oracle-bam-eventengine-ejb.jar'     , 'Target', BAMServer1Name)
    #assign('AppDeployment.SubDeployment','oracle-bam#11.1.1.oracle-bam-reportcache-ejb.jar'     , 'Target', BAMServer1Name)
    #assign('AppDeployment.SubDeployment','oracle-bam#11.1.1.oracle-bam-statuslistener-ejb.jar'  , 'Target', BAMServer1Name)
    #assign('AppDeployment.SubDeployment','oracle-bam#11.1.1.sdpmessagingclient-ejb.jar'         , 'Target', BAMServer1Name)

if osbEnabled == true:
    assign('AppDeployment', 'ALDSP Transport Provider'                  , 'Target', OsbAdmin)
    assign('AppDeployment', 'ALSB Coherence Cache Provider'             , 'Target', OSBClusterName)
    assign('AppDeployment', 'ALSB Framework Starter Application'        , 'Target', OsbAdmin)
    assign('AppDeployment', 'ALSB Logging'                              , 'Target', OsbAdmin)
    assign('AppDeployment', 'ALSB Publish'                              , 'Target', OsbAdmin)
    assign('AppDeployment', 'ALSB Resource'                             , 'Target', OSBClusterName)
    assign('AppDeployment', 'ALSB Routing'                              , 'Target', OsbAdmin)
    assign('AppDeployment', 'ALSB Subscription Listener'                , 'Target', OSBClusterName)
    assign('AppDeployment', 'ALSB Test Framework'                       , 'Target', OsbAdmin)
    assign('AppDeployment', 'ALSB Transform'                            , 'Target', OsbAdmin)
    assign('AppDeployment', 'ALSB UDDI Manager'                         , 'Target', Admin)
    assign('AppDeployment', 'ALSB WSIL'                                 , 'Target', OSBClusterName)
    assign('AppDeployment', 'BPEL 10g Transport Provider'               , 'Target', OsbAdmin)
    assign('AppDeployment', 'EJB Transport Provider'                    , 'Target', OsbAdmin)
    assign('AppDeployment', 'FLOW Transport Provider'                   , 'Target', OsbAdmin)
    assign('AppDeployment', 'JCA Transport Provider'                    , 'Target', OsbAdmin)
    assign('AppDeployment', 'JEJB Transport Provider'                   , 'Target', OsbAdmin)
    assign('AppDeployment', 'JMS Reporting Provider'                    , 'Target', OSBClusterName)
    assign('AppDeployment', 'MQ Transport Provider'                     , 'Target', OsbAdmin)
    assign('AppDeployment', 'SB Transport Provider'                     , 'Target', OsbAdmin)
    assign('AppDeployment', 'ServiceBus_Console'                        , 'Target', Admin)
    assign('AppDeployment', 'SOA-DIRECT Transport Provider'             , 'Target', OsbAdmin)
    assign('AppDeployment', 'Tuxedo Transport Provider'                 , 'Target', OsbAdmin)
    assign('AppDeployment', 'WS Transport Async Applcation'             , 'Target', OSBClusterName)
    assign('AppDeployment', 'WS Transport Provider'                     , 'Target', OsbAdmin)
    assign('AppDeployment', 'XBus Kernel'                               , 'Target', OsbAdmin)

# target to first osb server of the cluster
if osbEnabled == true:
    assign('AppDeployment', 'ALSB Cluster Singleton Marker Application' , 'Target', OSBServer1Name)
    assign('AppDeployment', 'ALSB Domain Singleton Marker Application'  , 'Target', OSBServer1Name)
    assign('AppDeployment', 'Message Reporting Purger'                  , 'Target', OSBServer1Name)

# target sub deployments to the the cluster
if osbEnabled == true:
    assign('AppDeployment', 'Email Transport Provider'                                  , 'Target', OsbAdmin)
    assign('AppDeployment.SubDeployment', 'Email Transport Provider.emailtransport.jar' , 'Target', OSBClusterName)
    assign('AppDeployment', 'File Transport Provider'                                   , 'Target', OsbAdmin)
    assign('AppDeployment.SubDeployment', 'File Transport Provider.filepoll.jar'        , 'Target', OSBClusterName)
    assign('AppDeployment', 'Ftp Transport Provider'                                    , 'Target', OsbAdmin)
    assign('AppDeployment.SubDeployment', 'Ftp Transport Provider.ftp_transport.jar'    , 'Target', OSBClusterName)
    assign('AppDeployment', 'SFTP Transport Provider'                                   , 'Target', OsbAdmin)
    assign('AppDeployment.SubDeployment', 'SFTP Transport Provider.sftp_transport.jar'  , 'Target', OSBClusterName)

if oimEnabled == true:
    assign('AppDeployment', 'Nexaweb', 'Target', OIMClusterName)
    assign('AppDeployment', 'spml-xsd', 'Target', OIMClusterName)
    assign('AppDeployment', 'RoleSOD', 'Target', OIMClusterName)

    if ofm_version > 1115:
      assign('AppDeployment', 'OIMAppMetadata#11.1.2.0.0', 'Target', OIMClusterName)
      assign('AppDeployment', 'OIMMetadata#11.1.2.0.0', 'Target', OIMClusterName)
      assign('AppDeployment', 'oim#11.1.2.0.0', 'Target', OIMClusterName)
      assign('AppDeployment', 'oracle.iam.console.identity.self-service.ear#V2.0', 'Target', OIMClusterName)
      assign('AppDeployment', 'oracle.iam.console.identity.sysadmin.ear#V2.0', 'Target', OIMClusterName)
      assign('AppDeployment', 'SodCheckService', 'Target', OIMClusterName)
      assign('AppDeployment', 'ProvCallback', 'Target', OIMClusterName)
      assign('AppDeployment', 'Reqsvc', 'Target', OIMClusterName)
    else:
      assign('AppDeployment', 'OIMMetadata#11.1.1.3.0', 'Target', OIMClusterName)
      assign('AppDeployment', 'oim#11.1.1.3.0', 'Target', OIMClusterName)

if oamEnabled == true and ofm_version < 1116:
    assign('AppDeployment', 'oam_server', 'Target', OAMClusterName)
    assign('AppDeployment', 'oam_admin#11.1.1.3.0', 'Target', Admin)
    assign('AppDeployment', 'oamsso_logout#11.1.1.3.0', 'Target', OamAdmin)
elif oamEnabled == true:
    assign('AppDeployment', 'oam_server#11.1.2.0.0', 'Target', OAMClusterName)
    assign('AppDeployment', 'oam_admin#11.1.2.0.0', 'Target', Admin)
    assign('AppDeployment', 'oamsso_logout#11.1.2.0.0', 'Target', OamAdmin)
    
if odsEnabled == true:
    assign('AppDeployment', 'odsm#11.1.1.2.0', 'Target', ODSClusterName)
    
assign('Library', 'emai'                                   , 'Target', Admin)

if oimEnabled == true and ofm_version > 1115:
    assign('Library', 'oracle.webcenter.skin#11.1.1@11.1.1'    , 'Target', OimAdmin)
else:
    assign('Library', 'oracle.webcenter.skin#11.1.1@11.1.1'    , 'Target', Admin)

if oimEnabled == true or oamEnabled == true or odsEnabled:
    assign('Library', 'oracle.idm.uishell#11.1.1@11.1.1'       , 'Target', All)
    assign('Library', 'oracle.webcenter.composer#11.1.1@11.1.1', 'Target', All)

    if oimEnabled == true and oamEnabled == true:
        assign('Library', 'oracle.idm.common.model#11.1.1@11.1.1'  , 'Target', OimOamAdmin)
        if ofm_version > 1115:
            assign('Library', 'oracle.idm.ids.config.ui#11.1.2@11.1.2' , 'Target', OimOamAdmin)

    elif oimEnabled == false and oamEnabled == true:
        assign('Library', 'oracle.idm.common.model#11.1.1@11.1.1'  , 'Target', OamAdmin)
        if ofm_version > 1115:
            assign('Library', 'oracle.idm.ids.config.ui#11.1.2@11.1.2' , 'Target', OamAdmin)

    elif oimEnabled == true and oamEnabled == false:
        assign('Library', 'oracle.idm.common.model#11.1.1@11.1.1'  , 'Target', OimAdmin)
        if ofm_version > 1115:
            assign('Library', 'oracle.idm.ids.config.ui#11.1.2@11.1.2' , 'Target', OimAdmin)
else:
    assign('Library', 'oracle.webcenter.composer#11.1.1@11.1.1', 'Target', Admin)

assign('Library', 'emas'                                   , 'Target', Admin)
assign('Library', 'emcore'                                 , 'Target', Admin)


assign('Library', 'adf.oracle.businesseditor#1.0@11.1.1.2.0'  , 'Target', All)
assign('Library', 'adf.oracle.domain#1.0@11.1.1.2.0'          , 'Target', All)
assign('Library', 'adf.oracle.domain.webapp#1.0@11.1.1.2.0'   , 'Target', All)

assign('Library', 'jsf#1.2@1.2.9.0' , 'Target', All)
assign('Library', 'jstl#1.2@1.2.0.1', 'Target', All)
assign('Library', 'ohw-rcf#5@5.0'   , 'Target', All)
assign('Library', 'ohw-uix#5@5.0'   , 'Target', All)

assign('Library', 'oracle.adf.desktopintegration.model#1.0@11.1.1.2.0', 'Target', All)
assign('Library', 'oracle.adf.desktopintegration#1.0@11.1.1.2.0'      , 'Target', All)
assign('Library', 'oracle.adf.dconfigbeans#1.0@11.1.1.2.0'            , 'Target', All)
assign('Library', 'oracle.adf.management#1.0@11.1.1.2.0'              , 'Target', All)

assign('Library', 'oracle.bi.jbips#11.1.1@0.1'                 , 'Target', All)
assign('Library', 'oracle.bi.composer#11.1.1@0.1'              , 'Target', All)
assign('Library', 'oracle.bi.adf.model.slib#1.0@11.1.1.2.0'    , 'Target', All)
assign('Library', 'oracle.bi.adf.view.slib#1.0@11.1.1.2.0'     , 'Target', All)
assign('Library', 'oracle.bi.adf.webcenter.slib#1.0@11.1.1.2.0', 'Target', All)

assign('Library', 'oracle.dconfig-infra#11@11.1.1.1.0'   , 'Target', All)
assign('Library', 'oracle.jrf.system.filter'             , 'Target', All)
assign('Library', 'oracle.jsp.next#11.1.1@11.1.1'        , 'Target', All)
assign('Library', 'oracle.pwdgen#11.1.1@11.1.1.2.0'      , 'Target', All)


assign('Library', 'oracle.wsm.seedpolicies#11.1.1@11.1.1', 'Target', All)
assign('Library', 'orai18n-adf#11@11.1.1.1.0'            , 'Target', All)
assign('Library', 'UIX#11@11.1.1.1.0'                    , 'Target', All)

# OIM Specific targets
if oimEnabled == true and ofm_version > 1115:
    if bamEnabled == true:
        assign('Library', 'oracle.sdp.client#11.1.1@11.1.1'                , 'Target', SoaBamOimOamAdmin)
        assign('Library', 'oracle.soa.rules_dict_dc.webapp#11.1.1@11.1.1'  , 'Target', SoaBamOim)
        assign('Library', 'oracle.rules#11.1.1@11.1.1'                     , 'Target', SoaBamOimAdmin)
    # Assume SOA is enabled for OIM
    else:
        assign('Library', 'oracle.sdp.client#11.1.1@11.1.1'                , 'Target', SoaOimOamAdmin)
        assign('Library', 'oracle.soa.rules_dict_dc.webapp#11.1.1@11.1.1'  , 'Target', SoaOimCluster)
        assign('Library', 'oracle.rules#11.1.1@11.1.1'                     , 'Target', SoaOimAdmin)

elif bamEnabled == true:
    assign('Library', 'oracle.sdp.client#11.1.1@11.1.1'                , 'Target', SoaBam)
    assign('Library', 'oracle.rules#11.1.1@11.1.1'                     , 'Target', SoaBamAdmin)
    assign('Library', 'oracle.soa.rules_dict_dc.webapp#11.1.1@11.1.1'  , 'Target', SoaBam)
    
elif soaEnabled == true:
    assign('Library', 'oracle.sdp.client#11.1.1@11.1.1'                , 'Target', SoaAdmin)
    assign('Library', 'oracle.rules#11.1.1@11.1.1'                     , 'Target', SoaAdmin)
    assign('Library', 'oracle.soa.rules_dict_dc.webapp#11.1.1@11.1.1'  , 'Target', SoaAdmin)

if soaEnabled == true:
    assign('Library', 'oracle.sdp.messaging#11.1.1@11.1.1'             , 'Target', SoaAdmin)
    assign('Library', 'oracle.bpm.mgmt#11.1.1@11.1.1'                  , 'Target', Admin)
    assign('Library', 'oracle.soa.bpel#11.1.1@11.1.1'                  , 'Target', SoaAdmin)
    assign('Library', 'oracle.soa.composer.webapp#11.1.1@11.1.1'       , 'Target', SoaAdmin)
    assign('Library', 'oracle.soa.ext#11.1.1@11.1.1'                   , 'Target', SoaAdmin)
    assign('Library', 'oracle.soa.mediator#11.1.1@11.1.1'              , 'Target', SoaAdmin)
    assign('Library', 'oracle.soa.worklist#11.1.1@11.1.1'              , 'Target', SoaAdmin)
    assign('Library', 'oracle.applcore.model#0.1@11.1.1.0.0'           , 'Target', SOAClusterName)
    assign('Library', 'oracle.applcore.view#0.1@11.1.1.0.0'            , 'Target', SOAClusterName)

    if ofm_version > 1115:
      assign('Library', 'oracle.applcore.config#0.1@11.1.1.0.0'          , 'Target', SOAClusterName)
    
    if oimEnabled == true:
        assign('Library', 'oracle.soa.workflow.wc#11.1.1@11.1.1'           , 'Target', SoaOimAdmin)
        assign('Library', 'oracle.soa.worklist.webapp#11.1.1@11.1.1'       , 'Target', SoaOimAdmin)
        assign('Library', 'oracle.soa.rules_editor_dc.webapp#11.1.1@11.1.1', 'Target', SoaAdmin)
        assign('Library', 'oracle.soa.workflow#11.1.1@11.1.1'              , 'Target', SoaAdmin)
    else:
        assign('Library', 'oracle.soa.workflow.wc#11.1.1@11.1.1'           , 'Target', SOAClusterName)
        assign('Library', 'oracle.soa.worklist.webapp#11.1.1@11.1.1'       , 'Target', SOAClusterName)
        assign('Library', 'oracle.soa.rules_editor_dc.webapp#11.1.1@11.1.1', 'Target', SoaAdmin)
        assign('Library', 'oracle.soa.workflow#11.1.1@11.1.1'              , 'Target', SOAClusterName)


if bamEnabled == true:
    assign('Library', 'oracle.bam.library#11.1.1@11.1.1'       , 'Target', BamAdmin)

#bpm
if bpmEnabled == true:
    assign('Library', 'oracle.bpm.client#11.1.1@11.1.1'        , 'Target', SoaAdmin)
    assign('Library', 'oracle.bpm.composerlib#11.1.1@11.1.1'   , 'Target', SoaAdmin)
    assign('Library', 'oracle.bpm.projectlib#11.1.1@11.1.1'    , 'Target', SoaAdmin)
    assign('Library', 'oracle.bpm.runtime#11.1.1@11.1.1'       , 'Target', SoaAdmin)
    assign('Library', 'oracle.bpm.webapp.common#11.1.1@11.1.1' , 'Target', SoaAdmin)
    assign('Library', 'oracle.bpm.workspace#11.1.1@11.1.1'     , 'Target', SoaAdmin)

if osbEnabled == true:
    assign('Library', 'oracle.jrf.coherence#3@11.1.1'                   , 'Target', OsbAdmin)
    assign('Library', 'coherence-l10n#11.1.1@11.1.1'                    , 'Target', OSBClusterName)
    assign('Library', 'ftptransport-l10n#2.5@2.5'                       , 'Target', OsbAdmin)
    assign('Library', 'sftptransport-l10n#3.0@3.0'                      , 'Target', OsbAdmin)
    assign('Library', 'emailtransport-l10n#2.5@2.5'                     , 'Target', OsbAdmin)
    assign('Library', 'filetransport-l10n#2.5@2.5'                      , 'Target', OsbAdmin)
    assign('Library', 'mqtransport-l10n#3.0@3.0'                        , 'Target', OsbAdmin)
    assign('Library', 'mqconnection-l10n#3.0@3.0'                       , 'Target', OsbAdmin)
    assign('Library', 'ejbtransport-l10n#2.5@2.5'                       , 'Target', OsbAdmin)
    assign('Library', 'tuxedotransport-l10n#2.5@2.5'                    , 'Target', OsbAdmin)
    assign('Library', 'aldsp_transport-l10n#3.0@3.0'                    , 'Target', OsbAdmin)
    assign('Library', 'wstransport-l10n#2.6@2.6'                        , 'Target', OsbAdmin)
    assign('Library', 'flow-transport-l10n#3.0@3.0'                     , 'Target', OsbAdmin)
    assign('Library', 'bpel10gtransport-l10n#3.1@3.1'                   , 'Target', OsbAdmin)
    assign('Library', 'jcatransport-l10n#3.1@3.1'                       , 'Target', OsbAdmin)
    assign('Library', 'wsif#11.1.1@11.1.1'                              , 'Target', OsbAdmin)
    assign('Library', 'JCAFrameworkImpl#11.1.1@11.1.1'                  , 'Target', OsbAdmin)
    assign('Library', 'jejbtransport-l10n#3.2@3.2'                      , 'Target', OsbAdmin)
    assign('Library', 'jejbtransport-jar#3.2@3.2'                       , 'Target', OsbAdmin)
    assign('Library', 'soatransport-l10n#11.1.1.2.0@11.1.1.2.0'         , 'Target', OsbAdmin)
    assign('Library', 'stage-utils#2.5@2.5'                             , 'Target', OsbAdmin)
    assign('Library', 'sbconsole-l10n#2.5@2.5'                          , 'Target', OsbAdmin)
    assign('Library', 'xbusrouting-l10n#2.5@2.5'                        , 'Target', OsbAdmin)
    assign('Library', 'xbustransform-l10n#2.5@2.5'                      , 'Target', OsbAdmin)
    assign('Library', 'xbuspublish-l10n#2.5@2.5'                        , 'Target', OsbAdmin)
    assign('Library', 'xbuslogging-l10n#2.5@2.5'                        , 'Target', OsbAdmin)
    assign('Library', 'testfwk-l10n#2.5@2.5'                            , 'Target', OsbAdmin)
    assign('Library', 'com.bea.wlp.lwpf.console.app#10.3.0@10.3.0'      , 'Target', OsbAdmin)
    assign('Library', 'com.bea.wlp.lwpf.console.web#10.3.0@10.3.0'      , 'Target', OsbAdmin)
    assign('Library', 'wlp-lookandfeel-web-lib#10.3.0@10.3.0'           , 'Target', OsbAdmin)
    assign('Library', 'wlp-light-web-lib#10.3.0@10.3.0'                 , 'Target', OsbAdmin)
    assign('Library', 'wlp-framework-common-web-lib#10.3.0@10.3.0'      , 'Target', OsbAdmin)
    assign('Library', 'wlp-framework-struts-1.2-web-lib#10.3.0@10.3.0'  , 'Target', OsbAdmin)
    assign('Library', 'struts-1.2#1.2@1.2.9'                            , 'Target', OsbAdmin)
    assign('Library', 'beehive-netui-1.0.1-10.0#1.0@1.0.2.2'            , 'Target', OsbAdmin)
    assign('Library', 'beehive-netui-resources-1.0.1-10.0#1.0@1.0.2.2'  , 'Target', OsbAdmin)
    assign('Library', 'beehive-controls-1.0.1-10.0-war#1.0@1.0.2.2'     , 'Target', OsbAdmin)
    assign('Library', 'weblogic-controls-10.0-war#10.0@10.2'            , 'Target', OsbAdmin)
    assign('Library', 'wls-commonslogging-bridge-war#1.0@1.1'           , 'Target', OsbAdmin)

if oamEnabled == true:
    assign('Library', 'oracle.oaam.libs#11.1.1.3.0@11.1.1.3.0' , 'Target', OAMClusterName) 
    
    if ofm_version > 1115:
      assign('Library', 'oracle.idm.ipf#11.1.2@11.1.2'           , 'Target', OamAdmin) 
      assign('Library', 'coherence#3.7.1.1@3.7.1.1'              , 'Target', OamAdmin) 
      assign('Library', 'coherence#3.7.1.1@3.7.1.1'              , 'Target', OamAdmin) 

if oimEnabled == true:
    assign('Library', 'oracle.grcc.oaacg#8.6.1@8.6.1'          , 'Target', OIMClusterName)
    assign('Library', 'org.bouncycastle.bcprovider#1.1@1.36.0' , 'Target', OIMClusterName)
    
    if ofm_version > 1115:
      assign('Library', 'oracle.iam.ui.model#1.0@11.1.1.5.0'     , 'Target', OIMClusterName) 
      assign('Library', 'oracle.iam.ui.view#11.1.1@11.1.1'       , 'Target', OIMClusterName) 
      assign('Library', 'oracle.iam.ui.oia-view#11.1.1@11.1.1'   , 'Target', OIMClusterName)
      assign('Library', 'oracle.iam.ui.custom#11.1.1@11.1.1'     , 'Target', OIMClusterName)

dumpStack();


assign('ShutdownClass', 'JOC-Shutdown'                                      , 'Target', All)
assign('ShutdownClass', 'DMSShutdown'                                       , 'Target', All)

assign('StartupClass' , 'JRF Startup Class'                                 , 'Target', All)
assign('StartupClass' , 'JPS Startup Class'                                 , 'Target', All)
assign('StartupClass' , 'ODL-Startup'                                       , 'Target', All)
assign('StartupClass' , 'AWT Application Context Startup Class'             , 'Target', All)
assign('StartupClass' , 'JMX Framework Startup Class'                       , 'Target', All)
assign('StartupClass' , 'Web Services Startup Class'                        , 'Target', All)
assign('StartupClass' , 'JOC-Startup'                                       , 'Target', All)
assign('StartupClass' , 'DMS-Startup'                                       , 'Target', All)

if oimEnabled:
    assign('StartupClass' , 'Audit Loader Startup Class'                       , 'Target', All)

if soaEnabled == true:
    assign('StartupClass' , 'SOAStartupClass'                                , 'Target', SOAClusterName)

if osbEnabled == true:
    assign('StartupClass' , 'OSB JCA Transport Post-Activation Startup Class', 'Target', OsbAdmin)

dumpStack();

assign('WldfSystemResource', 'Module-FMWDFW'       , 'Target', All)

assign('JdbcSystemResource', 'JMSDataSource'       , 'Target', All)

if soaEnabled == true:
    assign('JdbcSystemResource', 'EDNDataSource'       , 'Target', SOAClusterName)
    assign('JdbcSystemResource', 'EDNLocalTxDataSource', 'Target', SOAClusterName)
    assign('JdbcSystemResource', 'mds-soa'             , 'Target', SoaAdmin)
    assign('JdbcSystemResource', 'SOADataSource'       , 'Target', SOAClusterName)
    assign('JdbcSystemResource', 'SOALocalTxDataSource', 'Target', SOAClusterName)

    if oamEnabled == true and ofm_version > 1115:
        assign('JdbcSystemResource', 'opss-DBDS'       , 'Target', All)
    else:
        assign('JdbcSystemResource', 'opssDataSource'  , 'Target', All)

    if oimEnabled == true:
        assign('JdbcSystemResource', 'mds-owsm'            , 'Target', SoaOimAdmin)
    else:
        assign('JdbcSystemResource', 'mds-owsm'            , 'Target', SoaAdmin)
        assign('JdbcSystemResource', 'AuditDataSource'       , 'Target', SOAClusterName)

    if bamEnabled == true:
        assign('JdbcSystemResource', 'OraSDPMDataSource'   , 'Target', SoaBam)
    else:
        assign('JdbcSystemResource', 'OraSDPMDataSource'   , 'Target', SOAClusterName)

if oamEnabled == true:
    assign('JdbcSystemResource', 'oamDS'               , 'Target', OamAdmin)
    
if oimEnabled == true:
    assign('JdbcSystemResource', 'mds-oim'             , 'Target', OIMClusterName)
    assign('JdbcSystemResource', 'oimJMSStoreDS'       , 'Target', OIMClusterName)
    
    if soaEnabled == true:
        assign('JdbcSystemResource', 'oimOperationsDB'     , 'Target', SoaOimCluster)
    else:
        assign('JdbcSystemResource', 'oimOperationsDB'     , 'Target', OIMClusterName)

    if ofm_version > 1115:
        assign('JdbcSystemResource', 'ApplicationDB'       , 'Target', OIMClusterName)


if bamEnabled == true:
    assign('JdbcSystemResource', 'BAMDataSource'       , 'Target', BAMClusterName)

if osbEnabled == true:
    assign('JdbcSystemResource', 'wlsbjmsrpDataSource' , 'Target', OsbAdmin)

dumpStack()

updateDomain()
dumpStack();

print 'Successfully Updated SOA Domain.'

closeDomain() 