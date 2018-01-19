#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, glob
import time
cmd = ['/bin/tar','-x','-v','-f',]

tar_file_list = glob.glob('*.tar')
for tar_file in tar_file_list:
       if os.fork():
              os.wait()
       else:
              os.execv(cmd[0], cmd + [tar_file,])

print "======Install starting======"
workdir = "/home/"
CMD_check_firewall = '/usr/sbin/getenforce'
CMD_config_firewall = ['/usr/sbin/setenforce', "0"]
CMD_config_firewall_1 = ['/usr/bin/mv',"/etc/selinux/config","/etc/selinux/config.bak"]
CMD_config_firewall_2 = ['/usr/bin/cp',workdir + "config","/etc/selinux/config.bak"]
CMD_config_firewall_3 = ['/usr/sbin/iptables',"-F"]

CMD_check_openfile = "egrep '^\*' /etc/security/limits.conf"
CMD_config_openfile = "ulimit -HSn 65535"
CMD_config_openfile_1 = "echo -e '* - nofile  65535' >> /etc/security/limits.conf"
CMD_config_openfile_2 = "echo -e 'root - nofile 100000' >> /etc/security/limits.conf"

CMD_config_time = ['/usr/bin/timedatectl','set-timezone','Asia/Shanghai']

CMD_config_yum = "mkdir -p /etc/yum.bak"
CMD_config_yum_1 = "mv /etc/yum.repos.d/* /etc/yum.bak/"
CMD_config_yum_2 = "cp /home/CentOS-local.repo /etc/yum.repos.d/"
CMD_config_yum_3 = "yum clean all"
CMD_config_yum_4 = "yum makecache"
yum_file = "/etc/yum.repos.d/CentOS-local.repo"

CMD_install_zabbix = "yum -y install zabbix-server-mysql zabbix-web-mysql zabbix-agent"
zabbix_file="/etc/zabbix/zabbix_server.conf"

CMD_install_mysql = "yum -y install mariadb mariadb-server"
CMD_stop_mysql = "systemctl stop mariadb"
CMD_Init_mysql = "mysql_install_db"
CMD_Init_mysql_1 ="chmod -R 777 /var/lib/mysql"


CMD_config_mysql = "mv /etc/my.cnf /etc/my.cnf.bak"
CMD_config_mysql_1 = "cp /home/my.cnf /etc/my.cnf"
CMD_config_mysql_2 = "mkdir -p /home/mysql"
CMD_config_mysql_3 = "chown -R mysql.mysql /home/mysql/"
CMD_start_mysql = "systemctl start mariadb"
#CMD_config_mysql_4 = "mysql -u root -e 'UPDATE mysql.user SET Password=PASSWORD('password') WHERE User='root';'"
#CMD_restart_mysql = "systemctl restart mariadb"
CMD_config_mysql_5 = "mysql  -e 'create database zabbix character set utf8 collate utf8_bin;'"
CMD_config_mysql_6 = """mysql  -e 'grant all privileges on zabbix.* to zabbix@localhost identified by "zabbix";'"""
CMD_config_mysql_7 = "zcat /usr/share/doc/zabbix-server-mysql-3.4.1/create.sql.gz | mysql zabbix"

CMD_config_httpd = "mv  /etc/httpd/conf.d/zabbix.conf /etc/httpd/conf.d/zabbix.conf.bak"
CMD_config_httpd_1 = "cp /home/zabbix.conf /etc/httpd/conf.d/zabbix.conf"

CMD_config_zabbix = "mv /etc/zabbix/zabbix_server.conf /etc/zabbix/zabbix_server.conf.bak"
CMD_config_zabbix_1 = "cp /home/zabbix_server.conf /etc/zabbix/zabbix_server.conf"

print "======Init system======"
check_firewall = os.popen(CMD_check_firewall).read().strip('\n')
check_openfile = os.popen(CMD_check_openfile).read().strip('\n')

if check_openfile != "":
	print("Info: openfile already configured")
else:
	os.popen(CMD_config_openfile)
	os.popen(CMD_config_openfile_1)
	os.popen(CMD_config_openfile_2)
	print("Info: openfile configure done!")
time.sleep(2)

os.chdir(workdir)
if check_firewall == 'Permissive':
       print("Info: selinux already closed")
else:
       os.spawnv(os.P_WAIT,CMD_config_firewall[0],CMD_config_firewall)
       os.spawnv(os.P_WAIT, CMD_config_firewall_1[0], CMD_config_firewall_1)
       os.spawnv(os.P_WAIT, CMD_config_firewall_2[0], CMD_config_firewall_2)
       os.spawnv(os.P_WAIT, CMD_config_firewall_3[0], CMD_config_firewall_3)
       print("Info: firewall configure done!")
time.sleep(2)

os.spawnv(os.P_WAIT,CMD_config_time[0],CMD_config_time)
print("Info: timezone configure done!")
time.sleep(2)

if os.access(yum_file,os.F_OK):
	print("Info: yum file is exist.")
else:
	os.popen(CMD_config_yum)
	os.popen(CMD_config_yum_1)
	os.popen(CMD_config_yum_2)
	os.popen(CMD_config_yum_3)
	os.popen(CMD_config_yum_4)
	print("Info: yum repo configure done!")
time.sleep(2)

print "======Install starting======"

if os.access(zabbix_file,os.F_OK):
	print("Info: zabbix server has been installed...")
else:
	os.popen(CMD_install_zabbix)
	print("Info: zabbix install completed.")
time.sleep(1)

os.popen(CMD_install_mysql)
os.popen(CMD_stop_mysql)
os.popen(CMD_Init_mysql)
os.popen(CMD_Init_mysql_1)
print("Info: mysql install completed.")
time.sleep(1)

print "======config starting======"
os.popen(CMD_config_mysql)
os.popen(CMD_config_mysql_1)
os.popen(CMD_config_mysql_2)
os.popen(CMD_config_mysql_3)
os.popen(CMD_start_mysql)
print "Info: mysql init done!"
#os.popen(CMD_config_mysql_4)
#os.popen(CMD_restart_mysql)
os.popen(CMD_config_mysql_5)
os.popen(CMD_config_mysql_6)
os.popen(CMD_config_mysql_7)
print("Info: zabbix database create complete.")
print("Info: mysql configure done!")
time.sleep(2)

os.popen(CMD_config_httpd)
os.popen(CMD_config_httpd_1)
print("Info:httpd configure done!")
time.sleep(1)

os.popen(CMD_config_zabbix)
os.popen(CMD_config_zabbix_1)
print("Info:zabbix configure done!")
time.sleep(1)

os.popen("systemctl restart mariadb")
os.popen("systemctl restart zabbix-server")
os.popen("systemctl restart httpd")
print("   Completed!  ")

