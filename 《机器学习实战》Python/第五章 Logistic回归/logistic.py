from numpy import *


######################################################################
#
# 说明：
#   生成测试数据
#   X0,X1,X2
#
def load_datas():
    datas = []
    classes = []
    fr = open("testSet.txt")
    for line in fr.readlines():
        elems = line.strip().split()
        datas.append([1.0, float(elems[0]), float(elems[1])])
        classes.append(int(elems[-1]))
    return datas, classes


#
# 说明：
#   sigmod函数
# 参数：
#   datas[in][mat]：输入数据
#
def sigmoid(datas):
    return 1.0 / (1 + exp(-datas))


#
# 说明：
#   梯度下降算法实现
# 参数：
#   datas[in][list]：数据集
#   classes[in][list]：类标签
#   weights[out][mat]：模型参数矩阵
#
def grad_ascent(datas, classes):
    # 数据转换为矩阵形式
    datas_mat = mat(datas)
    classes_mat = mat(classes).transpose()

    # 梯度下降迭代训练
    weights = ones((datas_mat.shape[1], 1))
    cycles = 500
    alpha = 0.001
    for cyc in range(cycles):
        h = sigmoid(datas_mat * weights)
        err = (classes_mat - h)
        weights = weights + alpha * datas_mat.transpose() * err
    return weights


#
# 说明：
#   随机梯度下降算法实现。每次只取一个样本训练。
# 参数：
#   datas[in][array]：数据集
#   classes[in][list]：类标签
#   weights[out][array]：模型参数矩阵
#
def stoc_grad_ascent(datas, classes):
    m, n = shape(datas)

    # 随机梯度下降迭代训练
    alpha = 0.01
    weights = ones(n)
    for i in range(m):
        h = sigmoid(sum(datas[i] * weights))
        err = classes[i] - h
        weights = weights + alpha * err * datas[i]
    return weights


#
# 说明：
#   改进的随机梯度下降算法实现。每次只取一个样本训练，alpha值自动调整，训练样本随机采样。
# 参数：
#   datas[in][array]：数据集
#   classes[in][list]：类标签
#   weights[out][array]：模型参数矩阵
#
def stoc_grad_ascent1(datas, classes):
    m, n = shape(datas)

    # 改进随机梯度下降迭代训练，alpha自动适应，数据随机
    cycles = 500
    weights = ones(n)
    for cyc in range(cycles):
        data_indexes = list(range(m))
        for i in range(m):
            alpha = 4 / (1.0 + cyc + i) + 0.01
            rand_index = int(random.uniform(0, len(data_indexes)))
            h = sigmoid(sum(datas[rand_index] * weights))
            err = classes[rand_index] - h
            weights = weights + alpha * err * datas[rand_index]
            del(data_indexes[rand_index])
    return weights


if __name__ == '__main__':
    datas, classes = load_datas()
    #weights = grad_ascent(datas, classes)
    #weights = stoc_grad_ascent(array(datas), classes)
    weights = stoc_grad_ascent1(array(datas), classes)
    print(weights)
