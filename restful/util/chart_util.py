# -*- coding:utf-8 -*-
from sklearn import linear_model
import warnings
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pylab as pl
import matplotlib.dates as dt
import pygal
from restful.util.unit_converter import unit_converter, check_digital_storage_without_unit


warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")
# 解决Matplotlib中文问题
pl.mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
pl.mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-


def get_linear_model(x_params, y_params, predict_value):
    # Create linear regression object
    regression = linear_model.LinearRegression()
    regression.fit(x_params, y_params)
    predict_outcome = regression.predict(predict_value)
    predictions = {'intercept': regression.intercept_, 'coefficient': regression.coef_,
                   'predicted_value': predict_outcome}
    return predictions


def two_bar_charts(labels, capacity, color, file_path):
    x_pos = list(range(len(labels)))
    width = 0.4

    median = get_median(capacity[0] + capacity[1])
    unit_to = unit_converter(median, 'bytes')
    fig, ax = plt.subplots(figsize=(8, 6))
    for i, values in enumerate(capacity):
        values = values[-4::]
        test = [check_digital_storage_without_unit(x, 'bytes', unit_to, 0) for x in values]
        rects = plt.bar([p + width * i for p in x_pos], test, width,
                        alpha=0.5,
                        color=color[i])
        for ii, rect in enumerate(rects):
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2., 1.02 * height,
                     '%s' % int(test[ii]),
                     ha='center', va='bottom')

    ax.set_ylabel(u'容量(单位:%s)' % unit_to)
    ax.set_xticks([p + 0.5 * width for p in x_pos])
    ax.set_xticklabels(labels)

    test1 = capacity[0][-4::] + capacity[1][-4::]
    test2 = [check_digital_storage_without_unit(x, 'bytes', unit_to) for x in test1]

    plt.ylim([0, max(test2) * 1.3])

    plt.xlim(min(x_pos) - width, max(x_pos) + width * 2)

    plt.legend([u'已用容量', u'总容量'], loc='best', fontsize=7)
    plt.grid()
    plt.savefig(file_path)


def single_bar_charts(labels, capacity, file_path, title):
    time_list = pl.datestr2num(labels)
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.autofmt_xdate()
    plt.bar(time_list, capacity, ec='k', ls='-', alpha=0.5, color='r')
    ax.xaxis_date()
    plt.legend([title], loc='best', fontsize=7)
    plt.grid()
    plt.savefig(file_path)


def pie_charts(x, types, job_total, file_path):
    pie_chart2 = pygal.Pie()
    pie_chart2.title = "Total Count:" + str(job_total)
    for i in range(min(len(types), len(x))):
        if x[i] != 0:
            label = types[i] + ':' + str(x[i]) + ' ' + "%.1f" % (float(x[i]) / job_total * 100) + '%'
            pie_chart2.add(label, x[i])
    pie_chart2.render_to_png(file_path)


def n_lines_charts(labels, file_path, unit, type, y_max, y_title):
    plt.style.use('ggplot')
    plt.figure(figsize=(14, 4))

    for x1, x2, x3, x4, x5 in labels:
        pl.plot_date(x1, x2, label=x3, linestyle=x4, linewidth=x5)

    ax = pl.gca()
    xfmt = dt.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    pl.gcf().autofmt_xdate()
    # Y轴单位，例如50%，100%
    if 'SAMPLE' == type:
        # 如果是原始变量，直接根据单位设置Y轴单位后缀
        if 'percent' == unit:
            y_tick = y_max
            suffix = '%'  # 单位后缀
        elif 'bytes' == unit:
            if y_max > 1024 * 1024 * 1024 * 1024:
                y_tick = y_max / 1024 / 1024 / 1024 / 1024
                suffix = 'T'
            if y_max > 1024 * 1024 * 1024:
                y_tick = y_max / 1024 / 1024 / 1024
                suffix = 'G'
            elif y_max > 1024 * 1024:
                y_tick = y_max / 1024 / 1024
                suffix = 'M'
            elif y_max > 1024:
                y_tick = y_max / 1024
                suffix = 'K'  # 网络流量单位转换
            else:
                y_tick = y_max
                suffix = 'b'
    else:
        # 如果是计算变量，默认设置
        y_tick = y_max
        suffix = '%'

    y_ticks = [0, 0.5 * y_max, y_max]
    y_ticks_labels = ['0', "%.1f" % (0.5 * y_tick) + suffix, "%.1f" % y_tick + suffix]
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_ticks_labels)
    pl.legend(loc='best', fontsize=6)
    pl.grid(True)
    pl.ylabel(y_title)
    pl.savefig(file_path)
    pl.cla()


def get_median(data):
    data.sort()
    half = len(data) // 2
    return data[half] + data[~half]


if __name__ == '__main__':
    pie_chart = pygal.Pie()
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add('IE', 19.5)
    pie_chart.add('Firefox', 36.6)
    pie_chart.add('Chrome', 36.3)
    pie_chart.add('Safari', 4.5)
    pie_chart.add('Opera', 2.3)
    pie_chart.render_to_png("./pie2.png")
