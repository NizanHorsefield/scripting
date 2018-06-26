import sys
from java.io import FileInputStream

# Import the property file
# propInputStream = FileInputStream("../conf/sit1.properties") # use if a dir scaffold is in place
propInputStream = FileInputStream("sit1.properties")
configProps = Properties()
configProps.load(propInputStream)

#vars from props file
adminURL=configProps.get("admin.url")
adminUserName=configProps.get("admin.userName")
adminPassword=configProps.get("admin.password")

#redirect wlst's own output to null, print lines in the script itself
redirect('/dev/null', 'false')

# connect to the admin server
connect(adminUserName, adminPassword, adminURL)
#conn_cw=boto.ec2.cloudwatch.connect_to_region(reg)

# obtain a list of managed servers in this domain
servers = cmo.getServers()
#print servers

# move to the domain runtime
domainRuntime()
name = sys.argv[1]
try:
  cd('/ServerRuntimes/nexteesadf_server' + name)
  cd('ThreadPoolRuntime/ThreadPoolRuntime')
  hoggerTC = cmo.getHoggingThreadCount()
  print "HTC " + str(hoggerTC)
except WLSTException, e:  
  print e
disconnect()

