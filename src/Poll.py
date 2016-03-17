# coding: utf-8
from Fidelix import *
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta
import os
import logging
logging.basicConfig()

config = {
    'interval': int(os.environ.get('POLL_INTERVAL',15)),
    'fidelix_user': os.environ.get('FIDELIX_USER','user'),
    'fidelix_password': os.environ.get('FIDELIX_PASSWORD','pass'),
    'mqtt_host': os.environ.get('MQTT','192.168.99.100'),
    'mqtt_topic_stem': os.environ.get('MQTT_TOPIC','/fidelix/'),
    'verbose': (os.environ.get('VERBOSE','True') == 'True')
}

sched = BlockingScheduler()
print('type=info msg="polling scheduled" interval=%s verbose=%s' % (str(config['interval']), config['verbose'] ))

service = Fidelix()
service.host = config['mqtt_host']
service.stem = config['mqtt_topic_stem']
service.verbose = config['verbose']
print('type=info msg="mqtt configured" host=' + config['mqtt_host'])

@sched.scheduled_job('interval', seconds=config['interval'])
def poll_data():
    print('type=info msg="polling fidelix" time="%s"' % datetime.now())
    service.login(user=config['fidelix_user'],password=config['fidelix_password'])
    service.read_value()


# Start the schedule
sched.start()
