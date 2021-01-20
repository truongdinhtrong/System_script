#!/usr/local/bin/python3.6

import os
import sys
import re
import time
import datetime
import subprocess
import json, urllib.request
from urllib.error import HTTPError

# -------------------------------


IPWhiteList = '/home/script/fw_auto/IP_whitelist.txt'
file_listIpDrop = '/home/script/fw_auto/list_ip_Drop.txt'
iptablesLog = '/logs/iptables/iptables.log'

def time_ago(min):
    # get a minute ago:
    time_check = datetime.datetime.now() - datetime.timedelta(minutes=min)
    min_ago = str(time_check.day) + " " + str(time_check.hour) + ":" + str(time_check.minute) + ":"
    return min_ago

def check_ip_country(ip):
    # Check IP location:
    domain = "https://api.ipgeolocation.io/ipgeo"
    API_KEY = "Your API key"
    url = domain + "?" + "apiKey=" + API_KEY + "&ip=" + ip
    try:
        urllib.request.urlopen(url)
    except HTTPError as err:
        if err.code == 401:
            print("urllib.error.HTTPError: HTTP Error 401: Unauthorized ... exit !!! ")
    else:
        reponse = urllib.request.urlopen(url)
        data = json.loads(reponse.read())
        reponse.close()
        output = "Country_Name: %s " % data["country_name"],"Country_Capital: %s " % data["country_capital"],"ISP: %s " % data["isp"],"Organization: %s " % data["organization"]
        return output

def fwDROP_ConnLimit():

    list_ip_in_log = []
    with open(iptablesLog, 'r') as log_iptable:
        for line in log_iptable:
            if re.findall( r'(^.*)' + str(time_ago(1)) + '(.*)CONLIMIT_15(.*)', line):
                ip = re.findall( r'SRC=[0-9]+(?:\.[0-9]+){3}', line )
                ip = [ i.strip('SRC=') for i in ip]
                list_ip_in_log.append(ip)

    IP_whitelist = []
    with open(IPWhiteList, 'r') as file_IPWhilelist:
        for line in file_IPWhilelist:
            if re.findall(r'^[0-9]+(?:\.[0-9]+){3}', line):
                ip = re.findall(r'^[0-9]+(?:\.[0-9]+){3}', line)
                IP_whitelist.append(ip)

    jump = "DROP"
    ipt_line_number = subprocess.check_output("iptables -L -vn --line-numbers|grep CONLIMIT_15|awk '{print$1}'", shell=True).decode().strip()

    #remove IP duplicate
    listIpDrop = []
    for i in list_ip_in_log:
        if i not in listIpDrop:
            listIpDrop.append(i)

    if len(listIpDrop) > 0:
        current = time.strftime('%Y:%m:%d %H-%M-%S')
        f = open(file_listIpDrop, "a+")
        f.write("Time drop IP on firewall: %s \n" % current)
        for ip in listIpDrop:
            if ip not in IP_whitelist:
                deny_ip = "/sbin/iptables -I INPUT " + ipt_line_number + " -i eth1 -s " +  ip[0] + " -j "  + jump
                os.system(deny_ip)
                f.write("IP: %s | %s \n" % (ip[0],check_ip_country(ip[0])))
        f.write("-------------------------------- \n\n")
        f.close()
    sys.exit()


# # ----------- Main ----------- # #
if __name__ == "__main__":
    # --- Deny Conntion Limit -  Limit rates:
    fwDROP_ConnLimit()






