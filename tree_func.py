class Tree(object):
    def __init__(self, data_tree):
        self.data_tree = data_tree
        self.tree_list = []

    def id_tree_list(self):  # 将整理的关系数进行列表化
        with open(self.data_tree, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split('\n')
                line = line[0].split("-")
                self.tree_list.append(line)
        return self.tree_list

    def find_num(self, target):  # 查找所有下级ID
        tree_num = []
        list_one = []
        for list_temp in self.tree_list:
            if target in list_temp:
                tree_num.append(len(list_temp))
                for temp in list_temp:
                    list_one.append(temp)
            else:
                pass
        set_list = list(set(list_one))
        all_id = len(set_list)
        return [all_id, max(tree_num)]  # 第一个返回值是'所有下级+自身+所有上级的数量和',第二个返回值是最长的路径层数

    def sid_num(self, target):  # 获取目标id所在层级
        for line in self.tree_list:
            if target in line:
                num = len(line) - line.index(target)
                return num

    def immediate_num(self, target):  # 获取目标i直接下级会员
        immediate_list = []
        for line in self.tree_list:
            if target in line:
                i = line.index(target)
                if i == 0:
                    return 0
                if line[i - 1] not in immediate_list:
                    immediate_list.append(line[i - 1])
        return len(immediate_list)

    def id_query(self, id_key):
        num3 = self.sid_num(id_key)
        num1 = self.immediate_num(id_key)
        num_ = self.find_num(str(id_key))
        num2 = num_[0] - num3
        num4 = num_[1] - num3
        return [num1, num2, num3, num4]  # 1、直接下级、2、所有下级 3、所在层级 4、下线层级数

    def id_query_end(self, id_key):
        num3 = self.sid_num(id_key)
        num1 = 0
        num2 = 0
        num4 = 0
        return [num1, num2, num3, num4]  # 1、直接下级、2、所有下级 3、所在层级 4、下线层级数


if __name__ == '__main__':
    obj = Tree('temp_data.txt')
    obj.id_tree_list()
    key = '1000014'
    all_id_num = obj.find_num(key)
    print(all_id_num)
