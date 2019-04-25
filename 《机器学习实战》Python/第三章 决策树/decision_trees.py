from numpy import *
from math import log
import operator


######################################################################
#
# 说明：
#   计算信息熵
# 参数：
#   datas[in][list]：输入数据集
#
def calc_shannon_ent(datas):
    # 计算数据集中各分类数目
    classes = {}
    for line in datas:
        class_type = line[-1]
        classes[class_type] = classes.get(class_type, 0) + 1

    # 计算香农熵
    # H = -Σp(xi)log(p(xi))
    row = len(datas)
    shannon_ent = 0.0
    for key in classes:
        prob = float(classes[key]) / row
        shannon_ent -= prob * log(prob, 2)

    return shannon_ent


#
# 说明：
#   划分数据集。将数据集datas按照属性feac划分为各个子集
# 参数：
#   datas[in][list]：待划分数据集
#   feac_index[in]：要划分的属性值索引
#   value[in]：本次划分出的子集的feac值
#   new_datas[out]：按照feac=value划分出的子集
#
def split_datas(datas, feac_index, value):
    new_datas = []
    for line in datas:
        if line[feac_index] == value:
            reduced_line = line[:feac_index]
            reduced_line.extend(line[feac_index + 1:])
            new_datas.append(reduced_line)
    return new_datas


#
# 说明：
#   寻找最佳特征用于划分
#
def choose_best_feac(datas):
    best_gain = 0.0
    best_feac = -1
    feac_num = len(datas[0]) - 1

    # 计算父数据集香农熵
    base_ent = calc_shannon_ent(datas)

    # 依次计算按照每个特征划分后的香农熵
    # 找出获得最大信息增益的特征
    for feac in range(feac_num):
        # 统计该特征所有可能值
        feac_list = [example[feac] for example in datas]
        feac_unique = set(feac_list)
        # 按所有可能值对该特征划分子集，并计算子集上的香农熵
        # 子集香农熵 = 各个子集划分比例 * 各个子集数据香农熵
        sub_ent = 0.0
        for value in feac_unique:
            sub_datas = split_datas(datas, feac, value)
            prob = len(sub_datas) / float(len(datas))
            sub_ent += prob * calc_shannon_ent(sub_datas)
        # 计算该特征的信息增益，如果按该特征划分获得的信息增益最好则记录
        gain = base_ent - sub_ent
        if gain > best_gain:
            best_gain = gain
            best_feac = feac

    return best_feac


#
# 说明：
#   返回频率最高的类别。
#
def majority_cnt(classes):
    classes_count = {}
    for key in classes:
        classes_count[key] = classes_count.get(key, 0) + 1
    sorted_classes_count = sorted(classes_count.iteritems(), key=operator.itemgetter(1),reverse=True)
    return sorted_classes_count[0][0]


#
# 说明：
#   创建决策树
# 参数：
# datas[in][list]：数据样本集
# feac_descs[in][list]：特征名称，仅用于标注
# tree[out][map]：返回的决策树，各节点保存为[map]类型
#
def create_tree(datas, feac_descs):
    # 返回条件：数据集中所有样本属于同一类，返回此类别
    datas_classes = [example[-1] for example in datas]
    if datas_classes.count(datas_classes[0]) == len(datas_classes):
        return datas_classes[0]

    # 返回条件：没有可继续划分的特征，返回数目最多的类标签
    if len(datas[0]) == 1:
        return majority_cnt(datas_classes)

    # 选择最佳划分特征
    best_feac = choose_best_feac(datas)
    best_feac_desc = feac_descs[best_feac]
    del(feac_descs[best_feac])

    # 按最佳特征的所有可能值划分
    tree = {best_feac_desc: {}}
    feac_values = [example[best_feac] for example in datas]
    feac_unique = set(feac_values)
    for value in feac_unique:
        sub_datas = split_datas(datas, best_feac, value)
        sub_feac_descs = feac_descs[:]
        tree[best_feac_desc][value] = create_tree(sub_datas, sub_feac_descs)

    return tree


if __name__ == '__main__':
    fr = open("lenses.txt")
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    descs = ["age", "prescript", "astigmatic", "tearRate"]
    tree = create_tree(lenses, descs)
    print(tree)

