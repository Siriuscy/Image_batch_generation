import json
import pandas as pd


def excel_to_jsonl(excel_path, jsonl_path):
    # 读取Excel文件
    excel_file = pd.read_excel(excel_path)

    # 将数据框转换为JSON格式
    json_data = excel_file.to_json(orient='records')

    # 写入JSON数据到文件
    for i in json.loads(json_data):
        with open(jsonl_path, 'a', encoding='utf-8') as f:
            json.dump(i, f, ensure_ascii=False)
            f.write("\n")


if __name__ == '__main__':
    excel_path = "../../topic_splitting/topic_pool/topic_pool_update_1115.xlsx"
    jsonl_path = "../../topic_splitting/topic_pool/topic_pool_update_1115.jsonl"
    excel_to_jsonl(excel_path, jsonl_path)
