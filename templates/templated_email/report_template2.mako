{% block subject %}计量报告_{{ time }}{% endblock %}
{% block html %}
<head>
    <title></title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        table, table td, table th {
            border-collapse: collapse;
        }

        table td {
            min-width: 100px !important;
            height: 75px;
            text-align: center;
            vertical-align: center;
            max-width: 1000px !important;
        }

        table caption {
            font-size: 18px;
            font-weight: 700;
        }

        img {
            max-width: 1000px;
        }
    </style>
</head>

<body style="margin: 0; padding: 0;">
<table border="1" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td>
            <table bgcolor=#F9F9F9 border=1 cellpadding="0" cellspacing="0" align="center" width="600"
                   style="border-collapse: collapse;">
                <caption style="text-align:left;"><h1>成都综合生产集群报告</h1></caption>
                <tr>
                    <td style="text-align: left;">
                        <p style="font-size: 18px; font-weight: 700;">文件系统概况：</p>
                        <p style="margin-left:40px;">总容量：{{data.dfs_capacity}}T(已用HDFS容量：{{data.dfs_capacity_used}}T,
                            已用非HDFS容量：{{data.dfs_capacity_used_non_hdfs}}T, 剩余容量：{{data.remaining}}T,
                            使用率：{{data.rate}}%</p>
                        <p style="margin-left:40px;">NameNode:2个</p>
                        <p style="margin-left:40px;">Datanode：30个</p>
                    </td>
                </tr>
                <tr>
                    <td style="text-align: center; padding: 40px 30px 40px 30px;">
                        <br/>
                        <table bgcolor=#F9F9F9 border=1 cellspacing=0
                               style="table-layout:fixed;word-break:break-all;background:#f2f2f2">
                            <caption>周增长情况</caption>
                            <thead>
                            <tr>
                                <th>日期</th>
                                <th>已用容量(T)</th>
                                <th>上周容量(T)</th>
                                <th>增量(T)</th>
                                <th>周增长率(%)</th>
                                <th>趋势图</th>
                            </tr>
                            </thead>
                            <tbody>
                            {% for row in rows %}
                            <tr>
                                <td>{{row.col_1}}</td>
                                <td>{{row.col_2}}</td>
                                <td>{{row.col_3}}</td>
                                <td>{{row.col_4}}</td>
                                <td>{% widthratio row.col_4 row.col_3 100%}</td>
                                {% if 1 == forloop.counter %}
                                <td rowspan=4><img style="width: 400px;height:300px;" src={{ hdfs_weekly_image }}></td>
                                {% endif %}
                            </tr>
                            {% endfor %}
                            </tbody>
                            <tfoot>
                            <tr>
                                <td colspan="6">
                                    说明：按最近增长速度，预计还有
                                    <font color=red>{{remaining}}</font>天到达70%的警戒线<br/>
                                </td>
                            </tr>
                            </tfoot>
                        </table>
                        <br/>

                        <br/>
                        <table bgcolor=#F9F9F9 border=1 cellspacing=0
                               style="table-layout:fixed;word-break:break-all;background:#f2f2f2">
                            <caption>月增长情况</caption>
                            <thead>
                            <tr>
                                <th>日期</th>
                                <th>已用容量(T)</th>
                                <th>上月容量(T)</th>
                                <th>增量(T)</th>
                                <th>月增长率(%)</th>
                                <th>趋势图</th>
                            </tr>
                            </thead>
                            <tbody>
                            {% for row in rows1 %}
                            <tr>
                                <td>{{row.col_1}}</td>
                                <td>{{row.col_2}}</td>
                                <td>{{row.col_3}}</td>
                                <td>{{row.col_4}}</td>
                                <td>{% widthratio row.col_4 row.col_3 100%}</td>
                                {% if 1 == forloop.counter %}
                                <td rowspan=4><img style="width: 400px;height:300px;" src={{ hdfs_monthly_image }}></td>
                                {% endif %}
                            </tr>
                            {% endfor %}
                            </tbody>
                        </table>
                        <br/>
                        <br/>
                        <table bgcolor=#F9F9F9 border=1 cellspacing=0
                               style="table-layout:fixed;word-break:break-all;background:#f2f2f2">
                            <caption>季度增长情况</caption>
                            <thead>
                            <tr>
                                <th>日期</th>
                                <th>已用容量(T)</th>
                                <th>上季度容量(T)</th>
                                <th>增量(T)</th>
                                <th>季度增长率(%)</th>
                                <th>趋势图</th>
                            </tr>
                            </thead>
                            <tbody>
                            {% for row in rows2 %}
                            <tr>
                                <td>{{row.col_1}}</td>
                                <td>{{row.col_2}}</td>
                                <td>{{row.col_3}}</td>
                                <td>{{row.col_4}}</td>
                                <td>{% widthratio row.col_4 row.col_3 100%}</td>
                                {% if 1 == forloop.counter %}
                                <td rowspan=4><img style="width: 400px;height:300px;" src={{ hdfs_quarterly_image }}></td>
                                {% endif %}
                            </tr>
                            {% endfor %}
                            </tbody>
                        </table>
                        <br/>
                    </td>
                </tr>

                <tr>
                    <td>
                        <br>
                        <p style="font-size:18px;font-weight: 700;">每日文件数量</p>
                        <p>
                            <img src={{ file_image }}>
                        </p>
                        <br>
                        <p style="font-size:18px;font-weight: 700;">每日文件大小</p>
                        <p>
                            <img src={{ file2_image }}>
                        </p>
                    </td>
                </tr>

                <tr>
                    <td>
                        <br>
                        <p style="font-size:18px;font-weight: 700;">群集CPU(24h)使用情况</p>
                        <p>
                            <img src={{ cpu_image }}>
                        </p>
                        <br>
                        <p style="font-size:18px;font-weight: 700;">集群内存(24h)使用情况</p>
                        <p>
                            <img src={{ mem_image }}>
                        </p>
                        <br>
                        <p style="font-size:18px;font-weight: 700;">集群网络(24h)使用情况</p>
                        <p>
                            <img src={{ net_image }}>
                        </p>
                    </td>
                </tr>
                <tr>
                    <td style="max-width: 600px;overflow: scroll;">
                        <br>
                        <table bgcolor=#F9F9F9 border=1 cellspacing=0 style="table-layout: fixed">
                            <caption>Top20小文件数</caption>
                            <tr>
                                <th>db_name</th>
                                <th>tbl_name</th>
                                <th>tbl_owner</th>
                                <th>support_person</th>
                                <th>table_location</th>
                                <th>storage_format</th>
                                <th>file_size_type</th>
                                <th>small_files_count</th>
                            </tr>
                            {% if rows5 %}
                            {% for row in rows5 %}
                            <tr>
                                <td>{{row.0}}</td>
                                <td>{{row.1}}</td>
                                <td>{{row.2}}</td>
                                <td>{{row.3}}</td>
                                <td>{{row.4}}</td>
                                <td>{{row.5}}</td>
                                <td>{{row.6}}</td>
                                <td>{{row.7}}</td>
                            </tr>
                            {% endfor %}
                            {% else %}
                            <tr>
                                <td colspan="8" style="width: 600px">没有超时任务，运行正常</td>
                            </tr>
                            {% endif %}
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <br>
                        <p style="font-size:18px;font-weight: 700;">IMPALA-任务时长统计</p>
                        <p>
                            <img src={{ impala_pie_image }}>
                        </p>
                        <br>
                    </td>
                </tr>
                <tr>
                    <td style="max-width: 600px;overflow: scroll;">
                        <br>
                        <table bgcolor=#F9F9F9 border=1 cellspacing=0 style="table-layout: fixed">
                            <caption>impala-运行超过5分钟的任务</caption>
                            <tr>
                                <th>time</th>
                                <th>user</th>
                                <th>database</th>
                                <th>duration</th>
                                <th>executing</th>
                                <th>stats_missing</th>
                                <th>pool</th>
                                <th>statement</th>
                            </tr>
                            {% if rows4 %}
                            {% for row in rows4 %}
                            <tr>
                                <td>{{row.time}}</td>
                                <td>{{row.user}}</td>
                                <td>{{row.database}}</td>
                                <td>{{row.query_duration}}</td>
                                <td>{{row.executing}}</td>
                                <td>{{row.stats_missing}}</td>
                                <td>{{row.pool}}</td>
                                <td>{{row.statement}}</td>
                            </tr>
                            {% endfor %}
                            {% else %}
                            <tr>
                                <td colspan="8" style="width: 600px">没有超时任务，运行正常</td>
                            </tr>
                            {% endif %}
                        </table>
                    </td>
                </tr>
                   <tr>
                    <td>
                        <br>
                        <p style="font-size:18px;font-weight: 700;">HIVE任务时长统计</p>
                        <p>
                            <img src={{ hive_pie_image }}>
                        </p>
                        <br>
                    </td>
                </tr>
                <tr>
                    <td style="width: 600px;overflow: scroll;">
                        <br>
                        <table style="width: 600px;" bgcolor=#F9F9F9 border=1 cellspacing=0>
                            <caption>HIVE-运行超过15分钟的任务</caption>

                            <tr>
                                <th>time</th>
                                <th>user</th>
                                <th>name</th>
                                <th>duration</th>
                                <th>entityName</th>
                                <th>pool</th>
                            </tr>
                            {% if rows3 %}
                            {% for row in rows3 %}
                            <tr>
                                <td>{{row.time}}</td>
                                <td>{{row.user}}</td>
                                <td>{{row.name}}</td>
                                <td>{{row.application_duration}}</td>
                                <td>{{row.entityName}}</td>
                                <td>{{row.pool}}</td>
                            </tr>
                            {% endfor %}
                            {% else %}
                            <tr>
                                <td colspan="6" style="width: 600px">没有超时任务，运行正常</td>
                            </tr>
                            {% endif %}
                        </table>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
</body>
{% endblock %}
