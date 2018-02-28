# -*- coding:utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render

from restful.business.cluster_site import do_get_all_clusters, do_get_dfs_capacity, do_get_dfs_capacity_json, \
    do_get_dfs_cpu, do_get_dfs_mem, do_get_dfs_net
from restful.business.hdfs_site import do_get_top_user, do_get_hdfs_used_weekly, do_get_hdfs_used_monthly, \
    do_get_hdfs_used_quarterly, do_get_top_user_adding
from restful.business.small_file_site import do_query_hdfs_contents_adding
from restful.business.hive_site import do_get_hive_top, do_get_top_user_demo
from restful.business.impala_site import do_get_impala_top
from restful.util.json_util import MetricJsonEncoder
from restful.util.unit_converter import unit_converter, check_digital_storage
from restful.business.yarn_resource_site import do_get_vocre_site, do_get_memory_site
from restful.business.hive_table_add import generate_summer_hive_info, generate_table_info, generate_db_info


def get_all_clusters(request):
    clusters = do_get_all_clusters()
    resp = JsonResponse({
        'status': 0,
        'data': clusters,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def overview(request):
    string = u"welcome to my house by reborn"
    return render(request, 'index.html', {'reborn': string})


def storage(request):
    string = u"welcome to my house by reborn"
    return render(request, 'storage/index.html', {'reborn': string})


def top(request):
    string = u"welcome to my house by reborn"
    return render(request, 'top/index.html', {'reborn': string})


def users(request):
    string = u"welcome to my house by reborn"
    return render(request, 'users/index.html', {'reborn': string})


def cpu(request):
    string = u"welcome to my house by reborn"
    return render(request, 'iframes/cpu.html', {'reborn': string})


def memory(request):
    string = u"welcome to my house by reborn"
    return render(request, 'iframes/memory.html', {'reborn': string})


def network(request):
    string = u"welcome to my house by reborn"
    return render(request, 'iframes/network.html', {'reborn': string})


def ranking(request):
    string = u"welcome to my house by reborn"
    return render(request, 'iframes/ranking.html', {'reborn': string})


def get_dfs_capacity(request):
    dfs_capacity = do_get_dfs_capacity_json()
    resp = JsonResponse({
        'status': 0,
        'data': converter(dfs_capacity),
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_top_user(request):
    top_users = do_get_top_user()
    resp = JsonResponse({
        'status': 0,
        'data': top_users,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_top_user_adding(request):
    user_adding = do_get_top_user_adding()
    resp = JsonResponse({
        'status': 0,
        'data': user_adding,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_top_contents_adding(request):
    contents_adding = do_query_hdfs_contents_adding()
    resp = JsonResponse({
        'status': 0,
        'data': contents_adding,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_yarn_vcore_site(request):
    vcore_site = do_get_vocre_site()
    resp = JsonResponse({
        'status': 0,
        'data': vcore_site,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_yarn_memory_site(request):
    memory_site = do_get_memory_site()
    resp = JsonResponse({
        'status': 0,
        'data': memory_site,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_hive_summer(request):
    hive_summer = generate_summer_hive_info()
    resp = JsonResponse({
        'status': 0,
        'data': hive_summer,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_hive_database(request):
    hive_summer = generate_db_info()
    resp = JsonResponse({
        'status': 0,
        'data': hive_summer,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_hive_table(request):
    hive_table = generate_table_info()
    resp = JsonResponse({
        'status': 0,
        'data': hive_table,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_hive_top(request):
    top_hive = do_get_top_user_demo()
    resp = JsonResponse({
        'status': 0,
        'data': top_hive,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_impala_top(request):
    top_impala = do_get_impala_top()
    resp = JsonResponse({
        'status': 0,
        'data': top_impala,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_hdfs_used(request, frequent):
    line = {}
    if frequent == 'weekly':
        hdfs_used, remaining, metadata = do_get_hdfs_used_weekly(pic='fake')
        line['remaining'] = remaining
    if frequent == 'monthly':
        hdfs_used, metadata = do_get_hdfs_used_monthly(pic='fake')
    if frequent == 'quarterly':
        hdfs_used, metadata = do_get_hdfs_used_quarterly(pic='fake')
    line['hdfs_used'] = hdfs_used
    line['metadata'] = metadata
    resp = JsonResponse({
        'status': 0,
        'data': line,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def get_cluster_used(request, type):
    line = {}
    if type == 'cpu':
        cluster_used, unit = do_get_dfs_cpu(pic='fake')
    if type == 'mem':
        cluster_used, unit = do_get_dfs_mem(pic='fake')
    if type == 'net':
        cluster_used, unit = do_get_dfs_net(pic='fake')
    line['cluster_used'] = cluster_used
    line['unit'] = unit
    resp = JsonResponse({
        'status': 0,
        'data': line,
    }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
    return resp


def converter(values):
    for value in values:
        unit_to = unit_converter(value['value'], value['unit'])
        value_to = check_digital_storage(value['value'], value['unit'], unit_to, 1)
        value['value'] = value_to
        value['unit'] = unit_to
    return values
