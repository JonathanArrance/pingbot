import os
import logging
import re
import settings
from git import Repo
from pythonping import ping
from prometheus_client import start_http_server
from prometheus_client import Gauge
from prometheus_client import Counter

class Operations():
    
    def __init__(self):
        self.split = settings.CONFIG['SPLITFACTOR']
        self.giturl = settings.CONFIG['GITURL']
        self.gitroot = settings.CONFIG['GITROOT']
    
    def git_clone(self,input_dict={}):
        if len(input_dict) > 0:
            try:
                Repo.clone_from(input_dict['giturl'], input_dict['gitroot'], recursive=True)
            except Exception as e:
                logging.error(e)
                raise e
        else:
            try:
                Repo.clone_from(self.giturl, self.gitroot, recursive=True)
            except Exception as e:
                logging.error(e)
                raise e
    
    def split_up_list(self,input_list):
        """
        DESC: Chunk up the list of IP and hosts
        INPUT: input_list - list of dict - ip
                                         - host
        OUTPUT: out_list - list of lists
        NOTE:
        """
        try:
            logging.info("Splitting up the list of hosts and IPs.")
            return [input_list[i:i + self.split] for i in range(0, len(input_list), self.split)]
        except Exception as e:
            logging.error("Could not split up the host ip list.")
            logging.error(e)

    def read_hosts_file(self,host_file):
        """
        DESC: return a list of ip and hostname dictionaries from a unix style hosts file.
        INPUT: host_file - fully qualified path to file
        OUTPUT: out_list of dict - ip
                                 - hostname
        NOTE: Get rid of the cruft in the file
        """
        comment = "#+"
        local = "localhost+"
        colon = "^:+"
        blank = "\s+"
        valid_ip = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        nonprodhost = "empty+"
        out = []
        
        try:
            file = open(host_file,'r')
            for line in file.readlines():
                out_dict = {}
                if(re.search(comment,line) or re.search(local,line) or re.search(colon,line)):
                    continue
                else:
                    try:
                        line = line.strip().split()

                        #check for blank lines and ignore
                        if len(line) == 0:
                            continue

                        if(re.search(valid_ip,line[0])):
                            out_dict = {'ip':line[0],'hostname':line[1],'production':True}
                        else:
                            out_dict = {'ip':line[1],'hostname':line[0],'production':True}
                    except Exception as e:
                        logging.error(e)
                        print(e)

                    if re.search(nonprodhost,out_dict['hostname']):
                        out_dict['production'] = False
                    
                    out.append(out_dict)

        except IOError as i:
            logging.error('Could not open the file %s'%host_file)
            raise i

        return out
    
    def ping(self,ip):
        """
        DESC: Ping the host to see if it is on the network
        INPUT: ip - ip of the target host
        OUTPUT: False or Round trip time.
        NOTE: True if 
        """
        try:
            pinghost = os.system("ping -c 1 %s > /dev/null 2>&1"%(str(ip)))
        except Exception as e:
            logging.error('Could not ping the host %s.'%ip)
            raise e
        
        if pinghost == 0:
            return True
        else:
            #return True and the round trip time
            return False

class Prometheus():
    
    def __init__(self):
        logging.info("Starting Prometheus scrape endpoint")
        #start_http_server(9002)

    def start_server(self):
        start_http_server(9002)
        self.total_success = Counter('pingbot_total_success','Pingbot total successful ping',['hostname','ip','production'])
        self.total_fail = Counter('pingbot_total_fail','Pingbot total failed ping',['hostname','ip','production'])
        self.ping = Gauge('pingbot_ping', 'The current Pingbot ping job.',['hostname','ip','production'])
    
    def current_ping(self,input_dict):
        """
        DESC: Emit the current ping success
        INPUT: input_dict - hostname - hostname
                                     - ip     - ip address
                                     - status - True/False
                                     - production
        OUTPUT: None
        NOTE: This is a Gauge
        """
        print(input_dict)
        status = 0.0
        if input_dict['status'] == True:
            status = 1.0
        try:
            logging.info("Emitting ping metrics.")
            self.ping.labels(input_dict['hostname'],input_dict['ip'],input_dict['production']).set(status)
            self.total_success.labels(input_dict['hostname'],input_dict['ip'],input_dict['production']).inc()
        except Exception as e:
            self.ping.total_fail(input_dict['hostname'],input_dict['ip'],input_dict['production']).inc()
            logging.error(e)
            logging.error("Could not emit the ping metric.")