import pandas as pd
import sys

def parse_and_maintainer_data(source_file_path, dest_file_path):
    try:
        data = pd.read_csv(source_file_path)
        data.columns = ['GiteeID', 'Company', 'PR', 'Issue', 'Review']

        data['社区贡献总数'] = data['PR'] + data['Issue'] + data['Review']

        data.to_excel(dest_file_path, index=False)
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
    parse_and_maintainer_data(source_file_path, dest_file_path)