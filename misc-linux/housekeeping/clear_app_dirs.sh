#!/bin/bash
# Clear any file or directory that was created 90 days prior

/bin/find /opt/fpu/log -ctime +90 -exec rm -rf {} \;
/bin/find /opt/fpu/log -ctime +90 -exec rm -rf {} \;
