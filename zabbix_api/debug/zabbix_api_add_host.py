import requests
import json

url = 'http://172.31.4.128/zabbix_api/api_jsonrpc.php'
post_create_group = {
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": "test_api1",
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": "10.0.0.0",
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": "50050"
            }
        ],
        "templates": [
            {
                "templateid": "20045"
            }
        ],
        "inventory_mode": 0,
        "inventory": {
            "macaddress_a": "01234",
            "macaddress_b": "56768"
        }
    },
    "auth": "038e1d7b1735c6a5436ee9eae095879e",
    "id": 1
}
print json.dumps(post_create_group)

post_header = {'Content-Type': 'application/json'}

ret = requests.post(url, data=json.dumps(post_create_group), headers=post_header)

zabbix_ret = json.loads(ret.text)

print zabbix_ret