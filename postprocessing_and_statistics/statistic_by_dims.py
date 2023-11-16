import json
from collections import Counter
from prettytable import PrettyTable


class StatisticByDims(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def open_file(self):
        with open(self.file_path, encoding='utf-8') as f:
            json_file = []
            for line in f:
                json_file.append(json.loads(line))
        return json_file

    @staticmethod
    def append_in_list(json_file, label_list):
        """
        将要统计的数据添加进列表
        :param json_file: 数据文件
        :param label_list: 要统计的维度（key）列表
        :return: 待创建counter的列表，要统计的维度（key）列表
        """
        # 处理异常
        flag = 1
        keys_list = []  # 可供选择的keys列表
        error_list = []  # 不在可供选择的keys列表元素
        for k in range(1):
            keys_list = list(json_file[k].keys())
        for key in label_list:
            if key not in keys_list:
                flag = 0
                error_list.append(key)
        if not flag:
            for row in error_list:
                print(f"没有 “{row}” 这个维度")
                label_list.remove(row)

        # 将每个列表创建counter
        total_list = []
        for label in label_list:

            list_ = []

            for i in range(len(json_file)):

                if isinstance(json_file[i][f"{label}"], list):
                    for j in range(len(json_file[i][f"{label}"])):
                        list_.append(json_file[i][f"{label}"][j])
                elif isinstance(json_file[i][f"{label}"], str):
                    list_.append(json_file[i][f"{label}"])
                else:
                    list_.append(json_file[i][f"{label}"])

            total_list.append(list_)
        return total_list, label_list, flag

    @staticmethod
    def create_table_and_output(total_list, label_list):
        """
        创建表格并输出
        :param total_list:待创建counter的列表
        :param label_list:要统计的维度（key）列表
        :return:
        """
        index = 0
        for list_ in total_list:

            counter = Counter(list_)
            # 降序
            sorted_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
            # 制表
            table = PrettyTable()
            table.align = "l"  # 左对齐
            table.field_names = ["key", "value"]
            for key, value in sorted_counter:
                table.add_row([key, value])
            print(label_list[index], ":")
            print(table)
            index += 1

    def start(self, label_list):
        """
        开始统计
        :param label_list: 要统计的维度（key）列表
        :return:
        """
        json_file = self.open_file()

        total_list, label_list, flag = self.append_in_list(json_file, label_list)
        if flag:
            self.create_table_and_output(total_list, label_list)
