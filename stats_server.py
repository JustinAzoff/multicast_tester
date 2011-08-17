#!/usr/bin/env python
try:
    import json
except:
    import simplejson as json

import os
from bottle import Bottle, run, request, response, redirect, request, abort, json_dumps, static_file
from bottle import mako_view as view
import bottle
template_dir = os.path.join(os.path.dirname(__file__), "templates")
bottle.TEMPLATE_PATH.insert(0, template_dir)

#bottle.debug(True)
app = Bottle()

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger("stats-server")

#db stuff
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, DateTime, Float, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import mapper, relationship, sessionmaker
import datetime

engine = create_engine('sqlite:///stats.db', echo=False)
Session = sessionmaker(bind=engine)

metadata = MetaData()
stats = Table('stats', metadata,
    Column('id', Integer, primary_key=True),
    Column('test_id', None, ForeignKey('test_runs.id')),
    Column('idx', Integer),
    Column('time', DateTime),
    Column('ip', String(25)),
    Column('kbytes', Integer),
    Column('mbits', Float),
    Column('pps', Float),
    Column('dups', Integer),
    Column('delay', Float),
)
test_runs = Table('test_runs', metadata,
    Column('id', Integer, primary_key=True),
    Column('time', DateTime),
    Column('ip', String(25)),
    Column('kbytes', Integer),
    Column('mbits', Float),
    Column('pps', Float),
    Column('dups', Integer),
    Column('delay', Float),
)
try:
    metadata.create_all(engine) 
except:
    pass

class Base(object):
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

class Stat(Base):
    pass

class Test(Base):
    pass

mapper(Stat, stats)

mapper(Test, test_runs, properties={
    'stats':relationship(Stat, order_by=stats.c.idx, backref="test")
})
def avg(items):
    items = list(items)
    return sum(items) / len(items)
#########

def log_stats(ip, time, kbytes, mbits, delay=None, dups=None, pps=None, idx=None):
    log.info("%d %s got %d kbytes - %0.2f mbits %s pps %s dups %0.3f delay" % (idx, ip, kbytes, mbits, pps, dups, delay))
    s = Stat(time=time, ip=ip, kbytes=kbytes, mbits=mbits, pps=pps, idx=idx, dups=dups, delay=delay)
    return s

def get_stats():
    session = Session()
    return session.query(Test).order_by(Test.time.desc())

def get_machines():
    return engine.execute("select count(distinct(ip)) from test_runs").scalar()

def get_stats_for_ip(ip):
    session = Session()
    return session.query(Test).filter_by(ip=ip).order_by(Test.time.desc())

def update_stats(test):
    stats = test.stats
    test.kbytes = sum(s.kbytes for s in stats if s.kbytes)
    test.mbits = avg(s.mbits for s in stats if s.mbits)
    test.dups = sum(s.dups for s in stats if s.dups)
    test.pps = avg(s.pps for s in stats if s.pps)
    delays = [s.delay for s in stats if s.delay]
    if delays:
        test.delay = max(delays) - min(delays)

def insert_items(ip, items):
    session = Session()
    if items:
        test = Test(ip=ip,time=datetime.datetime.now())
        session.add(test)
    for item in items:
        time = datetime.datetime.fromtimestamp(item['time'])
        kbytes = item['kbytes']
        mbits = item['mbits']
        pps = item.get('pps', None)
        dups = item.get('dups', None)
        delay = item.get('delay', None)
        idx = item['idx']
        stat = log_stats(ip, time, kbytes, mbits, delay, dups, pps, idx)

        stat.test=test
        session.add(stat)

    update_stats(test)

    session.commit()

import manage_iperf
@app.route("/hello")
def hello():
    ip = request.environ['REMOTE_ADDR']
    log.info("Starting test for ip=%s" % ip)
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
    insert_items(ip, items)
    return "ok"

@app.route("/")
@view("index.mako")
def index():
    return dict(stats=get_stats(), machines=get_machines())

@app.route("/ip/:ip")
@view("ip.mako")
def ip_info(ip):
    return dict(tests=get_stats_for_ip(ip), title=ip)

@app.route("/test/:id")
@view("test.mako")
def test_info(id):
    session = Session()
    test = session.query(Test).get(id)
    stats = test.stats
    return dict(test=test, title=test.ip)

@app.route('/static/jquery.tablesorter.min.js')
def tablesort():
    return static_file('jquery.tablesorter.min.js', root='./')


def main():
    run(app, host='0.0.0.0',server='auto', port=7001)

if __name__ == "__main__":
    main()
