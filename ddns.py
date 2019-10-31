#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from urllib.parse import urlencode
import requests
import socket
import time
import fcntl
import struct
import os
import sys
 
def dp_dns(token_id, token_key, domain, record, ip):
    api_url = 'https://dnsapi.cn/'
    global_params = { 'login_token': '%d,%s' % (token_id, token_key),
        'format': 'json'
    }
    headers = {"Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/json"}
    global_params.update({'domain': domain})
    records = requests.post(api_url + 'Record.List', data=urlencode(global_params),
        headers=headers).json()
    record_id = [ i['id'] for i in records['records'] if i['name'] == record ][0]
    global_params.update({ 'record_id': record_id,
        'sub_domain': record,
        'record_line_id': 0,
        'value': ip
    })
    result = requests.post(api_url + 'Record.Ddns',
        data=urlencode(global_params), headers=headers)
    return result.status_code == 200

def cf_dns(token_id, token_key, domain, record, ip):
    api_url = 'https://api.cloudflare.com/client/v4/'
    params = {'name': domain,
        'status': 'active'}
    headers = {'Authorization': 'Bearer %s' % token_key,
        'Content-Type': 'application/json'}
    domains = requests.get(api_url + 'zones', params=params, headers=headers).json()
    domain_id = domains['result'][0]['id']

    params = {'type': 'A', 'name': record}
    records = requests.get(api_url + 'zones/%s/dns_records' % domain_id,
        params=params, headers=headers).json()
    record_id = records['result'][0]['id']

    data = {'type': 'A', 'name': record, 'content': ip}
    result = requests.put(api_url + 'zones/%s/dns_records/%s' % (domain_id, record_id),
        json=data, headers=headers)
    return result.status_code == 200
 
def get_public_ip():
    ip = requests.get('https://z.xdays.me/cip').text.strip('\n')
    return ip

def get_local_ip():
    '''get ip address from default route interface'''
    f = open('/proc/net/route')
    for i in f:
        s = i.split('\t')
        if s[1] == '00000000':
            iface = s[0]
            break
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl( 
        s.fileno(), 
        0x8915,  # SIOCGIFADDR 
        struct.pack('256s', iface[:15]) 
    )[20:24])

def get_env(var_name, default):
    return os.environ.get(var_name, default)
 
if __name__ == '__main__':
    envs = ['PROVIDER', 'TOKEN_ID', 'TOKEN_KEY', 'DOMAIN', 'RECORD', 'IP_TYPE']
    current_file = '/tmp/current'
    for env in envs:
        if env in os.environ:
            exec('%s="%s"' % (env, get_env(env, None)))
        else:
            print('%s is required' % env)
            sys.exit(1)
    if  os.path.exists(current_file):
        with open(current_file, 'r') as f:
            current_ip = f.read()
    else:
        current_ip = None
 
    if IP_TYPE == 'public':
        ip = get_public_ip()
    else:
        ip = get_local_ip()
    if current_ip != ip:
        if PROVIDER == 'dnspod':
            result = dp_dns(TOKEN_ID, TOKEN_KEY, DOMAIN, RECORD, ip)
        elif PROVIDER == 'cloudflare':
            result = cf_dns(TOKEN_ID, TOKEN_KEY, DOMAIN, RECORD, ip)
        else:
            result = None
            print('provider not support')
        if result:
            print('update %s dns record successfully' % PROVIDER)
        else:
            print('failed to update %s dns record' % PROVIDER)
        with open(current_file, 'w+') as f:
            f.write(ip)
    else:
        print('no change with ip')
