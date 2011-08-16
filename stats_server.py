#!/usr/bin/env python
try:
    import json
except:
    import simplejson as json

import os
from bottle import Bottle, run, request, response, redirect, request, abort, json_dumps
from bottle import mako_view as view
import bottle
template_dir = os.path.join(os.path.dirname(__file__), "templates")
bottle.TEMPLATE_PATH.insert(0, template_dir)

#bottle.debug(True)
app = Bottle()

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("stats-server")

#db stuff
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, DateTime, Float, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import func
import datetime

engine = create_engine('sqlite:///stats.db', echo=False)

metadata = MetaData()
stats = Table('stats', metadata,
    Column('id', Integer, primary_key=True),
    Column('idx', Integer),
    Column('time', DateTime),
    Column('ip', String(25)),
    Column('kbytes', Integer),
    Column('mbits', Float),
    Column('pps', Float),
)
try:
    metadata.create_all(engine) 
except:
    pass
#########

def log_stats(ip, time, kbytes, mbits, pps=None, idx=None):
    log.info("%d %s got %d kbytes - %0.2f mbits %s pps" % (idx, ip, kbytes, mbits, pps))
    conn = engine.connect()
    conn.execute(
        stats.insert().values(time=time, ip=ip, kbytes=kbytes, mbits=mbits, pps=pps, idx=idx)
    )

def get_stats():
    conn = engine.connect()
    return conn.execute("SELECT ip, max(time) as last, count(1) as samples, min(mbits) as min, max(mbits) as max, avg(mbits) as avg from stats group by ip order by max DESC")

def get_stats_for_ip(ip):
    conn = engine.connect()
    return conn.execute(stats.select(stats.c.ip==ip).order_by(stats.c.time.desc()))

import manage_iperf
@app.route("/hello")
def hello():
    manage_iperf.require_iperf()
    return "hello"

@app.post("/send")
def send():
    ip = request.environ['REMOTE_ADDR']
    mbits = float(request.POST.get("mbits"))
    time = float(request.POST.get("time"))
    time = datetime.datetime.fromtimestamp(time)
    kbytes = int(request.POST.get("kbytes"))
    log_stats(ip, time, kbytes, mbits)
    return "ok"

@app.post("/send_stats")
def send_stats():
    ip = request.environ['REMOTE_ADDR']
    data = request.body.read()
    items = json.loads(data)
    for item in items:
        time = datetime.datetime.fromtimestamp(item['time'])
        kbytes = item['kbytes']
        mbits = item['mbits']
        pps = item.get('pps', None)
        idx = item['idx']
        log_stats(ip, time, kbytes, mbits, pps, idx)
    return "ok"

@app.route("/")
@view("index.mako")
def index():
    return dict(stats=get_stats())

@app.route("/ip/:ip")
@view("ip.mako")
def ip_info(ip):
    return dict(stats=get_stats_for_ip(ip), title=ip)

def main():
    run(app, host='0.0.0.0',server='auto', port=7001)

if __name__ == "__main__":
    main()
