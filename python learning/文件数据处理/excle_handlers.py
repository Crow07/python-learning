# -*- coding:utf-8 -*-
import xlrd


url = 'http://172.31.6.112/zabbix/api_jsonrpc.php'
header = {"Content-Type": "application/json"}

def read_excle():
    inpath = '.\你好.xlsx'
    uipath = unicode(inpath, "utf8")
    workbook = xlrd.open_workbook(uipath)
    #print str(workbook.sheet_names()).decode("unicode_escape").encode("utf8")
    #print workbook.sheet_names()[0]
    #sheet2_name = workbook.sheet_names()[0]
    #sheet2 = workbook.sheet_by_index(3,3)
    #sheet2 = workbook.sheet_by_name('网络设备')
    #print sheet2.name, sheet2.nrows, sheet2.ncols
    #print sheet2.cell(1,0).value.encode('utf-8')
    #print sheet2.cell_value(1,1).encode('utf-8')
    #print sheet2.row(1)[2].value.encode('utf-8')
    #print sheet2.cell(1, 0).ctype
    network_name = "网络设备"
    unetwork_name = unicode(network_name,"utf8")
    compute_name = "计算节点"
    ucompute_name = unicode(compute_name,"utf8")
    storage_name = "存储设备"
    ustorage_name = unicode(storage_name,"utf8")
    print "0 : ","计算节点"
    print "1 : ","网络设备"
    print "2 : ","存储设备"
    input_node = input("Please choose node: ")
    key_list = ["计算节点","网络设备","存储设备"]
    uname = unicode(key_list[input_node],'utf8')
    table = workbook.sheet_by_name(uname)
    nrows = table.nrows
    for i in range(2,nrows):
        if "empty" in str(table.row(i)[2]):
            continue
        elif uname == ucompute_name:
            hostname = str(table.row(i)[2]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]
            ip = str(table.row(i)[3]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]
            cpuinfo1 = str(table.row(i)[6]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]
            cpuinfo2 = str(table.row(i)[7]).decode("unicode_escape").encode("utf8").strip("'").split(":")[1]
            vendor = str(table.row(i)[8]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]
            model = str(table.row(i)[9]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]


            data = json.dumps({
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
                        },
                        {
                            "type": 2,
                            "main": 1,
                            "useip": 1,
                            "ip": ip,
                            "dns": "",
                            "port": "161"
                        }
                    ],
                    "groups": [
                        {
                            "groupid": Input_Groupid
                        }
                    ],
                    "templates": [
                        {
                            "templateid": Input_Templateid
                        }
                    ],
                    "inventory_mode": 0,
                    "inventory": {
                        "software_app_a": cpuinfo1,
                        "software_app_b": cpuinfo2,
                        "vendor": vender,
                        "model": model
                    }
                },
                "auth": Authid,
                "id": 1
            })
            request = urllib2.Request(url, data)
            for key in header:
                request.add_header(key, header[key])
            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                print "\033[041m authenticate is failed, please check it !\033[0m", e.code
            else:
                response = json.loads(result.read())
                result.close()
                if "error" in response:
                    print response["error"]["data"]
                else:
                    hostsinfo = response['result']
                    print hostsinfo
        elif uname == unetwork_name:
            hostname = str(table.row(i)[2]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]
            ip = str(table.row(i)[3]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]
            vendor = str(table.row(i)[6]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]
            model = str(table.row(i)[7]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]

            data = json.dumps({
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
                        },
                        {
                            "type": 2,
                            "main": 1,
                            "useip": 1,
                            "ip": ip,
                            "dns": "",
                            "port": "161"
                        }
                    ],
                    "groups": [
                        {
                            "groupid": Input_Groupid
                        }
                    ],
                    "templates": [
                        {
                            "templateid": Input_Templateid
                        }
                    ],
                    "inventory_mode": 0,
                    "inventory": {
                        "vendor": vender,
                        "model": model
                    }
                },
                "auth": Authid,
                "id": 1
            })
            request = urllib2.Request(url, data)
            for key in header:
                request.add_header(key, header[key])
            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                print "\033[041m authenticate is failed, please check it !\033[0m", e.code
            else:
                response = json.loads(result.read())
                result.close()
                if "error" in response:
                    print response["error"]["data"]
                else:
                    hostsinfo = response['result']
                    print hostsinfo
        elif uname == ustorage_name:
            hostname = str(table.row(i)[2]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]
            ip = str(table.row(i)[3]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]
            vendor = str(table.row(i)[6]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]
            model = str(table.row(i)[7]).decode("unicode_escape").encode("utf8").strip("'").split(":u'")[1]
            data = json.dumps({
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
                        },
                        {
                            "type": 2,
                            "main": 1,
                            "useip": 1,
                            "ip": ip,
                            "dns": "",
                            "port": "161"
                        }
                    ],
                    "groups": [
                        {
                            "groupid": Input_Groupid
                        }
                    ],
                    "templates": [
                        {
                            "templateid": Input_Templateid
                        }
                    ],
                    "inventory_mode": 0,
                    "inventory": {
                        "vendor": vender,
                        "model": model
                    }
                },
                "auth": Authid,
                "id": 1
            })
            request = urllib2.Request(url, data)
            for key in header:
                request.add_header(key, header[key])
            try:
                result = urllib2.urlopen(request)
            except URLError as e:
                print "\033[041m authenticate is failed, please check it !\033[0m", e.code
            else:
                response = json.loads(result.read())
                result.close()
                if "error" in response:
                    print response["error"]["data"]
                else:
                    hostsinfo = response['result']
                    print hostsinfo
        else:
            print "input error"
            break

        #if table.row(i)[1].value == ""
    #for i in range(nrows):
        #print str(table.row_values(i)).decode("unicode_escape").encode("utf8")
read_excle()


