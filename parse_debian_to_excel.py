import pandas as pd
import sys

def txt_to_excel(source_file_path, target_file_path):
    try:
        # 读取数据，这里假设每行的四个数据字段由两个或多个空格分隔
        data = pd.read_csv(source_file_path, sep=r'\s{2,}', header=None)
        # 为列数据命名
        data.columns = ['Order', '软件包维护数', '姓名', '最后贡献时间']
        
        # 对第二列求和
        sum_of_packages = data['软件包维护数'].sum()
        total_contributors = len(data)
        
        # 计算贡献百分比
        data['贡献百分比'] = (data['软件包维护数'] / sum_of_packages) * 100
        data['累计贡献百分比'] = data['贡献百分比'].cumsum()
        data['贡献者百分比'] = data['Order'] / total_contributors * 100
        
        # 将数据写入Excel文件，不保留行索引
        data.to_excel(target_file_path, index=False)
        
        print("文件转换完成，已保存为：", target_file_path)
    except Exception as e:
        print("在转换文件时发生错误：", e)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python script_name.py source_file_path target_file_path")
        sys.exit(1)
    
    source_file_path = sys.argv[1]  # 命令行传入的源文件路径
    target_file_path = sys.argv[2]  # 命令行传入的目标文件路径

    # 调用函数进行转换
    txt_to_excel(source_file_path, target_file_path)