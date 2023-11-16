分维度统计
语气词处理
处理bad case



## 生成数据的主类

~~~python
from create_data import CreateData

file_path = "output/output.json"
topic_file_path = "../topic_splitting/topic_pool/topic_pool_original_1113.json"
case_file_path = "../topic_splitting/case_pool/case_pool_original_1113.json"

# 制造数据
c = CreateData(pool_data_file_path=topic_file_path, case_data_file_path=case_file_path, file_storage_path=file_path,
               kind=4)
for count in range(1, 3):
    c.start_create_data(count)

~~~

##### 类属性说明

- pool_data_file_path：话题池json文件路径
- case_data_file_path：人工写的例子池文件路径
- file_storage_path：生成的数据文件存放路径
- kind：整型，表示可以选择不同类型的prompt，0为多轮，1为一类打断，2为二类打断，3为三类打断，4为单轮

##### 类方法说明

~~~python
load_original_data():
# 读取话题库，返回话题文件

random_get_three_data(topic_data):
# 从话题文件中随机选择三条不重复数据，返回列表

select_prompt(selected_data):
# 选择不同的prompt，制造不同的数据，返回prompt

calling_gpt():
# 根据不同的prompt调用gpt，并将需要保存的数据存入队列

gpt_result_processing(self):
# 从队列中拿出数据存入jsonl文件

start_create_data(count):
# 开始制造数据
~~~

