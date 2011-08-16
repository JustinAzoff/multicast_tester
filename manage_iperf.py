#!/usr/bin/env python
import os
import signal
import time
import subprocess

IPERF="iperf -c 239.255.52.100 -t 14400 -u -T 3  -i 60 -b 100m -p 7000".split()

IPERF_RUNTIME = 60*10

def wait():
    try :
        os.wait()
    except:
        pass

def kill(pid):
    print "Killing iperf pid", pid
    os.kill(pid, signal.SIGTERM)
    p, status = os.waitpid(pid,os.P_NOWAIT)
    wait()

def require_iperf():
    f = open("need_iperf.dat.new",'w')
    f.write(str(cur_time()))
    f.close()
    os.rename("need_iperf.dat.new", "need_iperf.dat")

def start_iperf():
    print 'starting iperf'
    p=subprocess.Popen(IPERF,shell=False)
    print "iperf pid", p.pid
    return p.pid

def get_stored_time():
    if not os.path.exists("need_iperf.dat"):
        return 0
    f = open("need_iperf.dat")
    t = int(f.read())
    f.close()
    return t

def cur_time():
    return int(time.mktime(time.gmtime()))

def age(t):
    return cur_time() - t

def manage_iperf():
    pid = None
    while True:
        time.sleep(1)
        need_time = get_stored_time()
        if age(need_time) > IPERF_RUNTIME and pid:
            kill(pid)
            pid = None
        if age(need_time) <= IPERF_RUNTIME:
            if not pid:
                pid = start_iperf()
            else :
                p, status = os.waitpid(pid,os.P_NOWAIT)
                running = (p == 0)
                if not running:
                    pid = start_iperf()

if __name__ == "__main__":
    manage_iperf()
