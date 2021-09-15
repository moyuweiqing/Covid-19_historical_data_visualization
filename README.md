# Covid-19_historical_data_visualization
新冠疫情数据爬取及数据动态可视化

**数据爬取**  
从 <https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=> 爬取各国的疫情历史数据，包含当日新增、累计确诊、治愈、死亡人数，分类将各国的历史每天数据进行合并输出  

**数据可视化**
使用pyecharts，采用timeline + bar + grid的形式展现世界各国以来疫情情况的变化  
