#coding=utf-8
import re
import os
import time
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
import xlrd
import xlwt
import MySQLdb
from googletrans import Translator


# configure part
job_distribution_file = "./resources/job_distribution.xlsx"
vuln_id_file = "./resources/vuln_ids.xlsx"
cnnvd_file = './resources/cnnvd_cve.txt'
output_dir = './result/'
translator = Translator(service_urls=[
    'translate.google.cn'
])
person_length = 1200

PROBLEM_COLLECT = []

def get_name_list():
    data = xlrd.open_workbook(job_distribution_file)
    table = data.sheets()[0]
    nrows = table.nrows
    name_list = []
    for row in range(1, nrows):
        name_list.append(table.cell(row, 0).value)
    return name_list


def get_vuln_id_range(name):
    data = xlrd.open_workbook(job_distribution_file)
    table = data.sheets()[0]
    nrows = table.nrows
    jid_start = 0
    jid_end = 0
    vid_list = []
    for row in range(0, nrows):
        # print table.cell(row,0).value
        if name == table.cell(row, 0).value:
            jid_start = table.cell(row, 1).value
            jid_end = table.cell(row, 2).value
    if not (jid_start and jid_end):
        print "name: %s not found, pls retry." % name
        return []
    del table
    del data
    if int(jid_start) == 1:
        # jid = 1, tag = 'id', wrong
        jid_start = 2
    print "line tag: %d -- %d" % (int(jid_start), int(jid_end))
    data = xlrd.open_workbook(vuln_id_file)
    table = data.sheets()[0]
    total_vulns = table.nrows
    if int(jid_end) > total_vulns:
        line_end = total_vulns
    else:
        line_end = int(jid_end)
    for jid in range(int(jid_start), int(line_end)+1):
        vid_list.append(int(table.cell(int(jid-1), 0).value))
    # id_start = table.cell(int(jid_start-1), 0).value
    # id_end = table.cell(int(jid_end-1), 0).value
    # print "vuln id range: %d -- %d" % (int(id_start), int(id_end))
    # return int(id_start), int(id_end)
    print "total vulns: %d" % len(vid_list)
    return vid_list


def get_vuln_infos(vid_list, fname):
    sql_pre = "SELECT * FROM 1op WHERE "
    temp = ''
    for vid in vid_list:
        temp += 'id=%d OR ' % vid
    if not temp:
        return False
    sql = sql_pre + temp[:-3]
    # sql = "SELECT * FROM 1op WHERE id>=%d AND id<=%d" % (vid_start, vid_end)
    result = do_mysql_query_action(sql)
    path = os.path.join(output_dir, fname)
    if not result:
        return False
    if os.path.exists(path):
        os.remove(path)
    
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('output')

    for row in range(len(result)):
        for col in range(len(result[row])):
            item_value = result[row][col]
            if type(item_value) == unicode and len(item_value) > 32767:
                final_value = item_value[:1000] + item_value[-1000:]
                print "WARNING: String item longer than 32767 characters." + "cutting to [:1000] + [-1000:]"
            else:
                final_value = item_value
            worksheet.write(row, col, label=final_value)
    workbook.save(path)
    return path


def do_mysql_query_action(sql):
    db_host = '172.31.10.38'
    db_user = 'hanhua'
    db_password = '123456'
    db_dbname = 'hanhuaDB'
    result = ''
    try:
        temp_conn =  MySQLdb.connect(db_host, db_user, db_password, db_dbname,
                                        use_unicode=True, charset="utf8")
        cursor = temp_conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close() 
        temp_conn.close() 
    except Exception, e:
        print "Error in save_into_mysql"
        print e.message   
    return result


