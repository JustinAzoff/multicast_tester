#!/usr/bin/env python
import os
from bottle import Bottle, run, request, response, redirect, request, abort, json_dumps
from bottle import mako_view as view
import bottle
template_dir = os.path.join(os.path.dirname(__file__), "templates")
print 'template_dir', template_dir
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

engine = create_engine('sqlite:///stats.db', echo=False)

metadata = MetaData()
stats = Table('stats', metadata,
    Column('id', Integer, primary_key=True),
    Column('time', DateTime),
    Column('ip', String(25)),
    Column('kbytes', Integer),
    Column('mbits', Float),
)
try:
    metadata.create_all(engine) 
except:
    pass
#########

def log_stats(ip, kbytes, mbits):
    log.info("%s got %d kbytes - %0.2f mbits" % (ip, kbytes, mbits))
    conn = engine.connect()
    conn.execute(
        stats.insert().values(time=func.now(), ip=ip, kbytes=kbytes, mbits=mbits)
    )

def get_stats():
    conn = engine.connect()
    return conn.execute(stats.select().order_by(stats.c.time.desc()))

@app.post("/send")
def send():
    ip = request.environ['REMOTE_ADDR']
    mbits = float(request.POST.get("mbits"))
    kbytes = int(request.POST.get("kbytes"))
    log_stats(ip, kbytes, mbits)
    return "ok"

@app.route("/")
@view("index.mako")
def index():
    return dict(stats=get_stats())

def main():
    run(app, host='0.0.0.0',server='auto', port=7001)

if __name__ == "__main__":
    main()
