import pandas as pd
import os
from uuid import uuid4

def process_file(file_path: str, filename: str):
    # 使用唯一标识符创建临时文件名，避免文件名冲突
    unique_id = uuid4().hex
    processed_file_path = f"/tmp/processed_{unique_id}_{filename}.csv"

    try:
        # 根据文件扩展名选择读取方式
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(file_path)
        elif filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format")

        # 获取所有列名
        columns = df.columns

        # 创建一个空的 'sizes' 列
        df['sizes'] = ''

        # 遍历所有列（从第二列开始）
        for column_name in columns[1:]:
            new_column_name = f'size_{column_name}'
            df[new_column_name] = ''
            # 处理每一列的数据，并生成新的列
            df.loc[df[column_name] > 0, new_column_name] = column_name + '*' + df[column_name].fillna(0).astype(int).astype(str) + ','
            # 将新增的列内容合并到 'sizes' 列中
            df['sizes'] += df[new_column_name]

        # 删除所有新增的列
        df.drop(columns=[f'size_{column_name}' for column_name in columns[1:]], inplace=True)

        # 保存处理后的文件
        df.to_csv(processed_file_path, index=False)

        return processed_file_path

    finally:
        os.remove(file_path)