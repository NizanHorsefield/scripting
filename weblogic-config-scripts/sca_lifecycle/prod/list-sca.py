# STOPS A GIVEN COMPOSITE
# AUTHOR: NDH
# REVISION: 0.1

SOA_URL = sys.argv[1]
SOA_PORT = sys.argv[2]
USERNAME = sys.argv[3]
PASSWORD = sys.argv[4]

print "Listing Composites"
sca_listDeployedComposites(SOA_URL,SOA_PORT,USERNAME,PASSWORD)
print "Done"