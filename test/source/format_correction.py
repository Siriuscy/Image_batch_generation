import json

with open('../data/topic/pool.json', 'r', encoding='utf-8') as f:  # 使用utf-8编码打开文件
    json_data = json.load(f)
# 将列表转换为JSON并保存到文件中


print(len(json_data))
with open('../data/topic/pool.json', 'w', encoding='utf-8') as f:  # 使用utf-8编码打开文件
    json.dump(json_data, f, ensure_ascii=False, indent=2)  # 确保不将非ASCII字符转为\xxxx形式
