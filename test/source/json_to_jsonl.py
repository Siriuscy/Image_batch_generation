import json


def json_to_jsonl(json_path, jsonl_path):
    # 读取 JSON 文件
    with open(json_path, 'r', encoding="utf8") as file:
        data = json.load(file)

    # 转换为 JSONL 格式
    with open(jsonl_path, 'w', encoding="utf8") as file:
        for item in data:
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')


if __name__ == '__main__':
    json_path = "../data/test.json"
    jsonl_path = "../data/test.jsonl"
    json_to_jsonl(json_path, jsonl_path)
