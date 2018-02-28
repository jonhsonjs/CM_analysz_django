# -*- coding:utf-8 -*-
import os

import sys

from django.conf import settings
from templated_email import send_templated_mail
from mako.template import Template
from templated_email import InlineImage

from restful.business.cluster_site import do_get_dfs_capacity_email, do_get_dfs_mem, do_get_dfs_cpu, do_get_dfs_net
from restful.business.hdfs_site import do_get_hdfs_used_weekly, do_get_hdfs_used_monthly, do_get_hdfs_used_quarterly
from restful.business.hive_site import do_get_hive_top_email, do_get_hive_top_email_bac,get_hive_job_summary
from restful.business.impala_site import do_get_impala_top_email, do_get_impala_top_email_bac,get_impala_job_summary
from restful.business.small_file_site import query_small_files, query_file_incr_info
from restful.util.date_util import zone_conversion, get_now


def overall_report():
    os.chdir(os.path.dirname(sys.argv[0]))
    data = do_get_dfs_capacity_email()
    rows, remaining, metadata = do_get_hdfs_used_weekly()
    rows1, metadata = do_get_hdfs_used_monthly()
    rows2, metadata = do_get_hdfs_used_quarterly()
    rows3 = do_get_hive_top_email()
    rows4 = do_get_impala_top_email()
    rows5 = query_small_files()
    get_impala_job_summary()
    get_hive_job_summary()
    query_file_incr_info()
    do_get_dfs_cpu()
    do_get_dfs_mem()
    do_get_dfs_net()

    with open('./cpu.png', 'rb') as lena1:
        image1 = lena1.read()

    with open('./mem.png', 'rb') as lena2:
        image2 = lena2.read()

    with open('./net.png', 'rb') as lena3:
        image3 = lena3.read()

    with open('./hdfs_weekly.png', 'rb') as lena4:
        image4 = lena4.read()

    with open('./hdfs_monthly.png', 'rb') as lena5:
        image5 = lena5.read()

    with open('./hdfs_quarterly.png', 'rb') as lena6:
        image6 = lena6.read()

    with open('./file.png', 'rb') as lena7:
        image7 = lena7.read()

    with open('./file2.png', 'rb') as lena8:
        image8 = lena8.read()

    with open('./impala_pie.png', 'rb') as lena9:
        image9 = lena9.read()

    with open('./hive_pie.png', 'rb') as lena10:
        image10 = lena10.read()

    inline_image1 = InlineImage(filename="cpu.png", content=image1)
    inline_image2 = InlineImage(filename="mem.png", content=image2)
    inline_image3 = InlineImage(filename="net.png", content=image3)
    inline_image4 = InlineImage(filename="hdfs_weekly.png", content=image4)
    inline_image5 = InlineImage(filename="hdfs_monthly.png", content=image5)
    inline_image6 = InlineImage(filename="hdfs_quarterly.png", content=image6)
    inline_image7 = InlineImage(filename="file.png", content=image7)
    inline_image8 = InlineImage(filename="file2.png", content=image8)
    inline_image9 = InlineImage(filename="impala_pie.png", content=image9)
    inline_image10 = InlineImage(filename="hive_pie.png", content=image10)

    send_templated_mail(
        template_name='report_template2',
        from_email='hadoopreport@163.com',
        recipient_list=['wanghuan70@wanda.cn','594410045@qq.com'],
        context={
            'time': zone_conversion(get_now()),
            'data': data,
            'rows': rows,
            'rows1': rows1,
            'rows2': rows2,
            'rows3': rows3,
            'rows4': rows4,
            'rows5': rows5,
            'remaining': remaining,
            'cpu_image': inline_image1,
            'mem_image': inline_image2,
            'net_image': inline_image3,
            'hdfs_weekly_image': inline_image4,
            'hdfs_monthly_image': inline_image5,
            'hdfs_quarterly_image': inline_image6,
            'file_image': inline_image7,
            'file2_image': inline_image8,
            'impala_pie_image': inline_image9,
            'hive_pie_image': inline_image10

        },
        # Optional:
        # cc=['cc@example.com'],
        # bcc=['bcc@example.com'],
        # headers={'My-Custom-Header':'Custom Value'},
        # template_prefix="my_emails/",
        # template_suffix="email",
    )
    print 'email send'


