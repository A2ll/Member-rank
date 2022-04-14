import pandas as pd
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication
import sys

from loguru import logger
from tqdm import tqdm

from csv_pretreatment import DataPre
from tree_func import Tree


class WorkThread(QThread):
    trigger = pyqtSignal(str)

    def __init__(self):
        super(WorkThread, self).__init__()
        self.sid = None
        self.key_id = None
        self.file_path = None
        self.end_list = None
        self.data_tree = None
        self.target = None

    def set(self, target, file_path, key_id, sid):
        self.target = target
        self.data_tree = 'temp_data.txt'
        self.file_path = file_path
        self.key_id = key_id
        self.sid = sid

    def run(self):
        try:
            self.trigger.emit('层级分析开始···')
            obj = DataPre(self.file_path, self.key_id, self.sid)
            a = obj.read_date()
            self.end_list = obj.end_id_analyse()  # 末端用户id，也就是没有下级会员的人
            all_list = []  # 所有关联id列表
            obj_tree = Tree(self.data_tree)
            tree_list = obj_tree.id_tree_list()
            self.trigger.emit('关联查询开始···')
            logger.info('关联查询开始···')
            with tqdm(total=len(tree_list)) as pbar:
                for line in tree_list:
                    if self.target in line:
                        for key in line:
                            all_list.append(key)
                    pbar.update(1)
            all_list = list(set(all_list))
            num = len(all_list)
            if num == 0:
                self.trigger.emit('输入的关键用户id不存在，请重新确认')
            else:
                out_list = []
                self.trigger.emit('数据计算中，请等待···')
                logger.info('数据计算中，请等待···')
                with tqdm(total=num) as pbar:
                    for id_key in all_list:
                        if id_key in self.end_list:
                            temp = obj_tree.id_query_end(id_key)
                            out_list.append([id_key, temp[0], temp[1], temp[2], temp[3]])
                            self.end_list.remove(id_key)  # 删除已经出现过的数据
                            pbar.update(1)
                        else:
                            temp = obj_tree.id_query(id_key)
                            out_list.append([id_key, temp[0], temp[1], temp[2], temp[3]])
                            pbar.update(1)
                list_name = ['ID', '直接下级', '所有下级', '所在层级', '下线层级数']
                df_ = pd.DataFrame(columns=list_name, data=out_list)
                df_.to_excel('查询结果.xlsx')
                logger.success('分析完成，详见\'查询结果.xlsx\'')
                self.trigger.emit('分析完成，详见\'查询结果.xlsx\'')
        except Exception as e:
            logger.warning(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = WorkThread()
    t.set('1051666', 'm_member_info_202102011442.xlsx', 'id', 'sid')
    t.run()
