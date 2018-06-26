    ##################################################   
    # This script is used to check the status of all WL instances including the admin , then issue a lifecyle command based on the state
    ###########################################################  
      
    def conn():  
        configFile='/path/.AdminScripts/userConfigFile.sec'  
        configKey='/path/.AdminScripts/userKeyFile.sec'  
        admurl = "t3://hostname:wlport"  
      
        try:  
            connect(userConfigFile=configFile, userKeyFile=configKey, url=admurl)  
        except ConnectionException,e:  
            print '\033[1;31m Unable to find admin server...\033[0m'  
            exit()  
      
    def srvState():  
        print 'Fetching state of every WebLogic instance'  
    #Fetch the state of the every WebLogic instance  
        for name in serverNames:  
            cd("/ServerLifeCycleRuntimes/" + name.getName())  
            serverState = cmo.getState()  
            if serverState == "RUNNING":  
                print 'Server ' + name.getName() + ' is :\033[1;32m' + serverState + '\033[0m'
				shutdown(name.getName(), force=true)	
            elif serverState == "STARTING":  
                print 'Server ' + name.getName() + ' is :\033[1;33m' + serverState + '\033[0m'  
            elif serverState == "UNKNOWN":  
                print 'Server ' + name.getName() + ' is :\033[1;34m' + serverState + '\033[0m'  
				start(name.getName())
            else:  
                print 'Server ' + name.getName() + ' is :\033[1;31m' + serverState + '\033[0m'  
            quit()  
      
    def quit():  
        print '\033[1;35mRe-Run the script HIT any key..\033[0m'  
        Ans = raw_input("Are you sure Quit from WLST... (y/n)")  
        if (Ans == 'y'):  
            disconnect()  
            stopRedirect()  
            exit()  
        else:  
            srvState()  
      
    if __name__== "main":  
        redirect('./logs/Server.log', 'false')         
        conn()  
        serverNames = cmo.getServers()  
        domainRuntime()  
        srvState()  