# -*- coding:utf-8 -*-
import sys
import datetime
from impala.dbapi import connect
from restful.util.chart_util import single_bar_charts


today = datetime.date.today()
today_string = today.strftime('%Y-%m-%d')
yesterday = (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

COMMAND = "select to_date(t.day),t.num_of_files,t.total_size_gb from ( select trunc(modification_time,'DD') day,count(1) num_of_files, round(sum(filesize)/1024/1024/1024,2) total_size_gb from idc_infrastructure_db.hdfs_meta where trunc(modification_time,'DD') is not null group by trunc(modification_time,'DD') order by trunc(modification_time,'DD') desc limit 30 )t order by t.day ;"
COMMAND1 = "select db_name,tbl_name,tbl_owner,support_person,table_location,storage_format,file_size_type,small_files_count from idc_infrastructure_db.hdfs_small_files_result order by small_files_count desc limit 20;"
COMMAND_contents_today = "select joinedpath, size from idc_infrastructure_db.hdfs_meta_dir_all_daily where dt='" + today_string + "'and size>10"
COMMAND_contents_yesterday = "select joinedpath, size from idc_infrastructure_db.hdfs_meta_dir_all_daily where dt='" + yesterday + "'and size>10"


def main(argv):
    aa = query_small_files()
    print aa


def query_file_incr_info():
    title = u"每日文件总数"
    title2 = u"每日文件大小(G)"
    file_path = "./file.png"
    file_path2 = "./file2.png"
    time_list = []
    val_files_list = []
    val_size_list = []
    conn = connect(host='***', port=21050, user="***", password="***",
                   auth_mechanism="PLAIN")
    cur = conn.cursor()
    cur.execute(COMMAND)
    rows = cur.fetchall()
    for row in rows:
        time_list.append(row[0])
        val_files_list.append(float(row[1]))
        val_size_list.append(float(row[2]))

    single_bar_charts(time_list, val_files_list, file_path, title)
    single_bar_charts(time_list, val_size_list, file_path2, title2)


def query_small_files():
    conn = connect(host='***', port=21050, user="***", password="***",
                   auth_mechanism="PLAIN")
    cur = conn.cursor()
    cur.execute(COMMAND1)
    rows = cur.fetchall()
    return rows


def query_hdfs_contents(command):
    conn = connect(host='***', port=21050, user='***', password='***', auth_mechanism="PLAIN")
    cur = conn.cursor()
    cur.execute(command)
    rows = cur.fetchall()
    attrs = ['joinedpath', 'size']
    content_dict = dict((attr, []) for attr in attrs)
    content_info = {}
    for row in rows:
        content_dict['joinedpath'].append(row[0])
        content_dict['size'].append(row[1])
        content_info[row[0]] = row[1]
    return (content_dict, content_info)


def do_query_hdfs_contents_adding():
    attrs = ['joinedpath', 'add']
    contents_hdfs_today_rows = query_hdfs_contents(COMMAND_contents_today)
    contents_hdfs_yesterday_rows = query_hdfs_contents(COMMAND_contents_yesterday)

    dict_today = contents_hdfs_today_rows[1]
    dict_yesterday = contents_hdfs_yesterday_rows[1]
    user_today = contents_hdfs_today_rows[0][attrs[0]]
    user_yesterday = contents_hdfs_yesterday_rows[0][attrs[0]]
    add_info = []
    for i in range(len(user_today)):
        if user_today[i] in user_yesterday:
            adding_float = dict_today.get(user_today[i]) - dict_yesterday.get(user_today[i])
            adding = float('%.2f' % adding_float)
            add_info.append({
                'content': user_today[i],
                'sizeToday': dict_today.get(user_today[i]),
                'sizeYesterday': dict_yesterday.get(user_today[i]),
                'adding': adding
                }
            )
        else:
            adding = dict_today.get(user_today[i])
            add_info.append({
                'content': user_today[i],
                'sizeToday': dict_today.get(user_today[i]),
                'sizeYesterday': 0,
                'adding': adding
                }
            )
    if attrs[0] == 'joinedpath':
        path_temp = []
        for info in add_info:
            path = info['content']
            if len(path.split('/')[1:]) <= 2 or ".Trash" in path:
                path_temp.append(info)
        for i in range(len(path_temp)):
            add_info.remove(path_temp[i])
    add_info_sorted = sorted(add_info, key=lambda k: k['adding'], reverse=True)
    return add_info_sorted[0:100]

def main(argv):
    t = do_query_hdfs_contents_adding()
    print t
# The "main" entry
#
if __name__ == '__main__':
    sys.exit(main(sys.argv))
