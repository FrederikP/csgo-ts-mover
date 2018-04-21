from flask import Flask, request
from sys import exit
import json
import ts3


with open('ts-mover-service-config.json') as config_file:
    config = json.load(config_file)

ct_cid = None
t_cid = None

def init_ts3_conn(ts3conn):
    try:
       ts3conn.login(
           client_login_name=config['ts3_query_login_name'],
           client_login_password=config['ts3_query_login_password']
       )
    except ts3.query.TS3QueryError as err:
       print("Login failed:", err.resp.error["msg"])
       exit(1)

    ts3conn.use(port=config['ts3_port'])

with ts3.query.TS3Connection(config['ts3_host'], config['ts3_query_port']) as ts3conn:
    init_ts3_conn(ts3conn)
    resp = ts3conn.channellist()
    for channel in resp:
        if channel['channel_name'] == config['channel_names']['ct']:
            ct_cid = channel['cid']
        if channel['channel_name'] == config['channel_names']['t']:
            t_cid = channel['cid']

if not ct_cid or not t_cid:
    print('Did not find CT or T ts channel')
    exit(1)

steam_to_ts_mapping = config['steam_to_ts_mapping']

app = Flask('ts-mover')

def move_to(steam_ids, ts_cid):
    with ts3.query.TS3Connection(TS3_HOST, TS3_PORT) as ts3conn:
        init_ts3_conn(ts3conn)
        clientlist = ts3conn.clientlist()
        for steam_id in steam_ids:
            if steam_id not in steam_to_ts_mapping:
                print('Need TS mapping for steam id: ' + steam_id)
                continue
            nickname = steam_to_ts_mapping[steam_id]
            clids = [client for client in clientlist if client['client_nickname'] == nickname]
            if not clids:
                print('TS nickname not found on server ' + nickname)
                continue
            clid = clids[0]['clid']
            info = [client for client in clientlist if client['clid'] == clid][0]

            if info['cid'] != ts_cid:
                print('Moving ' + nickname + ' to other channel.')
                ts3conn.clientmove(cid=ts_cid, clid=clid)


@app.route("/teams", methods=['POST'])
def update():
    data = request.get_json(force=True)
    ts = data['ts']
    cts = data['cts']
    num = len(ts) + len(cts)
    if num >= 4:
        move_to(ts, t_cid)
        move_to(cts, ct_cid)

    return 'success'
