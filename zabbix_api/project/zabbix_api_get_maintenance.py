# -*- coding:utf-8 -*-

import json
import urllib2
from urllib2 import URLError
from zabbix_api_get_authid_project import Zabbix_Auth

Authid = str(Zabbix_Auth().user_login())

class Zabbix_Get_Maintenance:
    def __init__(self):
        self.url = 'http://172.31.6.112/zabbix/api_jsonrpc.php'
        self.header = {"Content-Type": "application/json"}

    def Maintenance_Info(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "maintenance.get",
            "params": {
                "output": "extend",
                "selectGroups": "extend",
                "selectTimeperiods": "extend"
            },
            "auth": Authid,
            "id": 1
        })

        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "\033[041m authenticate is failed, please check it !\033[0m", e.code
        else:
            response = json.loads(result.read())
            result.close()
            self.maintenanceinfo = response['result']
            return self.maintenanceinfo
    def Maintenance_Check_List(self):
        A =  Zabbix_Get_Maintenance()
        print "----maintenance List----"
        print "ID: ","MaintenanceName"
        for i in A.Maintenance_Info():
            print i["maintenanceid"],":",i["name"]
        print "----maintenance List----"