import requests
import json

url = 'http://172.31.4.128/zabbix_api/api_jsonrpc.php'
post_create_group = {
    "jsonrpc": "2.0",
    "method": "hostgroup.create",
    "params": {
        "name": "test for api"
    },
    "auth": "76078a0e878c0d4e874966a6d54e2c71",
    "id": 1
}
post_header = {'Content-Type': 'application/json'}

ret = requests.post(url, data=json.dumps(post_create_group), headers=post_header)

zabbix_ret = json.loads(ret.text)

print zabbix_ret