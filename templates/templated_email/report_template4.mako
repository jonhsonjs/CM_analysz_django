{% block subject %}sql优化{% endblock %}
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
<br/>这是今天平台一些job的运行情况，一起看看有没有可以优化的地方。<br>
<body style="margin: 0; padding: 0">
<table border="0" cellpadding="0" cellspacing="0" width="100%">
    {% if rows4 %}
    <br>impala-超过5分钟的任务<br>
    <table bgcolor=#F9F9F9 border=1 cellspacing=0>
        <tr>
            <th>time</th>
            <th>user</th>
            <th>database</th>
            <th>duration</th>
            <th>executing</th>
            <th>stats_missing</th>
##             <th>entityName</th>
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
            {% if row.stats_missing == 'true' %}
            <td><font size="3" color="red">{{row.stats_missing}}</font></td>
            {% else %}
            <td>{{row.stats_missing}}</td>
            {% endif %}
##             <td>{{row.entityName}}</td>
            <td>{{row.pool}}</td>
            <td>{{row.thread_cpu_time}}</td>
            <td>{{row.statement}}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}

    {% if rows3 %}
    <br>Hive-运行时间超过15分钟的任务<br>
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
    {% endif %}
</body>
{% endblock %}
