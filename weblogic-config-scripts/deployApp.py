connect('weblogic','weblogic','t3://localhost:7001')  
target='AdminServer' 

f = open(r'./applicationsList.txt','r')  

#In Above line you can specify the Complete Path of the “applications.txt” as well  

print f  

for i in range(3):  
line=f.readline()  
line1=line[:-1]  
appName='./'+line1  
print '*****************'+appName  
edit()  
startEdit()  
deploy(appName=line1,path=appName, targets=target)  
save()  
activate()  
f.close() 
