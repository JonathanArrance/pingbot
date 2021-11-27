import os
import logging
import settings
import time
import multiprocessing

from pingbot_lib import Operations as op
from pingbot_lib import Prometheus as prom

#Instantiate prom
pr = prom()
o = op()

def pinghost(input_list):
    for host in input_list:
        success = o.ping(host['ip'])
        if success:
            pr.current_ping({'hostname':host['hostname'],'ip':host['ip'],'production':host['production'],'status':True})
        else:
            pr.current_ping({'hostname':host['hostname'],'ip':host['ip'],'production':host['production'],'status':False})

def main():

    pr.start_server()

    #make sure the git repo has not already been cloned
    if not os.path.exists(settings.CONFIG['GITROOT']):
        logging.warn("No gitroot directory present")

        #get the directory
        if settings.CONFIG['CLONEREPO']:
            try:
                logging.info('Cloneing the git repo %s'%(settings.CONFIG['GITURL']))
                o.git_clone()
            except Exception as e:
                logging.error('Could not clone the repo %s.'%(settings.CONFIG['GITURL']))
                logging.error(e)

    while True:
        #read in the hosts file
        try:
            #open the hosts file and read it.
            hosts_file = settings.CONFIG['GITROOT'] + settings.CONFIG['HOSTS']
            out = o.read_hosts_file(hosts_file)
        except Exception as e:
            logging.error("Could not read the hosts file.")
            logging.error(e)

        try:
            split_list = o.split_up_list(out)
        except Exception as e:
            logging.error("Could not split up the ip list.")
            logging.error(e)

        #slow things down a little - lead into multi processor support
        for chunk in split_list:
            pinghost(chunk)

        time.sleep(settings.CONFIG['INTERVAL'])

if __name__ == '__main__':
    main()