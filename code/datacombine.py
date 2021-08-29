import pandas as pd
import os

def read_csv_file(col):
    # 读取所有的csv文件
    filepath = os.listdir('../data/')

    # 关联控制
    judge = True

    for file in filepath:
        if os.path.splitext(file)[1] == '.csv':
            try:
                data = pd.read_csv('../data/' + file)
            except:
                continue
            data.set_index(['year', 'date'], inplace=True)

            # 修改列名
            col_name_new = [i + file.split('.')[0] for i in data.columns]
            data.columns = col_name_new

            # 提取特定列
            data_tmp = data[col + file.split('.')[0]]

            # 关联
            if judge:
                merge_df = data_tmp
                judge = False
            else:
                merge_df = pd.merge(merge_df, data_tmp, how='outer', left_index=True, right_index=True)

    merge_df.fillna(0, inplace=True)
    merge_df.reset_index(inplace=True)
    rename_col = [v.replace(col, '') for v in merge_df.columns]
    merge_df.columns = rename_col
    return merge_df

if __name__ == '__main__':
    key_list = ['confirm_add', 'confirm', 'heal', 'dead']
    for key in key_list:
        merge_file = read_csv_file(key)
        merge_file.to_csv('../data/' + key + '.csv', encoding='gb18030')