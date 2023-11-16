import json


class DataFinalProcessing(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def get_json_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:  # 使用utf-8编码打开文件
            data = []
            for line in file:
                data.append(json.loads(line))
        return data

    def save_file(self, data):
        with open(self.file_path[:-5]+"_change.jsonl", 'w', encoding='utf-8') as file2:  # 使用utf-8编码打开文件
            for item in data:
                json.dump(item, file2, ensure_ascii=False)
                file2.write('\n')

    def cut_data(self, target, sub_index, proportion):
        """
        处理数据
        :param target: 要处理的数据的key，取值为user或者system
        :param sub_index: user或者system的索引
        :param proportion: 比例，取值为1-10之间整数，eg：3 表示前30%条数据截取30%，后70%条数据全截
        :return: None
        """
        # 读取原始数据
        data = self.get_json_data()
        flag = 1
        if 1 < int(proportion) < 10:
            # 总数据条数少于10条时，比例对半分
            seq = int(proportion) * int(len(data) / 10)
            if len(data) < 10:
                seq = int(len(data) / 2)

            for index in range(seq):

                if isinstance(data[index]["dialog"][target], list):
                    # 找“[”出现的位置
                    inx = data[index]["dialog"][target][sub_index].rfind('[')
                    # 截取话题
                    topic = self.topic_label_processing(data[index]["dialog"][target][sub_index][inx:])

                    data[index]["dialog"][target][sub_index] = data[index]["dialog"][target][sub_index][
                                                               :int(len(
                                                                   data[index]["dialog"][target][
                                                                       sub_index][:inx]) / 3)] + "......" + topic

                elif isinstance(data[index]["dialog"][target], str):
                    # 找“[”出现的位置
                    inx = data[index]["dialog"][target].rfind('[')
                    # 截取话题
                    topic = self.topic_label_processing(data[index]["dialog"][target][inx:])

                    data[index]["dialog"][target] = data[index]["dialog"][target][
                                                    :int(len(
                                                        data[index]["dialog"][target][:inx]) / 3)] + "......" + topic

            for index in range(seq, len(data)):

                if isinstance(data[index]["dialog"][target], list):
                    # 找“[”出现的位置
                    inx = data[index]["dialog"][target][sub_index].rfind('[')
                    # 截取话题
                    topic = self.topic_label_processing(data[index]["dialog"][target][sub_index][inx:])
                    data[index]["dialog"][target][sub_index] = topic
                elif isinstance(data[index]["dialog"][target], str):
                    # 找“[”出现的位置
                    inx = data[index]["dialog"][target].rfind('[')
                    # 截取话题
                    topic = self.topic_label_processing(data[index]["dialog"][target][inx:])

                    data[index]["dialog"][target] = topic
        else:
            print('比例设置错误')
            flag = 0
        if flag:
            # 存数据
            self.save_file(data)

    def replace_error(self, target, error_str, correct_str):
        """
        处理对话数据格式错误数据
        :param target: 要处理的数据，取值为user或者system
        :param error_str: 错误数据
        :param correct_str: 正确数据
        :return:
        """
        # 获取原数据
        data = self.get_json_data()

        change_list = []

        for index in range(len(data)):
            # 遍历要处理的对话
            for row in data[index]["dialog"][target]:
                # 存在则替换
                if error_str in row:
                    row = row.replace(error_str, correct_str)

                change_list.append(row)
            # 修改数据
            data[index]["dialog"][target] = change_list

            change_list = []

            self.save_file(data)
        print("done")

    @staticmethod
    def topic_label_processing(topic):
        """
        处理话题标签的异常
        :param topic: 待处理的话题标签
        :return: 处理后结果
        """
        content = topic[1:-1]
        tmp_str = content.replace("'", "")
        tmp_list = tmp_str.split(",")
        tmp_list = tmp_list[0:2]
        for i in range(len(tmp_list)):
            tmp_list[i] = tmp_list[i].strip()
            index = tmp_list[i].find(":")
            if index != -1:
                tmp_list[i] = tmp_list[i][index + 1:]
        topic = str(tmp_list)
        return topic

    def error_data_processing(self):
        """
        使用规则库删除有问题句子
        :return:
        """
        # 获取数据
        data = self.get_json_data()
        result_data = []
        single_sentences_list = []
        multiple_sentences_list = []
        for index in range(len(data)):
            if data[index]["cls"] == "单轮":
                # 规则一：轮数大于12轮的视为错误数据
                if data[index]["circle_number"] >= 12:
                    print("单轮数据条数太多")
                    print(data[index])
                    continue

                # 将句子放入句子列表
                single_sentences_list.append(data[index]["dialog"]["user"])
                single_sentences_list.append(data[index]["dialog"]["system"])

                # 规则二：处理单轮数据不是字符型的数据
                if (not isinstance(data[index]["dialog"]["user"], str) or
                        not isinstance(data[index]["dialog"]["system"], str)):
                    print("单轮数据格式不正确")
                    print(data[index])
                    continue

                # 处理格式问题数据
                if self.check_sentence(single_sentences_list):
                    print(data[index])
                    single_sentences_list = []
                    continue

                # 对没有整体错误的句子拆分内容与话题
                content, topic = self.separating_sentences(single_sentences_list[0])
                content2, topic2 = self.separating_sentences(single_sentences_list[1])

                # 处理句子中话题格式错误并重新赋值
                data[index]["dialog"]["user"] = content + self.topic_label_processing(topic)
                data[index]["dialog"]["system"] = content2 + self.topic_label_processing(topic2)

                # 将没有问题的数据加入列表
                result_data.append(data[index])

            elif data[index]["cls"] == "多轮":
                # 规则一：轮数大于12轮的视为错误数据
                if data[index]["circle_number"] >= 12:
                    print("多轮数据条数太多")
                    print(data[index])
                    continue

                # 将句子放入句子列表
                multiple_sentences_list = ([user for user in data[index]["dialog"]["user"]] +
                                           [system for system in data[index]["dialog"]["system"]])

                # 规则二：处理多轮数据里面不是列表的数据和是列表但是只有一条数据的
                if ((not isinstance(data[index]["dialog"]["user"], list) or (  # user类型不是列表或是列表但只有一条数据
                        isinstance(data[index]["dialog"]["user"], list) and len(
                    data[index]["dialog"]["user"]) < 2)) or
                        (not isinstance(data[index]["dialog"]["system"], list) or (  # system类型不是列表或是列表但只有一条数据
                                isinstance(data[index]["dialog"]["system"], list) and len(
                            data[index]["dialog"]["system"]) < 2)) or
                        (len(data[index]["dialog"]["user"]) != len(  # user与system条数不匹配
                            data[index]["dialog"]["system"]))):
                    print("多轮数据格式不正确或数据条数不够")
                    print(data[index])
                    continue

                # 处理格式问题数据
                if self.check_sentence(multiple_sentences_list):
                    print(data[index])
                    multiple_sentences_list = []
                    continue

                # 临时对话列表
                user = []
                system = []

                for sentence_inx in range(len(multiple_sentences_list)):
                    # 对没有整体错误的句子拆分内容与话题
                    content, topic = self.separating_sentences(multiple_sentences_list[sentence_inx])
                    # 处理话题部分格式错误
                    topic = self.topic_label_processing(topic)
                    # 更改错误数据并添加进临时列表
                    if sentence_inx < int(len(multiple_sentences_list) / 2):
                        user.append(content + topic)
                    else:
                        system.append(content + topic)

                # 处理句子中话题格式错误并重新赋值
                data[index]["dialog"]["user"] = user
                data[index]["dialog"]["system"] = system

                # 将没有问题的数据加入列表
                result_data.append(data[index])

            # 每条数据循环完之后置空
            single_sentences_list = []
            multiple_sentences_list = []

        # 保存数据
        self.save_file(result_data)

    @staticmethod
    def separating_sentences(text):
        """
        分割每个句子的内容和话题
        :param text: 句子
        :return:
        """
        # 句子内容
        content = ""
        # 句子话题
        topic = ""

        left_square_bracket = text.rfind('[')
        right_square_bracket = text.rfind(']')

        if left_square_bracket != -1 and right_square_bracket != -1:
            content = text[:left_square_bracket].strip()
            topic = text[left_square_bracket:right_square_bracket + 1].strip()
        return content, topic

    @staticmethod
    def is_contains_chinese(strs):
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
        return False

    def check_sentence(self, sentences_list):
        """
        检查句子是否有问题
        :param sentences_list: 句子列表
        :return:
        """
        for row in range(len(sentences_list)):
            content, topic = self.separating_sentences(sentences_list[row])
            # 规则三：处理句子中没有话题的数据
            if not content or not topic:
                print("无话题数据")
                return True
            # 规则四：处理句子中没有内容的,或内容低于5个字符的数据
            if len(content) <= 3:
                print("无内容数据")
                return True
            # 规则五：处理英文句子
            if not self.is_contains_chinese(content):
                print("含英文数据")
                return True
        return False

    def check_sentence_single(self, sentences_list):
        """
        检查单轮数据句子是否有问题
        :param sentences_list: 句子列表
        :return:
        """
        for row in range(len(sentences_list)):
            # 规则三：处理句子中没有内容的,或内容低于5个字符的数据
            if len(sentences_list[row]) <= 3:
                print("无内容数据")
                return True
            # 规则四：处理英文句子
            if not self.is_contains_chinese(sentences_list[row]):
                print("含英文数据")
                return True
        return False

    # def remove_spaces(self, target_list):
    #     """
    #     处理每句话中话题与内容之间的空格
    #     :param target_list: 要处理的数据列表
    #     :return: None
    #     """
    #     # 获取原始数据
    #     data = self.get_json_data()
    #
    #     change_list = []
    #     for index in range(len(data)):
    #         if data[index]["cls"] == "多轮":
    #             for target in target_list:
    #                 # 遍历要处理数据
    #                 for row in data[index]["dialog"][target]:
    #                     # 找到话题开始符的索引
    #                     inx = row.rfind('[')
    #                     # 删除内容与话题之间的空格
    #                     if inx != -1:
    #                         row = row[:inx].strip() + self.topic_label_processing(row[inx:])
    #                     change_list.append(row)
    #                 # 修改数据
    #                 data[index]["dialog"][target] = change_list
    #                 change_list = []
    #
    #         elif data[index]["cls"] == "单轮":
    #             for target in target_list:
    #                 row = data[index]["dialog"][target]
    #                 # 找到话题开始符的索引
    #                 inx = row.rfind('[')
    #                 if inx != -1:
    #                     # 删除内容与话题之间的空格
    #                     data[index]["dialog"][target] = row[:inx].strip() + self.topic_label_processing(row[inx:])
    #     self.save_file(data)
    #     print("done")
