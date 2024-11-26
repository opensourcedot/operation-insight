import pandas as pd
import sys

def maintainer_grouped_by_company(source_file_path, dest_file_path):
    try:
        data = pd.read_excel(source_file_path)
        data.columns = ['GiteeID', 'Company', 'PR', 'Issue', 'Review', '社区贡献总数']

        # 将'华为合作方'替换为'huawei'
        data['Company'] = data['Company'].replace('华为合作方', 'huawei')
        data['Company'] = data['Company'].replace('华为技术有限公司', 'huawei')

        # 统计每个Company中giteeid的个数
        company_counts = data.groupby('Company')['GiteeID'].nunique().reset_index()

        # 重命名列
        company_counts.columns = ['Company', 'MaintainerCount']

        company_counts.to_excel(dest_file_path, index=False)
        print("文件转换完成，已保存为：", dest_file_path)
    except Exception as e:
        print("在转换文件时发生错误：", e)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python script_name.py source_file_path target_file_path")
        sys.exit(1)
    
    source_file_path = sys.argv[1]  # 命令行传入的源文件路径
    dest_file_path = sys.argv[2]

    # 调用函数进行处理
    maintainer_grouped_by_company(source_file_path, dest_file_path)