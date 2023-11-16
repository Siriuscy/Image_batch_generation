import json
from collections import Counter
from prettytable import PrettyTable


class ModalParticlesProcessing(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def statistics_modal_particles(self, dim_list, sub_dim_list, length):
        """
        从不同维度统计对话中语气词
        :param dim_list: 第一维度：单轮或多轮或一起统计
        :param sub_dim_list: 第二维度：user或system或一起统计
        :param length: 语气词长度标准，表示length前多少位为语气词
        :return:
        """
        with open(self.file_path, encoding='utf-8') as f:
            data = []
            for line in f:
                data.append(json.loads(line))

        modal_particles_number = 0
        total_count = 0

        counter_list = []

        for i in range(len(data)):
            # 遍历第一维度，判断是单轮数据还是多轮数据
            for dim in dim_list:
                if data[i]["cls"] == dim == "多轮":
                    # 遍历第二维度，判断是user还是system
                    for sub_dim in sub_dim_list:
                        s = data[i]["dialog"][sub_dim]

                        for j in range(len(s)):

                            # 查找“，”所在index
                            index = s[j][:length].find('，') if (
                                s[j][:length].find('，') < s[j][:length].find('，')
                                if s[j][:length].find('！') != -1 else s[j][:length].find('！')) \
                                else s[j][:length].find('！')
                            index2 = s[j][:length].find('！') if (
                                s[j][:length].find('！') < s[j][:length].find('！')
                                if s[j][:length].find('，') != -1 else s[j][:length].find('，')) \
                                else s[j][:length].find('，')
                            if index == -1:
                                index = s[j][:length].find('！')
                            index = index if index < index2 else index2

                            # 截取语气词
                            substring = s[j][:index]
                            total_count += 1
                            if index != -1:
                                # 将所有的语气词存进列表
                                counter_list.append(substring)
                                modal_particles_number += 1
                elif data[i]["cls"] == dim == "单轮":
                    for sub_dim in sub_dim_list:
                        s = data[i]["dialog"][sub_dim]

                        # 查找“，”所在index
                        index = s[:length].find('，') if (
                            s[:length].find('，') < s[:length].find('，') if
                            s[:length].find('！') != -1 else s[:length].find('！')) else s[:length].find('！')
                        index2 = s[:length].find('！') if (
                            s[:length].find('！') < s[:length].find('！') if
                            s[:length].find('，') != -1 else s[:length].find('，')) else s[:length].find('，')
                        if index == -1:
                            index = s[:length].find('！')
                        index = index if index < index2 else index2

                        # 截取语气词
                        substring = s[:index]
                        total_count += 1
                        if index != -1:
                            # 将所有的语气词存进列表
                            counter_list.append(substring)
                            modal_particles_number += 1

        # 统计语气词列表中各元素个数
        counter = Counter(counter_list)
        print("modal_particles_number:", modal_particles_number)
        print("total_number:", total_count)
        # 降序
        sorted_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        # 制表
        table = PrettyTable()
        table.field_names = ["key", "count", "single_percentage", "total_percentage"]

        for key, value in sorted_counter:
            table.add_row([key, value, f"{value / total_count:.2%}", f"{modal_particles_number / total_count:.2%}"])

        print(table)

    def del_modal_particles(self, modal_particles, dim_list, sub_dim_list, length, number=0):
        """
        批量删除语气词
        :param modal_particles: 待删除的语气词
        :param dim_list: 第一维度：单轮或多轮或一起处理
        :param sub_dim_list: 第二维度：user或system或一起处理
        :param length: 语气词长度标准，表示length前多少位为语气词
        :param number: 待删除语气词个数
        :return:
        """

        modal_particles_number = 0  # 有语气词句子条数
        total_count = 0  # 总句子条数
        flag = 1
        i_value = []  # 每条数据的索引值列表
        dim_value = []  # 每条数据的第一维度列表
        sub_dim_value = []  # 每条数据的第二维度列表
        j_value = []  # 每条数据的第二维度内元素索引值
        str_value = []  # 切割语气词后的句子列表
        counter_list = []  # 所有语气词列表

        # 加载文件
        with open(self.file_path, encoding='utf-8') as f:
            data = []
            for line in f:
                data.append(json.loads(line))

        for i in range(len(data)):
            # 遍历第一维度，判断是单轮数据还是多轮数据
            for dim in dim_list:
                if data[i]["cls"] == dim == "多轮":
                    # 遍历第二维度，判断是user还是system
                    for sub_dim in sub_dim_list:
                        s = data[i]["dialog"][sub_dim]

                        for j in range(len(s)):

                            # 查找“，”所在index
                            index = s[j][:length].find('，') if (
                                s[j][:length].find('，') < s[j][:length].find('，') if
                                s[j][:length].find('！') != -1 else
                                s[j][:length].find('！')) else s[j][:length].find('！')
                            index2 = s[j][:length].find('！') if (
                                s[j][:length].find('！') < s[j][:length].find('！') if
                                s[j][:length].find('，') != -1 else
                                s[j][:length].find('，')) else s[j][:length].find('，')
                            if index == -1:
                                index = s[j][:length].find('！')
                            index = index if index < index2 else index2

                            # 截取语气词
                            substring = s[j][:index]

                            total_count += 1
                            if index != -1 and substring == modal_particles:
                                cut_data = s[j][index + 1:]
                                # print(cut_data)
                                # 将所有的语气词存进列表
                                counter_list.append(substring)

                                i_value.append(i)
                                dim_value.append("多轮")
                                sub_dim_value.append(sub_dim)
                                j_value.append(j)
                                str_value.append(cut_data)
                                modal_particles_number += 1
                elif data[i]["cls"] == dim == "单轮":
                    for sub_dim in sub_dim_list:
                        s = data[i]["dialog"][sub_dim]

                        # 查找“，”所在index
                        index = s[:length].find('，') if (
                            s[:length].find('，') < s[:length].find('，') if
                            s[:length].find('！') != -1 else s[:length].find('！')) else s[:length].find('！')
                        index2 = s[:length].find('！') if (
                            s[:length].find('！') < s[:length].find('！') if
                            s[:length].find('，') != -1 else s[:length].find('，')) else s[:length].find('，')
                        if index == -1:
                            index = s[:length].find('！')
                        index = index if index < index2 else index2

                        # 截取语气词
                        substring = s[:index]

                        total_count += 1
                        if index != -1 and substring == modal_particles:
                            # 删除语气词后数据
                            cut_data = s[index + 1:]
                            # 将所有的语气词存进列表
                            counter_list.append(substring)
                            # 将本条数据的索引值存入列表
                            i_value.append(i)
                            # 将本条数据的类型存入列表
                            dim_value.append("单轮")
                            # 将本条数据的user或system存入列表
                            sub_dim_value.append(sub_dim)
                            # 将本条数据中user或system内的索引存入列表
                            j_value.append(1)
                            # 将删除语气词后数据存入列表
                            str_value.append(cut_data)
                            modal_particles_number += 1

        # 当要删除输入数量大于实际删除数量时：
        if number > len(i_value):
            number = len(i_value)

        if len(i_value) == 0:
            print(f"语气词 '{modal_particles}' 未找到，请换一个语气词。")
        else:
            # 删除语气词
            for row in range(len(i_value)):
                if dim_value[row] == "单轮":
                    data[i_value[row]]["dialog"][sub_dim_value[row]] = str_value[row]
                    if row + 1 == number and row + 1 != 0:
                        print(f"已删除语气词为：‘{modal_particles}’的{number}个数据")
                        flag = 0
                        break
                else:
                    data[i_value[row]]["dialog"][sub_dim_value[row]][j_value[row]] = str_value[row]
                    if row + 1 == number and row + 1 != 0:
                        print(f"已删除语气词为：‘{modal_particles}’的{number}个数据")
                        flag = 0
                        break
            if (number == 0 or number == len(i_value)) and flag:
                print(f"已删除语气词为：‘{modal_particles}’的{len(i_value)}个数据")
            with open(self.file_path, 'w', encoding='utf-8') as f:  # 使用utf-8编码打开文件
                for item in data:
                    json.dump(item, f, ensure_ascii=False)
                    f.write('\n')
