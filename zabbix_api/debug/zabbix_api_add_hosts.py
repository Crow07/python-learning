import re
import requests
import json

url = 'http://172.31.6.112/zabbix/api_jsonrpc.php'
post_header = {'Content-Type': 'application/json'}

post_auth = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "Admin",
        "password": "zabbix"
    },
    "id": 1
}

ret = requests.post(url, data=json.dumps(post_auth), headers=post_header)
zabbix_ret = json.loads(ret.text)
zabbix_auth = zabbix_ret.get('result')

post_group = {
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": {
        "output": "extend"
    },
    "auth": zabbix_auth,
    "id": 1
}
ret_group = requests.post(url, data=json.dumps(post_group), headers=post_header)
json_group = json.loads(ret_group.text)
zabbix_group = json_group.get('result')

post_template = {
    "jsonrpc": "2.0",
    "method": "template.get",
    "params": {
        "output": "extend"
    },
    "auth": zabbix_auth,
    "id": 1
}
ret_template = requests.post(url, data=json.dumps(post_template), headers=post_header)
json_template = json.loads(ret_template.text)
zabbix_template = json_template.get('result')

#add host
f = open('E:/project/python/zabbix_api/ips')
for line in f:
    dic =re.split(r'[",",\n]',line)
    ip = dic[1]
    hostname = dic[0]
    cpuInfo = dic[4]
    cpuFreq = dic[5]
    cpuNum = dic[6]
    vender = dic[7]
    model = dic[8]
    groupname = dic[9]
    templatename = dic[10]
    for group in zabbix_group:
        if group["name"] == groupname:
            groupid = group["groupid"]
    for template in zabbix_template:
        if template["name"] == templatename:
            templateid = template["templateid"]
    post_add_host = {
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": hostname,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": groupid
            }
        ],
        "templates": [
            {
                "templateid": templateid
            }
        ],
        "inventory_mode": 0,
        "inventory": {
            "macaddress_a": cpuInfo,
            "macaddress_b": cpuFreq
        }
    },
    "auth": zabbix_auth,
    "id": 1
    }

    host_result = requests.post(url, data=json.dumps(post_add_host), headers=post_header)
    print host_result
    print "create sucessful %s" % (hostname)