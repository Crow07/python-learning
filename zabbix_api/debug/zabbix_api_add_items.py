import requests
import json

url = 'http://172.31.4.128/zabbix_api/api_jsonrpc.php'
post_data =  {
     "jsonrpc": "2.0",
     "method": "host.get",
     "params": {
		"output": [
			"hostid",
			"host"],
		"selectInterfaces":[
			"ip",
			"interfaceid"
			]
     },
     "auth": "76078a0e878c0d4e874966a6d54e2c71",
     "id": 1
 }
post_header = {'Content-Type': 'application/json'}

ret = requests.post(url, data=json.dumps(post_data), headers=post_header)

zabbix_ret = json.loads(ret.text)
zabbix_result = zabbix_ret.get('result')
print zabbix_result
n = int
for n in zabbix_result:
    host_id = n['hostid']
    interface_id = n['interfaces'][0]['interfaceid']
    post_create_items_forall = {
        "jsonrpc": "2.0",
        "method": "item.create",
        "params": {
            "name": "test for add item to all host",
            "key_": "test_item_forall",
            "hostid": host_id,
            "type": 0,
            "value_type": 4,
            "interfaceid": interface_id,
            "delay": 60
        },
        "auth": "76078a0e878c0d4e874966a6d54e2c71",
        "id": 3
    }
    create_item_ret = requests.post(url, data=json.dumps(post_create_items_forall), headers=post_header)
    zabbix_create_item_ret = json.loads(create_item_ret.text)
    print zabbix_create_item_ret