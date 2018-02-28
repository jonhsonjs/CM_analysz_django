# -*- coding:utf-8 -*-
import inspect
import logging
import sys
import textwrap

import pytz

from restful.util.chart_util import n_lines_charts
import pylab as pl
#
# Customize these constants for your Cloudera Manager.
#
from restful.common.api_client import ApiClient
from restful.common.timeseries import do_query_rollup, do_query
from restful.util.date_util import get_one_day_ago_from, get_n_hour_ago_from, zone_conversion, zone_conversion_date
from restful.util.unit_converter import check_digital_storage, check_digital_storage_without_unit

LOG = logging.getLogger(__name__)


class ClusterInfo(ApiClient):
    """
    
    """

    def get_all_clusters(self):
        return self._api.get_all_clusters()


def do_get_all_clusters():
    """
    """
    cluster_info = ClusterInfo()
    clusters = cluster_info.get_all_clusters()
    # for cluster in clusters:
    #     do_print(cluster)
    return massage_cluster_for_json(clusters)


def do_get_dfs_capacity():
    responses = do_query(
        "select dfs_capacity,dfs_capacity_used,dfs_capacity_used_non_hdfs where entityName=hdfs:nn-idc", None,
        None)
    return responses


def do_get_dfs_capacity_json():
    responses = do_get_dfs_capacity()

    massage_dfs = []
    for response in responses:
        if response.timeSeries:
            for ts in response.timeSeries:
                metadata = ts.metadata
                test = {}
                test['name'] = metadata.metricName
                if metadata.unitNumerators:
                    test['unit'] = metadata.unitNumerators[0]
                for data in ts.data:
                    test['value'] = data.value
                massage_dfs.append(test)
    return massage_dfs


def do_get_dfs_capacity_email():
    massage_dfs = do_get_dfs_capacity_json()
    massage_dfs_capacity = {}
    for value in massage_dfs:
        value['value'] = check_digital_storage_without_unit(value['value'], value['unit'], 'TB', 1)
        value['unit'] = 'TB'
        massage_dfs_capacity[value['name']] = value['value']

    massage_dfs_capacity['remaining'] = massage_dfs_capacity['dfs_capacity'] - massage_dfs_capacity[
        'dfs_capacity_used'] - massage_dfs_capacity['dfs_capacity_used_non_hdfs']
    massage_dfs_capacity['rate'] = "%.2f" % ((massage_dfs_capacity['dfs_capacity_used'] + massage_dfs_capacity[
        'dfs_capacity_used_non_hdfs']) / massage_dfs_capacity['dfs_capacity'] * 100)
    return massage_dfs_capacity


def do_get_dfs_mem(pic=''):
    responses = do_query_rollup(
        "select 100 * total_physical_memory_used_across_hosts/total_physical_memory_total_across_hosts "
        "WHERE category=CLUSTER",
        get_n_hour_ago_from(n=24), None, 'HOURLY')

    file_path = "./mem.png"
    code = ['-', ':', '--', '-.', '-.']
    test = []
    index = 0
    for response in responses:
        if response.timeSeries:
            for ts in response.timeSeries:
                print index
                x = []
                mean_values = []
                metadata = ts.metadata
                unit = metadata.unitNumerators[0].encode("utf-8")
                for data in ts.data:
                    x_time = pl.datetime.datetime.fromtimestamp(
                        zone_conversion_date(timestamp=data.timestamp).timestamp, pytz.timezone('Asia/Shanghai'))
                    x.append(x_time)
                    mean_values.append("%.2f" % data.value)
                    data_type = data.type
                legend = metadata.entityName
                label_mean = legend
                test.append((x, mean_values, label_mean, code[index], 1))
                index = index + 1

        if not pic:
            n_lines_charts(test, file_path, unit, data_type, 100, u'群集Mem使用率')
        return test, 'percent'


