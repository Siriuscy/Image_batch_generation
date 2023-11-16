import queue
import threading
import time

from create_data import CreateData


from postprocessing_and_statistics.statistic_by_dims import StatisticByDims
from postprocessing_and_statistics.data_final_processing import DataFinalProcessing
from postprocessing_and_statistics.modal_particles_processing import ModalParticlesProcessing

if __name__ == '__main__':
    file_path = "out.jsonl"
    topic_file_path = "../topic_splitting/topic_pool/topic_pool_original_1113.jsonl"
    case_file_path = "../topic_splitting/case_pool/case_pool_original_1113.jsonl"

    # # 制造数据
    create = CreateData(pool_data_file_path=topic_file_path, case_data_file_path=case_file_path,
                        file_storage_path=file_path,
                        kind=4)

    create.start_create_data(100)

    # # 语气词处理
    # processor_2 = ModalParticlesProcessing(file_path=file_path)
    # processor_2.statistics_modal_particles(dim_list=["单轮", "多轮"], sub_dim_list=["user", "system"], length=9)
    # processor_2.del_modal_particles("当然知道啦", dim_list=["单轮", "多轮"], sub_dim_list=["user", "system"], length=9,
    #                                 number=2)
    # # 分维度统计
    # statistic_by_dims = StatisticByDims(file_path=file_path)
    # statistic_by_dims.start(["class","topic","sub_topic"])
    #
    # # 数据最终处理
    # processor_1 = DataFinalProcessing(file_path=file_path)
    # processor_1.cut_data("system", 0, 5)
    # processor_1.remove_spaces(["user", "system"
    # processor_1.error_data_processing()
