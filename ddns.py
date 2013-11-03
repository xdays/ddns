#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import httplib, urllib
import socket
import time
import fcntl
import struct
 
type = 'public' #type of ip address, public or private
params = dict(
    login_email="email", # replace with your email
    login_password="pass", # replace with your password
    format="json",
    domain_id=100, # replace with your domain_od, can get it by API Domain.List
    record_id=100, # replace with your record_id, can get it by API Record.List
    sub_domain="pi", # replace with your sub_domain
    record_line="默认",
)
current_file = open('./current', 'r')
current_ip = current_file.read()
current_file.close()
 
def ddns(ip):
    params.update(dict(value=ip))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept":
"text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", "/Record.Ddns", urllib.urlencode(params), headers)
    
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    conn.close()
    return response.status == 200
 
def get_public_ip():
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
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
 
if __name__ == '__main__':
    try:
        if type == 'public':
            ip = get_public_ip()
        else:
            ip = get_local_ip()
        print ip
        if current_ip != ip:
            if ddns(ip):
                current_file = open('./current', 'w+')
                current_file.write(ip)
                current_file.close()
    except Exception, e:
        print e
        pass