def trans_excel_data(start, end, source):
    data = xlrd.open_workbook(source)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    global PROBLEM_COLLECT
    # print table.row_values(0)
    # print "total rows: " + str(nrows)
    cnnvd_dict = {}
    with open(cnnvd_file, 'r') as f:
        for line in f.readlines():
            cnnvd, cve = line.split('\t')
            cve = cve.strip('\n')
            cnnvd_dict[cve] = cnnvd

    trans_list = []
    if end > nrows:
        end = nrows
    for i in range(start, end):
        print "####### Count: " + str(i)
        vid = int(table.cell(i, 0).value)
        print "id: " + str(vid)

        oid = table.cell(i, 1).value

        name_string = table.cell(i, 2).value
        name_string = name_string.replace('\n', '').replace('  ', ' ')
        # print "name: " + name_string
        name = translate(name_string)
        if name == -1:
            PROBLEM_COLLECT.append((i+1, vid, 'name', name_string[:100]))
            name = name_string
        name = name.replace('Update for', '更新')

        cveid = table.cell(i, 3).value
        score = table.cell(i, 4).value
        # cnnvdid = table.cell(i, 5).value
        cnnvdid = get_cnnvd(cnnvd_dict, cveid)

        summary_string = table.cell(i, 6).value
        summary_string = summary_string.replace('\n', '').replace('  ', ' ')
        # print "summary: " + summary_string
        summary = translate(summary_string)
        if summary == -1:
            PROBLEM_COLLECT.append((i+1, vid, 'summary', summary_string[:100]))
            summary = summary_string
        desc_string = table.cell(i, 7).value
        desc_string = desc_string.replace('\n', '').replace('  ', ' ')
        # print "description: " + desc_string
        desc_list = desc_string.split('|')
        result = ['', '', '', '']
        solution = ''
        desc_dict = {}
        for item in desc_list:
            temp = item.split('=')
            desc_dict[temp[0].strip(' ')] = temp[1]

        if 'cvss_base_vector' in desc_dict.keys():
            result[0] = 'cvss_base_vector: ' + desc_dict['cvss_base_vector']
        else:
            result[0] = 'cvss_base_vector: ' + '无'

        if 'vuldetect' in desc_dict.keys():
            mess = translate(desc_dict['vuldetect'])
            if mess == -1:
                PROBLEM_COLLECT.append((i+1, vid, 'desc.vuldetect', desc_dict['vuldetect'][:100]))
                mess = desc_dict['vuldetect']
            result[1] = '漏洞检测方法：' + mess
        else:
            result[1] = '漏洞检测方法：' + '无'

        if 'insight' in desc_dict.keys():
            mess = translate(desc_dict['insight'])
            if mess == -1:
                PROBLEM_COLLECT.append((i+1, vid, 'desc.insight', desc_dict['insight'][:100]))
                mess = desc_dict['insight']
            result[2] = '参考：' + mess
        else:
            result[2] = '参考：' + '无'
        
        if 'affected' in desc_dict.keys():
            result[3] = '影响：' + temp[1]
        else:
            result[3] = '影响：' + '无'

        if 'solution' in desc_dict.keys():
            mess = translate(desc_dict['solution'])
            if mess == -1:
                PROBLEM_COLLECT.append((i+1, vid, 'desc.solution', desc_dict['solution'][:100]))
                mess = desc_dict['solution']
            solution = mess
        else:
            solution = '无'
        
        xref = table.cell(i, 9).value
        enabled = table.cell(i, 10).value
        version = table.cell(i, 11).value
        created = table.cell(i, 12).value
        modified = table.cell(i, 13).value
        deleted = table.cell(i, 14).value
        category = table.cell(i, 15).value
        family = table.cell(i, 16).value
        custom_risk = table.cell(i, 17).value
        cright = table.cell(i, 18).value
        bugtraq_id = table.cell(i, 19).value
        
        if '' in result or solution == '':
            print '>>>>>>>>>>>>>connectting maybe error, pls retry it.!'
            sys.exit(-1)
        else:
            trans_list.append((int(vid), oid, name, cveid, score, cnnvdid, summary, '\n'.join(result),
                               solution, xref, enabled, version, created, modified, deleted, category,
                               family, custom_risk, cright, bugtraq_id))
    return trans_list


def save_data(data_list, output):
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('output')
    for i in range(len(data_list)):
        for j in range(len(data_list[i])):
            worksheet.write(i, j, label=data_list[i][j])

    if os.path.exists(output):
        os.remove(output)
    workbook.save(output)
    print "save successed in " + output


def get_cnnvd(cnnvd_dict, cve_str):
    cnnvd_list = []
    if cve_str == 'NOCVE' or (not cve_str):
        cnnvdid_str = 'NO-CNNVD'
    else:
        for cve in cve_str.split(','):
            cve = cve.strip()
            if cve in cnnvd_dict.keys():
                cnnvd = cnnvd_dict[cve]
            else:
                cnnvd = 'NO-CNNVD'
            cnnvd_list.append(cnnvd)
        cnnvdid_str = ','.join(cnnvd_list)
    return cnnvdid_str


def translate(str_string):
    try:
        ans = translator.translate(str_string, dest='zh-cn').text
    except ValueError, e:
        print e.message
        print "**"*10 + "translate error for string---whw"
        print "translate value error, pls do it self. save in the ./temp/problem.txt"
        return -1
    except Exception, e:
        print "translate error... for: %s" % str_string
        print "connectting maybe error, pls retry it."
        print e.message
        sys.exit(-1)
    return ans


def merge_trans_xls(output_file):
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('output')
    title = ['id', 'oid', 'name', 'cve_id', 'cvssscore', 'cnnvdid',	'总结', '描述', '解决方法', '参考',
             'enabled', 'version', 'created', 'modified', 'deleted', 'category', 'family', 'custom_risk',
             'copyright', 'bugtraq_id']
    for t in range(len(title)):
        worksheet.write(0, t, label=title[t])
    for count in range(1, person_length/100+1):
        trans_file = './temp/temp_%d.xls' % ((count*100))
        if not os.path.exists(trans_file):
            continue
        data = xlrd.open_workbook(trans_file)
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        for i in range(nrows):
            for j in range(ncols):
                worksheet.write((count-1)*100+i + 1, j, label=table.cell(i, j).value)
        # break
        print "trans file %s....finished." % trans_file
    if os.path.exists(output_file):
        os.remove(output_file)
    workbook.save(output_file)
    return "success merge trans file to %s." % output_file


