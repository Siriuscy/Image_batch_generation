import pandas as pd
import json


def jsonl_to_json(jsonl_path, json_path):
    with open(jsonl_path, "r", encoding='utf-8') as f:
        json_file = []
        for line in f:
            json_file.append(json.loads(line))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_file, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    jsonl_path = "../../topic_splitting/topic_pool/topic_pool_update_1115.jsonl"
    json_path = "../../topic_splitting/topic_pool/topic_pool_update_1115.json"
    jsonl_to_json(jsonl_path, json_path)