def do_get_dfs_cpu(pic=''):
    responses = do_query_rollup("select cpu_percent_across_hosts WHERE category = CLUSTER",
                                get_n_hour_ago_from(n=24), None, 'HOURLY')
    file_path = "./cpu.png"
    code = ['-', ':', '--', '-.', '-.']
    test = []
    index = 0
    y_max = 100
    for response in responses:
        if response.timeSeries:
            for ts in response.timeSeries:
                x = []
                max_values = []
                mean_values = []
                metadata = ts.metadata
                unit = metadata.unitNumerators[0].encode("utf-8")
                for data in ts.data:
                    x_time = pl.datetime.datetime.strptime(
                        zone_conversion(timestamp=data.timestamp, format=u'YYYY-MM-DD HH:mm:ss'), "%Y-%m-%d %H:%M:%S")
                    x.append(x_time)
                    if data.aggregateStatistics:
                        max_values.append("%.2f" % data.aggregateStatistics.max)
                    mean_values.append("%.2f" % data.value)
                    data_type = data.type
                legend = metadata.entityName

                if max_values:
                    label_max = legend + "Max"
                    test.append((x, max_values, label_max, code[index], 1))
                label_mean = legend + "Avg"
                test.append((x, mean_values, label_mean, code[index], 1))
                index = index + 1
        if not pic:
            n_lines_charts(test, file_path, unit, data_type, y_max, u'群集CPU使用率')
        return test, unit


def do_get_dfs_net(pic=''):
    responses = do_query_rollup("select total_bytes_transmit_rate_across_network_interfaces where category = CLUSTER",
                                get_n_hour_ago_from(n=24), None, 'HOURLY')

    file_path = "./net.png"
    code = ['-', ':', '--', '-.', '-.']
    test = []
    index = 0
    y_max = 0
    for response in responses:
        if response.timeSeries:
            for ts in response.timeSeries:
                x = []
                max_values = []
                mean_values = []
                metadata = ts.metadata
                unit = metadata.unitNumerators[0].encode("utf-8")
                for data in ts.data:
                    x_time = pl.datetime.datetime.strptime(
                        zone_conversion(timestamp=data.timestamp, format=u'YYYY-MM-DD HH:mm:ss'), "%Y-%m-%d %H:%M:%S")
                    x.append(x_time)
                    mean_values.append("%.2f" % data.value)
                    data_type = data.type
                legend = metadata.entityName
                label_mean = legend
                test.append((x, mean_values, label_mean, code[index], 1))
                index = index + 1
                if max_values:
                    y_max = max(y_max, max(max_values))
                y_max = max(y_max, max(mean_values))
        if not pic:
            n_lines_charts(test, file_path, unit, data_type, float(y_max), u'群集Net传输量')
        return test, unit


def do_print(cluster):
    print("<ApiCluster>")
    print("  name: %s" % cluster.name)
    print("  displayName: %s" % cluster.displayName)
    print("  version: %s" % cluster.version)
    print("  fullVersion: %s" % cluster.fullVersion)
    if cluster.entityStatus:
        print("  entityStatus: %s" % cluster.entityStatus)


def usage():
    doc = inspect.getmodule(usage).__doc__
    print >> sys.stderr, textwrap.dedent(doc % (sys.argv[0],))


def setup_logging(level):
    logging.basicConfig()
    logging.getLogger().setLevel(level)


def massage_cluster_for_json(clusters):
    massage_cluster = []
    for cluster in clusters:
        massage_cluster.append(
            {
                'name': cluster.name,
                'displayName': cluster.displayName,
                'version': cluster.version,
                'fullVersion': cluster.fullVersion,
                'entityStatus': cluster.entityStatus
            }
        )
    return massage_cluster


def main(argv):
    setup_logging(logging.INFO)
    # Do work
    # t = do_get_dfs_capacity_email()
    do_get_dfs_mem(pic='fake')
    # do_get_dfs_cpu()
    # do_get_dfs_net()


#
# The "main" entry
#
if __name__ == '__main__':
    sys.exit(main(sys.argv))
