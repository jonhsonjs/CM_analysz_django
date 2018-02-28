{% block subject %}My subject for {{ username }}{% endblock %}
{% block html %}
<head>
    <title></title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        table, table td, table th {
            border-collapse: collapse;
        }
    </style>
</head>

<body style="margin: 0; padding: 0">
<table border="0" cellpadding="0" cellspacing="0" width="100%">

<h1>成都综合生产集群报告</h1>
文件系统概况：<br/>
总容量：1088.3T(已用HDFS容量：421.5T，已用非HDFS容量：54.5T，剩余容量：612.3T，使用率：43.7%)
<br/>
NameNode:2个,Datanode：30个<br/>
<br/>
<br/>周增长情况<br>
<table bgcolor=#F9F9F9 border=1 cellspacing=0 style="table-layout:fixed;word-break:break-all;background:#f2f2f2">
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
        <td rowspan=4><img src={{ test_image1 }}></td>
        {% endif %}
    </tr>
    {% endfor %}
    </tbody>

</table>

说明：按最近增长速度，预计还有
<font color=red>264.6</font>天到达70%的警戒线<br/><br>月增长情况<br>
<table bgcolor=#F9F9F9 border=1 cellspacing=0>
    <tr>
        <th>日期</th>
        <th>已用容量(T)</th>
        <th>上月容量(T)</th>
        <th>增量(T)</th>
        <th>月增长率(%)</th>
        <th>趋势图</th>
    </tr>
    {% for row in rows1 %}
    <tr>
        <td>{{row.col_1}}</td>
        <td>{{row.col_2}}</td>
        <td>{{row.col_3}}</td>
        <td>{{row.col_4}}</td>
        <td>{% widthratio row.col_4 row.col_3 100%}</td>
        {% if 1 == forloop.counter %}
        <td rowspan={{ rows1|length }}><img src={{ test_image2 }}></td>
        {% endif %}
    </tr>
    {% endfor %}
</table>
<br>季度增长情况<br>
<table bgcolor=#F9F9F9 border=1 cellspacing=0>
    <tr>
        <th>日期</th>
        <th>已用容量(T)</th>
        <th>上季度容量(T)</th>
        <th>增量(T)</th>
        <th>季度增长率(%)</th>
        <th>趋势图</th>
    </tr>
    {% for row in rows2 %}
    <tr>
        <td>{{row.col_1}}</td>
        <td>{{row.col_2}}</td>
        <td>{{row.col_3}}</td>
        <td>{{row.col_4}}</td>
        <td>{% widthratio row.col_4 row.col_3 100%}</td>
        {% if 1 == forloop.counter %}
        <td rowspan={{ rows2|length }}><img src={{ test_image3 }}></td>
        {% endif %}
    </tr>
    {% endfor %}
</table>
<br><br><br>
群集CPU(24h)使用情况
<p>
    <img src={{ cpu_image }}>
</p>
<br><br><br>集群内存(24h)使用情况<p>
    <img src={{ mem_image }}>
</p>
<br><br><br>集群网络(24h)使用情况<p>
    <img src={{ net_image }}>
</p>


<br>impala<br>
<table bgcolor=#F9F9F9 border=1 cellspacing=0>
    <tr>
        <th>time</th>
        <th>user</th>
        <th>database</th>
        <th>duration</th>
        <th>executing</th>
        <th>stats_missing</th>
        <th>entityName</th>
        <th>pool</th>
        <th>thread_cpu_time</th>
        <th>statement</th>
    </tr>
    {% for row in rows4 %}
    <tr>
        <td>{{row.time}}</td>
        <td>{{row.user}}</td>
        <td>{{row.database}}</td>
        <td>{{row.query_duration}}</td>
        <td>{{row.executing}}</td>
        <td>{{row.stats_missing}}</td>
        <td>{{row.entityName}}</td>
        <td>{{row.pool}}</td>
        <td>{{row.thread_cpu_time}}</td>
        <td>{{row.statement}}</td>
    </tr>
    {% endfor %}
</table>

<br>hive<br>
<table bgcolor=#F9F9F9 border=1 cellspacing=0>
    <tr>
        <th>time</th>
        <th>user</th>
        <th>name</th>
        <th>duration</th>
        <th>entityName</th>
        <th>pool</th>
        <th>cpu_milliseconds</th>
    </tr>
    {% for row in rows3 %}
    <tr>
        <td>{{row.time}}</td>
        <td>{{row.user}}</td>
        <td>{{row.name}}</td>
        <td>{{row.application_duration}}</td>
        <td>{{row.entityName}}</td>
        <td>{{row.pool}}</td>
        <td>{{row.cpu_milliseconds}}</td>
    </tr>
    {% endfor %}
</table>


</body>
{% endblock %}
