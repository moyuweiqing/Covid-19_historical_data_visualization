import pandas as pd
import os
from pyecharts.charts import Timeline
from pyecharts.charts import Bar, Grid
from pyecharts import options as opts

key_Chinese = {'confirm': '累计确诊', 'confirm_add': '当日新增确诊', 'heal': '累计治愈', 'dead': '累计死亡'}

def main_entry(key_list):
    timeline = Timeline(init_opts=opts.InitOpts(
            width='1900px',
            height='900px',
        ))
    timeline.add_schema(is_auto_play=True, is_timeline_show=False, play_interval = 300)

    for row in range(0, 579):
        grid_chart = Grid()

        for key in key_list:
            df = pd.read_csv('../data/' + key + '.csv', encoding='gb18030')
            c = draw_subplot(df, key, row)
            # print('finished', key, row + 1)
            if key == 'confirm':
                grid_chart.add(c, grid_opts=opts.GridOpts(pos_left='4%', pos_top='7%', pos_right='51%', pos_bottom='52%'))
            if key == 'confirm_add':
                grid_chart.add(c, grid_opts=opts.GridOpts(pos_left='4%', pos_top='53%', pos_right='51%', pos_bottom='4%'))
            if key == 'heal':
                grid_chart.add(c, grid_opts=opts.GridOpts(pos_left='51%', pos_top='7%', pos_right='4%', pos_bottom='52%'))
            if key == 'dead':
                grid_chart.add(c, grid_opts=opts.GridOpts(pos_left='51%', pos_top='53%', pos_right='4%', pos_bottom='4%'))

        timeline.add(grid_chart, str(row))
    timeline.render('../result/timeline.html')

def draw_subplot(df, replace_key, row):

    top10 = pd.DataFrame(df.iloc[row])
    top10.drop(index=['year', 'date'], inplace=True)
    top10.columns = ['tmpcol']
    top10.sort_values(by='tmpcol', inplace=True, ascending=False)

    ydata = top10['tmpcol'].head(10).tolist()
    xdata = top10.head(10).index.tolist()

    title = key_Chinese[replace_key] + '人数'
    title_location_dic = {'累计确诊': "50%", '当日新增确诊': "60%",'累计治愈': "70%", '累计死亡': "80%"}
    title_location = title_location_dic[key_Chinese[replace_key]]

    c = (
        Bar(
            init_opts=opts.InitOpts(
                # width='1800px',
                # height='800px',
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="elasticOut"
                )
            )
        )
        .add_xaxis(xdata)
        .add_yaxis(series_name = title,
                   is_selected = True,
                   y_axis = ydata,
                   label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(title_opts=opts.TitleOpts(
                              title='年份：' + str(df['year'].iloc[row]), subtitle="日期：" + str(df['date'].iloc[row]),
                              pos_left="10%",
                              title_textstyle_opts=opts.TextStyleOpts(font_size = 25),
                              subtitle_textstyle_opts=opts.TextStyleOpts(font_size = 20)
                         ),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                         axispointer_opts=opts.AxisPointerOpts(
                             is_show=True,
                             link=[{"xAxisIndex": "all"}],
                             label=opts.LabelOpts(background_color="#777"),
                         ),
                         legend_opts=opts.LegendOpts(
                             is_show=True,
                             pos_top=10,
                             pos_left=title_location,
                             item_width=30,
                             item_height=15,
                             legend_icon = 'circle',
                             textstyle_opts=opts.TextStyleOpts(
                                 font_family='Microsoft Yahei',
                                 font_size=15,
                                 # font_style='oblique'
                             )
                         ),
                         tooltip_opts=opts.TooltipOpts(
                             trigger="axis",
                             axis_pointer_type="cross",
                             background_color="rgba(245, 245, 245, 0.8)",
                             border_width=1,
                             border_color="#ccc",
                             textstyle_opts=opts.TextStyleOpts(color="#000"),
                         ),
                         )
    )

    return c

if __name__ == '__main__':
    key_list = ['confirm_add', 'confirm', 'heal', 'dead']
    main_entry(key_list)