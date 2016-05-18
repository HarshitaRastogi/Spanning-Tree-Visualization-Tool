"""list-switches,protocol
dictionary-spanningtree"""
import pyeapi
import json
from json import dumps, load
switches=['mt701','mt702','mt703','mt704']      #SPECIFYING THE HOSTNAMES OF SWITCHES FOR WHICH THE SPANNING-TREE WILL BE DRAWN"
shspan={}
shlldpne={}
switchport={}
roles=[]
ports={}
lldp={}
list2=[]
filenames={}
portsdummyfiles={}
instances=[]

n=0
spanoutputtxt=[]
portsdummy=[]

fo = open("physical_topology.json","w")         #OPENING THE JSON OUTPUT FILE 'physical_toplogy.json', TO BE USED TO CONSTRUCT THE PHYSICAL TOPOLOGY

for x in switches:                              #FETCHING THE OUTPUT REQUIRED TO DRAW THE SPANNING-TREE USING EAPI"
   node = pyeapi.connect_to(x)
   shspan[x] = node.enable('show spanning-tree detail',encoding='json')           
   shlldpne[x] =node.enable('show lldp neighbors',encoding='json')
   switchport[x] =node.enable('show interfaces switchport',encoding='json')  
   l1=shlldpne[x][0]                            #CONSTRUCTING A DICTIONARY 'lldp', TO BE USED TO CREATE THE PHYSICAL TOPOLOGY
   l2=l1['result']
   l3=l2['lldpNeighbors']
   s1=switchport[x][0]
   s2=s1['result']
   s3=s2['switchports']
   list1=[]
   for x1 in l3:
      list1.append(x1['port'])
   del list1[-1]
   for q in list1:
      q1=0
      for x2 in s3:
        if(q==x2):
          q1=1
      if(q1!=1):
       list1.remove(q)
   ports[x]=list1
   for y in ports[x]:
       for y1 in l3:
          if(y == y1['port']):
            lldp[n]={'source1': x,'dest':y1['neighborDevice'][:5],'from1':y, 'to1':y1['neighborPort']}
            n=n+1
   shspan[x][0].update({'host': x})            #INSERTING HOSTNAME INTO DICTIONARY "shspan"
   d1=shspan[x][0]
   key1=d1['result']['spanningTreeInstances']  #CHECKING THE NUMBER INSTANCES CONFIGURED ON EACH SWITCH
   for k1 in key1:
     instances.append(k1)                      #LIST IS CREATED WITH DUPLICATE ENTRIES OF INSTANCES

instances1 = []                                #CREATING A LIST WHERE THERE ARE NO DUPLICATE ENTRIES OF INSTANCES
for i in instances:
       if i not in instances1:
          instances1.append(i)
          
lldp2 = dict(lldp)                             #MODIFYING "lldp" TO ENSURE THERE ARE NO DUPLICATE ENTERIES FOR A SINGLE PHYSICAL CONNECTION BETWEEN SWITCHES

for r1 in lldp2:
    for r2 in lldp2:
       if(r1!=r2):
         if((lldp2[r1]['dest']==lldp2[r2]['source1']) and (lldp2[r2]['dest']==lldp2[r1]['source1']) and (lldp2[r2]['to1']==lldp2[r1]['from1']) and (lldp2[r2]['from1']==lldp2[r1]['to1'])):
            if(r1<r2):
              lldp.pop(r2, None)

with open("physical_topology.json","a") as outfile:
    json.dump(lldp, outfile, indent=4)
              
l3=dict(lldp)


for i in instances1:                          #CREATING THE JSON OUTPUT FILES NEEDED TO CREATE THE FORWARDING TOPOLOGY FOR EACH INSTANCE
   file1="spanoutput"+i+".json"
   filenames[i]=file1
   fo5 = open(filenames[i], "w")
   fo5.close()
   file2="portsdummy"+i+".json"
   portsdummyfiles[i]=file2
   fo4=open(portsdummyfiles[i],"w")
   fo4.close()

for i in instances1:                         #DUMPING JSON OUTPUT FOR 'shspan' FOR ONE INSTANCE FOR ALL RELEVANT SWITCHES INTO A JSON FILE 'spanoutputMSTx.json' x-INSTANCE NO.
   spanoutputtxt[:]=[]
   
   for x in switches:
       d1=shspan[x][0]
       key1=d1['result']['spanningTreeInstances'] 

       for k1 in key1:
         d2=d1['result']['spanningTreeInstances'][k1]
         if(k1==i):
            c=0
            for d3 in d2:                    #CHECKING IF CURRENT SWITCH IS ROOT BRIDGE BY SEARCHING IF A ROOT PORT EXISTS ON THE SWITCH
                if(d3=='rootPort'):
                       c=1
            if(c==0):
               shspan[x][0].update({'host': x +":(RootBridge)"})
               rootbridge=x
      
            else:
             shspan[x][0].update({'host': x})
             rootbridge=x
             
            d5={}
            d5["host"]=shspan[x][0]["host"]
            d5["result"]={}
            d5["result"]["spanningTreeInstances"]={}
            d5["result"]["spanningTreeInstances"][i]={}
            d5["result"]["spanningTreeInstances"][i]=shspan[x][0]["result"]["spanningTreeInstances"][i]
            spanoutputtxt.append(d5)
            break
   with open(filenames[i], "a") as outfile:
           json.dump(spanoutputtxt, outfile, indent=4)
     

###################################################

#########for instance 1
for i in instances1:                      #FOR EACH INSTANCE, PORT ROLES OF EACH INTERFACE ARE FETCHED AND "lldp" IS MODIFIED TO CONTAIN THIS INFORMATION. THE PORT ROLE OF THE LOCAL AND NEIGHBORING INTERFACE ARE FETCHED.
   portsdummy[:]=[]
   lldp3=dict(l3)
   lldp=dict(l3)
   for z in lldp3:
      c1=0
      s=l3[z]['source1']
      #print s
      a = shspan[s][0]
      a1= a['result']['spanningTreeInstances']
      for a2 in a1:
         if(a2==i):
            c1=1
      if(c1==0):
         lldp.pop(z, None)
   
   lldp5=dict(lldp)
   
   for z in lldp5:
    source=lldp5[z]['source1']
    a11 = shspan[source][0]
    a12= a11['result']['spanningTreeInstances']
    for allkeys in a12:
       if(allkeys==i):  
        v = a11['result']['spanningTreeInstances'][allkeys]['interfaces']
        for v1 in v:
           if((v1==lldp5[z]['from1'])):
             if((v[v1]['role']=="alternate")):
                 lldp.pop(z, None)
             else:
               lldp[z]['roles']=v[v1]['role']
               
    lldp6 =dict(lldp)
    
   for z in lldp6:
        target=lldp6[z]['dest']
        a = shspan[target][0]
        a1= a['result']['spanningTreeInstances']
        for a2 in a1:
         if(i==a2):  
          b = a['result']['spanningTreeInstances'][a2]['interfaces']
          for b1 in b:
           #print b[b1]['role']
           if((b1==lldp6[z]['to1'])):
             if((b[b1]['role']=="alternate")):
                 lldp.pop(z, None)
             else:
              lldp[z]['rolet']=b[b1]['role']            
   
   portsdummy.append(lldp)                   
   with open(portsdummyfiles[i],"a") as outfile:
      json.dump(portsdummy, outfile, indent=4)
