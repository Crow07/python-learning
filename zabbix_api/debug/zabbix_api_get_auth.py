import requests
import json

url = 'http://172.31.4.128/zabbix_api/api_jsonrpc.php'
post_data = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "Admin",
        "password": "zabbix_api"
    },
    "id": 1
}
post_header = {'Content-Type': 'application/json'}

ret = requests.post(url, data=json.dumps(post_data), headers=post_header)
zabbix_ret = json.loads(ret.text)
print zabbix_ret
if not zabbix_ret.has_key('result'):
    print 'login error'
else:
    print zabbix_ret.get('result')