def vuln_info_collect(name, vid_list):
    print "save vulnerability infos into result dir...."
    time.sleep(2)
    file_name = "%s_job.xls" % name
    path = get_vuln_infos(vid_list, file_name)
    if path:
        print "save successed in %s" % path
    else:
        print "save error pls check it."
        sys.exit(-1)


def translate_and_save(name, start=1):
    print "translate and save..."
    time.sleep(2)
    path = os.path.join(output_dir, "%s_job.xls" % name)
    # print "delete temp file..."
    # os.system('rm -rf ./temp/*')
    global PROBLEM_COLLECT
    for i in range(start, person_length/100+1):
        t_result = trans_excel_data((i-1)*100, i*100, path)
        temp_file = './temp/temp_%d.xls' % (i*100)
        print "save result in temp file: %s..." % temp_file
        save_data(t_result, temp_file)
    print "translate finished, check and self audit the tempFile"
    
    print "check problem translation..."
    temp_list = []
    if PROBLEM_COLLECT:
        print "problem translation: "
        for pc in PROBLEM_COLLECT:
            print pc
            temp_list.append(str(pc))
        problem_file = os.path.join(output_dir, "%s_problem.txt" % name)
        print " problems save in %s, format: (id, vid, location, infos[:100])" % problem_file
        with open(problem_file, 'w') as f:
            f.write('\n'.join(temp_list))
    else:
        print "no problem translation, continue."
    PROBLEM_COLLECT = []


def merge_temp_result(name):
    # ans = raw_input("translate finished, continue merge?(y/n): ")
    ans = 'y'
    while ans.lower() != 'y':
        print 'use another terminal to check!'
        ans = raw_input("translate finished, continue merge?(y/n): ")
    
    output = os.path.join(output_dir, "%s_result.xls" % name)
    print "translate finished. merge into %s..." % output
    time.sleep(2)
    merge_trans_xls(output)
    
    print "最终结果存于./result/下"
    print """*_job.xls: 原始漏洞信息文档
        *_result.xls: 翻译后的合并文档
        *_problem.txt: 翻译出错文档,请自行前往translate.google.cn翻译输出
        格式：(id, vid, location, infos[:100])
        注：请进行人工复核漏洞信息中的name、summary、description、solution等字段信息。"""


def new_main():
    name_list = get_name_list()
    # print name_list
    # print len(name_list)
    for name in name_list:
        print "name: " + name
        result_file = os.path.join(output_dir, "%s_result.xls" % name)
        if os.path.exists(result_file):
            continue
        vid_list = get_vuln_id_range(name)
        vuln_info_collect(name, vid_list)
        translate_and_save(name)
        merge_temp_result(name)
        # break


def main():
    print "translate vulnerability infos with google-translate..."
    time.sleep(2)
    # print "install necessary python package...?"
    # print "run:  pip install googletrans xlrd xlwt xlutils "
    name = raw_input('please input your chinese name: ').strip()
    vid_list = []
    # print get_vuln_infos(100000, 100009, name)
    # sys.exit(-1)
    while not vid_list:
        vid_list = get_vuln_id_range(name)
        if not vid_list:
            name = raw_input('please input your chinese name: ')

    temp_file_name = os.path.join(output_dir, "%s_job.xls" % name)
    tag = 1
    while tag:
        print """select process:
                1:  normal process (recommended)
                2： only collect the job source file
                3:  job source created, now start translate
                4:  translate process broken, and continue translate
                5:  temp file created, and only merge them
                0:  exit process
            """
        ans = raw_input("your choice is: ")
        if int(ans) == 1:
            vuln_info_collect(name, vid_list)
            translate_and_save(name)
            merge_temp_result(name)
            tag = 0
        elif int(ans) == 2:
            vuln_info_collect(name, vid_list)
            tag = 1
        elif int(ans) == 3:
            if not os.path.exists(temp_file_name):
                print "cannot find job source file, pls select '1'"
                tag = 1
            else:
                translate_and_save(name)
                merge_temp_result(name)
                tag = 0
        elif int(ans) == 4:
            print "check the ./temp/ dir, and input the lastest file id number"
            temp_id = raw_input("lastest file id number: ")
            start_id = int(temp_id)/100 + 1
            if start_id < 1 or start_id > 12:
                print "wrong id number..."
                tag = 1
            else:
                translate_and_save(name, start_id)
                merge_temp_result(name)
                tag = 0
        elif int(ans) == 5:
            merge_temp_result(name)
            tag = 0
        elif int(ans) == 0:
            tag = 0
        else:
            print "select wrong, pls re-select."


if __name__ == "__main__":
    main()
    # new_main()

    
    

    



