# -*- coding: utf-8 -*-
import time

import openai
import json
import random
import re
import os
from dataclasses import dataclass
import queue
import threading
import datetime

openai.api_key = '43hUgmEfQB65uyqckUOS9IYSQdLQSYin'
openai.api_base = "https://gptproxy.llmpaas.tencent.com/v1"


@dataclass
class CreateData(object):
    pool_data_file_path: str
    case_data_file_path: str
    file_storage_path: str
    kind: int

    def load_original_data(self):
        """
        加载原始数据文件：话题池、例子
        :return:
        """
        # 读取话题库
        with open(self.pool_data_file_path, encoding='utf-8') as f1:
            topic_data = json.load(f1)

    @staticmethod
    def random_get_three_data(topic_data):
        """
        从话题池中挑选数据
        :param topic_data: 话题池
        :return:
        """
        # 从数据中随机选择三个不重复的记录
        selected_data = random.sample(topic_data, 3)
        return selected_data

    def select_prompt(self, selected_data):
        """
        选择不同的prompt
        :param selected_data: 从话题池挑选的三条数据
        :return: prompt
        """
        prompt = ""
        if self.kind == 0:
            prompt = f'''
                    你现在是展厅导览员吉莉。
                    现在是
                    上面有三组数据，各自包含了分类、话题和事实三类信息。请你帮我生成对话数据，下面我将给出一个案例和对你的要求。
                    案例为：
                    user:哎，吉莉姐，你是不是很会玩狙击枪啊？
                    system:对呀，我可是王牌狙击手呢，现在还是一名和平精英特训官呢。
                    user:我也可以成为像你这样优秀的人吗？
                    system:当然可以啦，只要你坚持自己的梦想，然后不断的去努力，相信你也一定可以做到的。加油喔。
                    user:那你的梦想是什么呢？
                    system:我从小的梦想就是成为一名优秀的狙击手呀。
                    user:那你为了这个梦想肯定做过很多努力吧？
                    system:那可不，我经常和我的团队一起训练呢，为的就是早日实现梦想。
                    user:诶，说到团队，那你能介绍一下你的团队信息吗？
                    system:我的团队是一个专业的小队，名字是叫吉莉战队，一共有四个人，拥有智慧的舰长是我们小队的队长，智慧与美貌并存，才华与气质兼具的我是狙击手角色，以及强壮的火力手维克托，还有自由人奥利弗。
                    要求为：
                    1. 提问者是user，他的人物性格是深思熟虑、诚实坦率、目标明确、果敢坚毅、纪律性强、专业精通和性格外向等。回答者是system，她的性格是比较活泼好动，非常英姿飒爽，比较具有亲活力；
                    2. 我给的数据里面里面会有几个分类，其中'吉莉'这个分类里面的数据是system在回答时的身份信息；其他的分类里面的数据全部都是吉莉这个人所了解到的知识，与她本身身份无关。
                    3. 生成新对话的时候时候必须遵循提问者和回答者的性格。在生成的问题以及答案中的主语谓语宾语顺序可以更换，也可以变换不同的句式；
                    5. 如果你选择的是一个话题，你必须保证每轮对话之间的连贯性和自然性，如果你选择的是多个话题，在转换话题的时候要比较自然；
                    6. 在提问或者转换话题的时候需要当做不知道我给的事实信息来提问而且还得考虑哪个话题作为对话的开始会比较合理；
                    7. 每一个多轮对话结束后紧跟着在后面加上'###'，最后一个多轮不加'###'。
                    8. 每一个多轮对话前面不准编号是第几轮，直接返回给我对话内容；
                    9. 每一句话后面加上：['分类','话题']表明这句话是围绕哪个话题进行对话的。
                    我现在需要得到3份多轮对话，现在开始生成。'''
        if self.kind == 1:
            pass
        if self.kind == 2:
            prompt = f'''
                    {selected_data[0]}，
                    {selected_data[1]}，
                    {selected_data[2]}。
                    上面有三组数据，各自包含了分类、话题和事实三类信息。请你帮我生成对话，下面我将给出一个案例和对你的要求。
                    案例为：
                    user:哎，吉莉姐，你是不是很会玩狙击枪啊？
                    system:对呀，我可是王牌狙击手呢，现在还是一名和平精英特训官呢。
                    user:我也可以成为像你这样优秀的人吗？
                    system:当然可以啦，只要你坚持自己的梦想，然后不断的去努力，相信你也一定可以做到的。加油喔。
                    user:那你的梦想是什么呢？
                    system:我从小的梦想就是成为一名优秀的狙击手呀。
                    user:那你为了这个梦想肯定做过很多努力吧？
                    system:那可不，我经常和我的团队一起训练呢，为的就是早日实现梦想。
                    user:诶，说到团队，那你能介绍一下你的团队信息吗？
                    system:我的团队是一个专业的小队，名字是叫吉莉战队，一共有四个人，拥有智慧的舰长是我们小队的队长，智慧与美貌并存，才华与气质兼具的我是狙击手角色，以及强壮的火力手维克托，还有自由人奥利弗。
                    user:哇，听起来挺不错的，你们团队合作怎么样呢？
                    user:可以给我详细介绍一下吗，比如所有哪些人，都担任哪些角色那些。
                    要求为：
                    1. 对话中包含两个身份，提问者是user，他的人物性格是深思熟虑、诚实坦率、目标明确，说话方式比较得体。回答者是system，她的性格是活泼好动，英姿飒爽，具有亲活力；
                    2. 所有问题以及回答都使用中文；
                    3. 每一个多轮对话必须包含6对的问题以及答案；
                    4. 生成的对话是自然顺畅、闲聊的，提问的话题是从我提供的三组数据中选取，回答的答案从事实信息中提炼答案,每组数据的话题和事实不能交叉提问；
                    5. 如果你选择的是一个话题，你必须保证每轮对话之间的连贯性和自然性，如果你选择的是多个话题，在转换话题的时候要比较自然；
                    6. 转换话题不能太频繁，最多转换两次话题，已经出现过的话题不允许第二次转换；
                    7. 每个对话开始时从user这个身份开始，system回答的时候可以适当给一些引导性提问，引导user去问给出的话题；
                    8. 在提问以及回答时，不要称呼对方的身份角色；
                    9. 最后两轮对话在对话时不允许转换话题；
                    10.对话的最后一个问题是由user提出，需要对上个问题进行深入提问，来达到补充说明的效果；
                    11.每一句话后面加上：['分类','话题']表明这句话是围绕哪个话题进行对话的；
                    12.每一个多轮对话结束后紧跟着在后面加上‘###’不要有换行符以及多余的空格，最后一个多轮对话不加‘###’；
                    我现在需要得到2份多轮对话，现在开始生成。'''

        if self.kind == 3:
            pass
        if self.kind == 4:
            prompt = f'''
                    {selected_data[0]}
                    上面是一条数据：包含了分类、话题和事实三类信息。请你帮我生成对话，下面我将给出一个案例和对你的要求。
                    案例为：
                    user:你的梦想是什么？
                    system:我从小的梦想就是成为一名优秀的狙击手呀。
                    要求为：
                    1. 对话中包含两个身份，提问者是user，他的人物性格是深思熟虑、诚实坦率、目标明确，说话方式比较得体。回答者是system，她的性格是活泼好动，英姿飒爽，具有亲活力；
                    2. 根据我提供的话题和事实信息进行提问以及回答，不允许偏离我提供的话题和事实；
                    3. 生成的对话是自然顺畅、闲聊的，提问的话题是从我提供的三组数据中选取，回答的答案从事实信息中提炼答案,每组数据的话题和事实不能交叉提问；
                    4. 在生成的问题以及答案中的主语谓语宾语顺序可以更换，也可以变换不同的句式；
                    5. 所有问题以及回答都使用中文；
                    6. 在所有的答案中永远不要写表达自己是AI或者是人工智能这种话术；
                    7. 每一句话后面加上：['分类','话题']表明这句话是围绕哪个话题进行对话的；
                    8. 每一个对话结束后紧跟着在后面加上‘###’不要有换行符以及多余的空格，最后一个多轮对话不加‘###’；
                    我现在需要得到3份对话，现在开始生成。'''
        return prompt

    def calling_gpt(self):
        """
        调用gpt生产数据并存入队列
        :return:
        """
        try:
            selected_data, model_replay = "", ""
            with open(self.pool_data_file_path, encoding='utf-8') as f1:
                topic_data = json.load(f1)
            selected_data = self.random_get_three_data(topic_data)
            prompt = self.select_prompt(selected_data)
            # 调用gpt接口
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system",
                     "content": '你的名字是吉莉，原本是腾讯的一款游戏《和平精英》的一个角色，目前你是一名腾讯Air square 展厅的导览员，该展厅展示腾讯人工智能实验室和机器人实验室的先进技术和产品。'},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6
            )
            # 获取模型返回结果
            model_replay = completion.choices[0].message.content

            return selected_data, model_replay
        except Exception as e:
            print(f"error:{e}")
            return selected_data, model_replay

    def gpt_result_processing(self, selected_data, model_replay):
        """
        循环消费数据
        :return:
        """
        try:
            model_replay = re.sub('###\n', '###',
                                  re.sub(r'\n\n###', '###',
                                         re.sub(r'\n###', '###',
                                                re.sub(r'\n\n', '\n',
                                                       re.sub('### ', '###', model_replay))))).split('###')
            # 循环出返回的结果并放入result
            for j in range(len(model_replay)):
                result = model_replay[j].strip().split('\n')

                new_result = []
                for w in result:
                    w = re.sub(": ", ":", w)
                    inx = w.find(":")
                    sub_w = w[inx + 1:]
                    new_result.append(sub_w)
                # 处理异常
                if len(new_result) % 2 != 0:
                    new_result.pop()
                if len(new_result) >= 2:
                    if self.kind == 4:
                        # 存单轮数据
                        for index in range(0, len(new_result), 2):
                            tmp_dict = {"tag": [selected_data[0]["class"]],
                                        "cls": "单轮",
                                        "topic": [selected_data[0]["topic"]],
                                        "fact": [selected_data[0]["mess"]],
                                        "topic_number": 1,
                                        "circle_number": 1,
                                        "label": "gpt",
                                        "interrupt": 0,
                                        "dialog": {"user": new_result[index].strip(),
                                                   "system": new_result[index + 1].strip()}}

                            with open(self.file_storage_path, 'a', encoding='utf-8') as f:  # 使用utf-8编码打开文件
                                json.dump(tmp_dict, f, ensure_ascii=False, indent=2)  # 确保不将非ASCII字符转为\xxxx形式
                            print(tmp_dict)
                    else:
                        # 存多轮数据
                        user = []
                        system = []
                        for index in range(0, len(new_result), 2):
                            # 处理每句话前后空格并加入列表
                            user.append(new_result[index].strip())
                            system.append(new_result[index + 1].strip())
                        tmp_dict = {
                            "tag": [selected_data[0]["class"], selected_data[1]["class"],
                                    selected_data[2]["class"]],
                            "cls": "多轮",
                            "topic": [selected_data[0]["topic"], selected_data[1]["topic"],
                                      selected_data[2]["topic"]],
                            "fact": [selected_data[0]["mess"], selected_data[1]["mess"],
                                     selected_data[2]["mess"]],
                            "topic_number": 3,
                            "circle_number": int(len(new_result) / 2),
                            "label": "gpt",
                            "interrupt": self.kind,
                            "dialog": {"user": user, "system": system}}

                        with open(self.file_storage_path, 'a', encoding='utf-8') as f:  # 使用utf-8编码打开文件
                            json.dump(tmp_dict, f, ensure_ascii=False, indent=2)  # 确保不将非ASCII字符转为\xxxx形式
                        print(tmp_dict)
        except Exception as e:
            print("保存数据时error：", e, )

    def start_create_data(self):
        selected_data, model_replay = self.calling_gpt()
        self.gpt_result_processing(selected_data, model_replay)
        # 生产数据

    def start(self, count):
        for inx in range(count):
            producer_thread = threading.Thread(target=self.start_create_data)
            producer_thread.start()
            # time.sleep(0.5)


if __name__ == '__main__':
    file_path = "out_gai2.jsonl"
    topic_file_path = "../../topic_splitting/topic_pool/topic_pool_original_1113.json"
    case_file_path = "../../topic_splitting/case_pool/case_pool_original_1113.json"

    # # 制造数据
    create = CreateData(pool_data_file_path=topic_file_path, case_data_file_path=case_file_path,
                        file_storage_path=file_path,
                        kind=2)

    create.start(10)