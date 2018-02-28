from django.conf.urls import url

from restful.business.views import get_all_clusters, get_dfs_capacity, get_top_user, get_hive_top, get_impala_top, \
    get_hdfs_used, get_cluster_used, get_top_user_adding, get_top_contents_adding, get_yarn_vcore_site, \
    get_yarn_memory_site, get_hive_summer, get_hive_table, get_hive_database

urlpatterns = [
    url(r'^clusters$', get_all_clusters, name='clusters'),
    url(r'^clusters/capacity', get_dfs_capacity, name='capacity'),
    url(r'^clusters/hdfs/top', get_top_user, name='top-user'),
    url(r'^clusters/hive/top', get_hive_top, name='top-hive-user'),
    url(r'^clusters/impala/top', get_impala_top, name='top-impala-user'),
    url(r'^clusters/charts/hdfs/(?P<frequent>[0-9a-zA-Z_-]+)', get_hdfs_used, name='hdfs-userd'),
    url(r'^clusters/charts/cluster/(?P<type>[0-9a-zA-Z_-]+)', get_cluster_used, name='cluster-userd'),
    url(r'^clusters/hdfs/user/adding', get_top_user_adding, name='top-adding-user'),
    url(r'^clusters/hive/summer/adding', get_hive_summer, name='summer-adding-hive'),
    url(r'^clusters/hive/database/adding', get_hive_database, name='database-adding-hive'),
    url(r'^clusters/hive/table/adding', get_hive_table, name='table-adding-hive'),
    url(r'^clusters/hdfs/contents/adding', get_top_contents_adding, name='top-adding-contents'),
    url(r'^clusters/yarn/vcore', get_yarn_vcore_site, name='top-yarn-vcore'),
    url(r'^clusters/yarn/memory', get_yarn_memory_site, name='top-yarn-memory'),
]
