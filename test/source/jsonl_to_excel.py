import pandas as pd
import json


def jsonl_to_excel(jsonl_path, excel_path):
    # 读取JSONL文件
    data = []
    with open(jsonl_path, 'r', encoding="utf-8") as f:
        for line in f:
            data.append(pd.json_normalize(json.loads(line)))

        # 将数据合并为一个DataFrame
    df = pd.concat(data, ignore_index=True)

    # 将DataFrame写入Excel文件
    df.to_excel(excel_path, index=False)


if __name__ == '__main__':
    jsonl_path = "../../topic_splitting/topic_pool/topic_pool_update_1114.jsonl"
    excel_path = "../../topic_splitting/topic_pool/topic_pool_update_1114.xlsx"
    jsonl_to_excel(jsonl_path, excel_path)
