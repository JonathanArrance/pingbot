#!/bin/python
import os
import socket
import time
import calendar

#git URL
GITURL = os.getenv('GITURL',None)

#Should the repo get cloned
CLONEREPO = os.getenv('CLONEREPO',False)
if type(CLONEREPO) != 'bool':
    #need to get an ignore case operation here
    if CLONEREPO== 'False':
        CLONEREPO = False
    else:
        CLONEREPO = True

#hostname
HOSTNAME = socket.gethostname()

#Git Username
GITUSER = os.getenv('GITUSER',None)

#GIT user token. Needs to be generated in Git or can be plain password.
GITTOKEN = os.getenv('GITTOKEN',None)

#GIT root direcrtory. Directory where git clones repos to
GITROOT = os.getenv('GITROOT',os.environ['HOME'])

#ip file name path within the gitroot
HOSTS = os.getenv('HOSTS',None)

#The time interval in seconds
INTERVAL = os.getenv('INTERVAL',10)
INTERVAL = int(INTERVAL)

#How many chunks to split Hosts list into
#Each chunk will have 20 hosts in it.
SPLITFACTOR = os.getenv('SPLITFACTOR',20)
SPLITFACTOR = int(SPLITFACTOR)

CONFIG = {  'GITURL':GITURL,
            'HOSTNAME':HOSTNAME,
            'GITUSER':GITUSER,
            'GITTOKEN':GITTOKEN,
            'GITROOT':GITROOT,
            'HOSTS':HOSTS,
            'CLONEREPO':CLONEREPO,
            'INTERVAL':INTERVAL,
            'SPLITFACTOR':SPLITFACTOR
            }