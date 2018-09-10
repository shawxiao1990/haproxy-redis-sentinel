#!/usr/bin/env python
import redis
import fileinput
import  os,re,sys
from subprocess import call
from redis.sentinel import Sentinel
sentinel1=os.getenv('haproxy_sentinel1')
sentinel2=os.getenv('haproxy_sentinel2')
sentinel3=os.getenv('haproxy_sentinel3')
sentinel_port=os.getenv('sentinel_port')
sentinel = Sentinel([(sentinel1, sentinel_port),
                     (sentinel2, sentinel_port),
                     (sentinel3, sentinel_port)
		     ],
                    socket_timeout=0.5)
master=str(sentinel.discover_master('mymaster'))
master_ip= master.strip('()').split(',')[0]
master_port= master.strip('()').split(',')[1].strip()
master= master_ip.strip('\'')+':'+ master_port
conf= "haproxy.cfg"
haproxy_ip=''
master_ip_port="    " + "server redis1" + " " + master + " " +  "check inter 1s"
with open(conf,'r') as ha:
    for line in ha:
        line = line.strip('\n')
        if re.match('\s+server',line):    
           backend_name = re.split('\s+',line)
           server_name=[]
           server_name.append(backend_name)
           haproxy_ip= server_name[0][3]


def file_insert(fname, str):
        r = 'redis1'
        f = open(fname)
        old = f.read()
        num = int(re.search(r, old).start())
        f_input = fileinput.input(fname, inplace=1)
        #for line in fileinput.input(fname, inplace=1):
        for line in f_input:
            if r in line:
                print line.replace(line,str)
                print f.read()
                break
            else:
                print line.rstrip()
        f.close()
        f_input.close()

def rebot_haproxy():
    cmd1="killall nginx"
    call(cmd1,shell=True)
    cmd2="systemctl start nginx"
    call(cmd2,shell=True)
    
if master == haproxy_ip:
   pass
else:
   file_insert(conf,master_ip_port)
   rebot_haproxy()
