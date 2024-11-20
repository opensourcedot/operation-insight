import pandas as pd
import sys

def parse_openEuler_csv(source_file_path, target_file_path):
    try:
        # 读取数据，这里假设每行的四个数据字段由两个或多个空格分隔
        data = pd.read_csv(source_file_path)
        # 为列数据命名
        data.columns = ['Repo', 'Company', 'Count']
        
        company_count = data.groupby('Company')['Count'].sum().reset_index()
        sum_of_count = data['Count'].sum()
        company_count['Percentage'] = (company_count['Count'] / sum_of_count) * 100
        
        # 将数据写入Excel文件，不保留行索引
        company_count.to_excel(target_file_path, index=False)
        
        print("文件转换完成，已保存为：", target_file_path)
    except Exception as e:
        print("在转换文件时发生错误：", e)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python script_name.py source_file_path target_file_path")
        sys.exit(1)
    
    source_file_path = sys.argv[1]  # 命令行传入的源文件路径
    target_file_path = sys.argv[2]  # 命令行传入的目标文件路径

    # 调用函数进行处理
    parse_openEuler_csv(source_file_path, target_file_path)
