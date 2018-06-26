#http://docs.oracle.com/cd/E28280_01/core.1111/e12036/target_appendix_soa.htm

WLHOME='<%= @weblogic_home_dir %>'
DOMAIN_PATH='<%= @domain_dir %>'

ADFClusterName = '<%= @adf_cluster_name %>'
UCMClusterName = '<%= @ucm_cluster_name %>'
JATClusterName = '<%= @jat_cluster_name %>'

Ucm = '<%= @ucm_cluster_name %>'
Admin          = '<%= @adminserver_name %>'

ofm_version    = int(<%= @ofm_version %>)

AllArray = []
AdapterArray = []

AdapterArray.append('<%= @adminserver_name %>')
AllArray.append('<%= @adminserver_name %>')

AllArray.append('<%= @adf_cluster_name %>')
AllArray.append('<%= @ucm_cluster_name %>')
AllArray.append('<%= @jat_cluster_name %>')

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

cd('/Servers/UCM_server1')
set('ListenAddress','')

updateDomain()

cd('/')

delete('UCM_server1'        , 'Server')

unassign('StartupClass'           ,'*', 'Target' , All)
unassign('ShutdownClass'          ,'*', 'Target' , All)
unassign('Library'                ,'*', 'Target' , All)
unassign('AppDeployment'          ,'*', 'Target' , All)
unassign('JdbcSystemResource'     ,'*', 'Target' , All)
unassign('WldfSystemResource'     ,'*', 'Target' , All)

# apps
assign('AppDeployment', 'DMS Application#11.1.1.1.0'             , 'Target', All)
assign('AppDeployment', 'em'                                     , 'Target', Admin)
assign('AppDeployment', 'FMW Welcome Page Application#11.1.0.0.0', 'Target', Admin)
assign('AppDeployment', 'Oracle UCM Help'                               , 'Target', Ucm)
assign('AppDeployment', 'Oracle UCM Native Web Services'                               , 'Target', Ucm)
assign('AppDeployment', 'Oracle UCM Web Services'                               , 'Target', Ucm)
assign('AppDeployment', 'Oracle Universal Content Management - Content Server', 'Target', Ucm)
assign('AppDeployment', 'wsil-wls'                               , 'Target', All)
assign('AppDeployment', 'wsm-pm'                     , 'Target', All)

# libraries
assign('Library', 'adf.oracle.businesseditor#1.0@11.1.1.2.0'  , 'Target', All)
assign('Library', 'adf.oracle.domain#1.0@11.1.1.2.0'          , 'Target', All)
assign('Library', 'adf.oracle.domain.webapp#1.0@11.1.1.2.0'   , 'Target', All)

assign('Library', 'emai'                                   , 'Target', Admin)
assign('Library', 'emas'                                   , 'Target', Admin)
assign('Library', 'emcore'                                 , 'Target', Admin)

assign('Library', 'jsf#1.2@1.2.9.0' , 'Target', All)
assign('Library', 'jstl#1.2@1.2.0.1', 'Target', All)
assign('Library', 'ohw-rcf#5@5.0'   , 'Target', All)
assign('Library', 'ohw-uix#5@5.0'   , 'Target', All)

assign('Library', 'oracle.adf.dconfigbeans#1.0@11.1.1.2.0'            , 'Target', All)
assign('Library', 'oracle.adf.desktopintegration#1.0@11.1.1.2.0'      , 'Target', All)
assign('Library', 'oracle.adf.desktopintegration.model#1.0@11.1.1.2.0', 'Target', All)
assign('Library', 'oracle.adf.management#1.0@11.1.1.2.0'              , 'Target', All)

assign('Library', 'oracle.bi.adf.model.slib#1.0@11.1.1.2.0'    , 'Target', All)
assign('Library', 'oracle.bi.adf.view.slib#1.0@11.1.1.2.0'     , 'Target', All)
assign('Library', 'oracle.bi.adf.webcenter.slib#1.0@11.1.1.2.0', 'Target', All)
assign('Library', 'oracle.bi.composer#11.1.1@0.1'              , 'Target', All)
assign('Library', 'oracle.bi.jbips#11.1.1@0.1'                 , 'Target', All)

assign('Library', 'oracle.bpm.mgmt#11.1.1@11.1.1'                  , 'Target', Admin)

assign('Library', 'oracle.dconfig-infra#11@11.1.1.1.0'   , 'Target', All)
assign('Library', 'oracle.jrf.system.filter'             , 'Target', All)
assign('Library', 'oracle.jsp.next#11.1.1@11.1.1'        , 'Target', All)
assign('Library', 'oracle.pwdgen#11.1.1@11.1.1.2.0'      , 'Target', All)

assign('Library', 'oracle.webcenter.composer#11.1.1@11.1.1', 'Target', Admin)
assign('Library', 'oracle.webcenter.skin#11.1.1@11.1.1'    , 'Target', Admin)

assign('Library', 'oracle.wsm.seedpolicies#11.1.1@11.1.1', 'Target', All)
assign('Library', 'orai18n-adf#11@11.1.1.1.0'            , 'Target', All)
assign('Library', 'ReportPublisher Library'            , 'Target', Ucm)
assign('Library', 'ucm.em'            , 'Target', Admin)
assign('Library', 'UIX#11@11.1.1.1.0'                    , 'Target', All)

dumpStack();

assign('ShutdownClass', 'DMSShutdown'                                       , 'Target', All)
assign('ShutdownClass', 'JOC-Shutdown'                                      , 'Target', All)

assign('StartupClass' , 'AWT Application Context Startup Class'             , 'Target', All)
assign('StartupClass' , 'DMS-Startup'                                       , 'Target', All)
assign('StartupClass' , 'JMX Framework Startup Class'                       , 'Target', All)
assign('StartupClass' , 'JOC-Startup'                                       , 'Target', All)
assign('StartupClass' , 'JPS Startup Class'                                 , 'Target', All)
assign('StartupClass' , 'JRF Startup Class'                                 , 'Target', All)
assign('StartupClass' , 'ODL-Startup'                                       , 'Target', All)
assign('StartupClass' , 'Web Services Startup Class'                        , 'Target', All)

dumpStack();

assign('WldfSystemResource', 'Module-FMWDFW'       , 'Target', All)

assign('JdbcSystemResource', 'CSDS'            , 'Target', Ucm)
assign('JdbcSystemResource', 'JMSDataSource'       , 'Target', All)
assign('JdbcSystemResource', 'mds-owsm'            , 'Target', All)
assign('JdbcSystemResource', 'opssDataSource'  , 'Target', All)

dumpStack()

updateDomain()
dumpStack();

print 'Successfully Updated WebCenter Domain.'

closeDomain() 