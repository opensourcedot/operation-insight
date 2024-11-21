import pandas as pd
import sys

def parse_and_sum_contributions(source_file_path, dest_file_path):
    try:
    
        data = pd.read_csv(source_file_path, header=None)
        # 将数据转换为DataFrame
        df = pd.DataFrame(data)

        # 忽略第一列（时间戳）
        df = df.iloc[:, 1:]

        # 计算每家企业的贡献数据总和
        # 假设企业名称在第一行，贡献数据在第二行和第三行
        company_names = df.iloc[0, :]  # 第一行是企业名称
        
        # 将贡献数据转换为数值格式，忽略非数值数据
        contributions_data = df.iloc[1:3, :].apply(pd.to_numeric, errors='coerce')

        # 计算贡献数据的总和
        contributions_sum = contributions_data.sum(axis=0)
        # 将企业名称和对应的贡献数据总和组合成一个新的DataFrame
        result_df = pd.DataFrame({'Company': company_names, 'TotalContribution': contributions_sum})

        total_contribution = result_df['TotalContribution'][1:].sum(axis=0)
        result_df_new = result_df.assign(Percentage = result_df['TotalContribution']/total_contribution * 100)

        result_df_new.to_excel(dest_file_path, index=False)
        print(f"结果已成功保存到Excel文件：{dest_file_path}")

    except Exception as e:
        print("在解析文件时发生错误：", e)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python script_name.py source_file_path target_file_path")
        sys.exit(1)
    
    source_file_path = sys.argv[1]  # 命令行传入的源文件路径
    dest_file_path = sys.argv[2]

    # 调用函数进行处理
    parse_and_sum_contributions(source_file_path, dest_file_path)