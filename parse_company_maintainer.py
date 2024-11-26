import sys
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid
from pyecharts.globals import ThemeType


def parse_company_maintainer(source_file_path, dest_file_path):
    try:
        try:
            data = pd.read_csv(source_file_path, encoding='utf-8')
        except UnicodeDecodeError:
            data = pd.read_excel(source_file_path) 
        data.columns = ['GiteeID', 'Company', 'PR', 'Issue', 'Review', '社区贡献总数']

        # 将'华为合作方'替换为'huawei'
        data['Company'] = data['Company'].replace('华为合作方', 'huawei')

        # 定义一个函数来分类社区贡献总数
        def classify_contribution(x):
            if x > 1000:
                return '> 1000'
            elif x > 350:
                return '350 < 1000'
            elif x > 50:
                return '50 < 350'
            elif x > 12:
                return '12 < 50'
            else:
                return '< 12'
        
        # 对数据进行分类
        data['分类'] = data['社区贡献总数'].apply(classify_contribution)

        # 按'Company'聚合，并计算每个公司的各类别的数量
        grouped = data.groupby(['Company', '分类']).size().unstack(fill_value=0)

        # 创建Grid对象，用于布局
        grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))

        # 为每个公司创建一个堆积柱状图
        count = 0
        for company in grouped.index:
            company_data = grouped.loc[company]
            bar = Bar()
            bar.add_xaxis(company_data.index.tolist())
            for category in company_data.index:
                bar.add_yaxis(category, company_data[category].tolist(), stack='stack')
            bar.set_global_opts(
                title_opts=opts.TitleOpts(title=f"{company} 社区贡献总数按分类统计"),
                yaxis_opts=opts.AxisOpts(name="数量"),
                xaxis_opts=opts.AxisOpts(name="分类"),
                legend_opts=opts.LegendOpts(is_show=True)
            )
            # 将每个Bar添加到Grid中，并设置位置
            grid.add(bar, grid_opts=opts.GridOpts(pos_left=f"{count % 2 * 50}%", pos_top=f"{count // 2 * 50}%", pos_right="60%"))
            count += 1

        # 渲染图表到文件
        grid.render("community_contribution_stacked_bar_chart.html")
        
        print("文件处理完成，已保存为：", dest_file_path)
    except Exception as e:
        print("在处理文件时发生错误：", e)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python script_name.py source_file_path target_file_path")
        sys.exit(1)
    
    source_file_path = sys.argv[1]  # 命令行传入的源文件路径
    target_file_path = sys.argv[2]  # 命令行传入的目标文件路径

    # 调用函数进行处理
    parse_company_maintainer(source_file_path, target_file_path)

