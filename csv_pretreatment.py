import os

import pandas as pd
from PyQt5.QtCore import pyqtSignal, QThread
from loguru import logger
from collections import Counter

from tqdm import tqdm

from UI import Ui_Form

'''
数据预处理程序，将推荐人ID和用户ID进行树形结构整理
'''


class DataPre(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, file_path, key_id, sid):
        super(DataPre, self).__init__()
        self.sid = sid
        self.key_id = key_id
        self.file_path = file_path
        self.df = None
        self.cate_dict = None

    def read_date(self):
        logger.info('开始执行读取文件···')
        self.df = pd.read_excel(self.file_path)
        return self.df

    def run(self):
        try:
            self.trigger.emit('程序开始运行')  # 传回线程数据
            self.read_date()
            flog = self.data_id_recheck()
            if flog == 0:
                logger.info('开始创建推荐树···')
                global word
                end_id_list = self.end_id_analyse()
                try:
                    os.remove('temp_data.txt')
                except:
                    pass
                with tqdm(total=len(end_id_list)) as pbar:
                    for end_id in end_id_list:
                        f = open('temp_data.txt', 'a', encoding='utf-8')
                        word = ''
                        word = word + str(end_id)
                        try:
                            while 1 == 1:
                                word = word + '-' + str(self.cate_dict[end_id])
                                end_id = self.cate_dict[end_id]
                        except KeyError:
                            f.write(word + '\n')
                            f.close()
                        pbar.update(1)
                logger.success('数据预处理完成！\n')
                self.trigger.emit('数据预处理完成！')  # 传回线程数据
        except KeyError as e:
            logger.warning(e)
            self.trigger.emit('确认输入的用户id字段名和推荐id字段名是否正确,错误信息：' + str(e))  # 传回线程数据

    def data_id_recheck(self):  # 对用户id进行检查，查看是否用户id值唯一
        logger.info('数据异常检测开始执行···')
        flog = 0
        dict_temp = Counter(self.df[self.key_id].values)
        for k, v in dict_temp.items():
            if v > 1:
                logger.warning('发现重复id：' + str(k))
                flog = flog + 1
        if flog == 0:
            logger.success('数据检测正常！')
            self.trigger.emit('数据检测正常！')  # 传回线程数据
            return 0

    def data_dict(self):  # 将用户id和推荐id进行字典化，加快匹配速度
        logger.info('开始数据字典化···')
        dict_temp = self.df[[self.key_id, self.sid]].to_dict(orient='split')
        self.cate_dict = dict()
        for pair in dict_temp['data']:
            key_v = pair[0]
            self.cate_dict[key_v] = pair[1]
        return self.cate_dict

    def end_id_analyse(self):  # 获取并确认末端用户，确定推荐线路图
        logger.info('确认推荐树最底层用户信息···')
        self.data_dict()
        end_id_list = []
        id_list = self.cate_dict.keys()
        sid_list = self.cate_dict.values()
        sid_list = set(sid_list)
        for id_temp in id_list:
            if id_temp not in sid_list:
                end_id_list.append(id_temp)
        return end_id_list


if __name__ == '__main__':
    obj = DataPre('m_member_info_202102011442.xlsx', 'id', 'sid')
    obj.run()
