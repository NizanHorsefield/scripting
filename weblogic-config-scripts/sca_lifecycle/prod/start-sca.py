# STOPS A GIVEN COMPOSITE
# AUTHOR: NDH
# REVISION: 0.1

SOA_URL = sys.argv[1]
SOA_PORT = sys.argv[2]
USERNAME = sys.argv[3]
PASSWORD = sys.argv[4]
COMPOSITE_NAME = sys.argv[5]
REVISION = sys.argv[6]

print "Stopping the composite " + COMPOSITE_NAME
sca_startComposite(SOA_URL,SOA_PORT,USERNAME,PASSWORD,COMPOSITE_NAME,REVISION,partition="default")
print "Done"