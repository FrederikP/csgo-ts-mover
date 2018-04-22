import logging
from logging.config import dictConfig
from sys import exit

import ts3
import yaml
from flask import Flask, request

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'stdout': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['stdout']
    }
})

logger = logging.getLogger(__name__)

with open('ts-mover-service-config.yaml') as config_file:
    config = yaml.load(config_file)

def init_ts3_conn(ts3conn):
    try:
       ts3conn.login(
           client_login_name=config['ts3_query_login_name'],
           client_login_password=config['ts3_query_login_password']
       )
    except ts3.query.TS3QueryError:
       logger.fatal("Login failed.", exc_info=True)
       exit(1)

    ts3conn.use(port=config['ts3_port'])

ct_cid = config['channel_ids']['ct']
t_cid = config['channel_ids']['t']
lobby_cid = config['channel_ids']['lobby']

steam_to_ts_mapping = config['steam_to_ts_mapping']

app = Flask('ts-mover')

logger.info('TS Mover is running')

def move_to(steam_ids, ts_cid):
    with ts3.query.TS3Connection(config['ts3_host'], config['ts3_query_port']) as ts3conn:
        init_ts3_conn(ts3conn)
        for steam_id in steam_ids:
            if steam_id not in steam_to_ts_mapping:
                logger.warning('Need TS mapping for steam id: %s', steam_id)
                continue
            cluid = steam_to_ts_mapping[steam_id]
            clid_result = ts3conn.clientgetids(cluid=cluid)
            if not clid_result:
                logger.warning('Did not find active client for cluid %s. Not logged in?', cluid)
                continue
            clid = clid_result[0]['clid']
            info = ts3conn.clientinfo(clid=clid)[0]
            if info['cid'] != ts_cid:
                nickname = info['client_nickname']
                logger.info('Moving %s to other channel', nickname)
                ts3conn.clientmove(cid=ts_cid, clid=clid)


@app.route("/teams", methods=['POST'])
def update():
    data = request.get_json(force=True)
    ts = data['ts']
    cts = data['cts']
    num = len(ts) + len(cts)
    if num >= config['lobby_threshold']:
        move_to(ts, t_cid)
        move_to(cts, ct_cid)
    else:
        move_to(ts+cts, lobby_cid)

    return 'success'