def sendmailto_sql_users():
    # Do work
    top_impalas = do_get_impala_top_email_bac()
    top_hives = do_get_hive_top_email_bac()
    user_impala_map = {}
    user_hive_map = {}
    aggregation_map = {}
    users = []
    impattr = ['time','user','database','duration','executing','stats_missing','entityName','pool','thread_cpu_time','statement']
    hiveattr = ['time','user','name','duration','entityName','pool','cpu_milliseconds']
    # step-1: 根据执行用户聚合
    for top_impala in top_impalas:
        key = top_impala['user']
        if key not in users:
            users.append(key)
        value = top_impala
        for vv in impattr:
            if not value.has_key(vv):
                value[vv] = 'N/A'
            if vv == 'statement' and not (value[vv].startswith('refresh')) \
                    and not (value[vv].startswith('INVALIDATE')) and not (value[vv].startswith('GET')):
                if key not in user_impala_map:
                    user_impala_map[key] = [value]
                else:
                    user_impala_map[key].append(value)
    for top_hive in top_hives:
        for vv in hiveattr:
            if not top_hive.has_key(vv):
                top_hive[vv] = 'N/A'
        key = top_hive['user']
        if key not in users:
            users.append(key)
        if key not in user_hive_map:
            value = [top_hive]
            user_hive_map[key] = value
        else:
            user_hive_map[key].append(top_hive)

    from metricBA_apps.models import UserGroup
    from metricBA_apps.models import StaffInfo
    queryset = UserGroup.objects.filter(name='admin')
    admins = StaffInfo.objects.all().filter(group=queryset)
    # step-2: 执行用户和员工进行映射
    for user in users:
        queryset = UserGroup.objects.filter(name=user)
        staffs = StaffInfo.objects.all().filter(group=queryset)
        if not staffs:
            value = {
                'impala': [],
                'hive': [],
                'staff': user,
                'email': [str(user)+'@wanda.cn']
            }
            if user in user_impala_map:
                value['impala'] = user_impala_map[user]
            if user in user_hive_map:
                value['hive'] = user_hive_map[user]
            aggregation_map[user] = value
        else:
            for staff in staffs:
                if user not in aggregation_map:
                    value = {
                                    'impala':[],
                                    'hive':[],
                                    'staff': staff.code,
                                    'email': [staff.email]
                                }
                    if user in user_impala_map:
                        value['impala'] = user_impala_map[user]
                    if user in user_hive_map:
                        value['hive'] = user_hive_map[user]
                    aggregation_map[user] = value
                else:
                    aggregation_map[user]['email'].append(staff.email)
    for i in aggregation_map:
        if len(aggregation_map[i]['impala'])>0 or len(aggregation_map[i]['hive'])>0:
            send_templated_mail(
                template_name='report_template4',
                from_email='hadoopreport@163.com',
                recipient_list=aggregation_map[i]['email'],
                context={
                    'username': aggregation_map[i]['email'],
                    'rows4': aggregation_map[i]['impala'],
                    'rows3': aggregation_map[i]['hive'],
                },
                # Optional:
                cc=['594410045@qq.com','wanghuan70@wanda.cn','ourui@wanda.cn','yuanbowen1@wanda.cn'],
                # bcc=['bcc@example.com'],
                # headers={'My-Custom-Header':'Custom Value'},
                # template_prefix="my_emails/",
                # template_suffix="email",
            )


def test1():
    mytemplate = Template(filename='./test.mako')
    print(mytemplate.render())


if __name__ == '__main__':
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metricBA.settings")
    django.setup()
    overall_report()
    # sendmailto_sql_users()