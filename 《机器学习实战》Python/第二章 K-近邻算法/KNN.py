from numpy import *
import operator
import os


######################################################################
#
# 说明：
#   KNN算法实现
#
# 参数：
#   sample_data[in][numpy.array]: 输入待测试实例
#   train_data[in][numpy.array]: 训练样本
#   class_data[in][list]: 样本对应的类别
#   k[in]: KNN中的k，即前k个最近距离
#
def knn_classify(sample_data, train_datas, class_datas, k):
    # 计算欧式距离：sqrt[(x1 - x2)^2 + (y1 - y2)^2 + ...]
    row_count = train_datas.shape[0]
    diff_data = tile(sample_data, (row_count, 1)) - train_datas
    diff_data_sqrt = diff_data ** 2
    diff_data_distances = diff_data_sqrt.sum(axis=1)
    euclid_distances = diff_data_distances ** 0.5

    # 根据距离排序
    sorted_indexes = euclid_distances.argsort()

    # 统计前k个距离最近样本的类别
    class_count = {}
    for i in range(k):
        class_type = class_datas[sorted_indexes[i]]
        class_count[class_type] = class_count.get(class_type, 0) + 1

    # 输出最多类别为测试实例类别
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


######################################################################
# 示例 1: 电影分类
def create_movie_datas():
    train_movie_datas = array([[1, 101], [5, 89], [108, 5], [115, 8]])
    class_movie_datas = ["love", "love", "action", "action"]
    return train_movie_datas, class_movie_datas


def movie_run():
    movie_train_datas, movie_class_datas = create_movie_datas()
    movie_result = knn_classify(array([101, 20]), movie_train_datas, movie_class_datas, 3)
    print(movie_result)


######################################################################
# 示例 2: 海伦约会分类
#
# 说明：
#   将数据文件样本内容转换为相应格式
#
def file_to_matrix(file_name):
    fp = open(file_name)
    lines = fp.readlines()
    line_count = len(lines)
    train_datas = zeros((line_count, 3))
    class_datas = []
    index = 0
    for line in lines:
        line = line.strip()
        elems = line.split('\t')
        train_datas[index, :] = elems[0:3]
        class_datas.append(elems[-1])
        index += 1
    return train_datas, class_datas


#
# 说明：
#   特征归一化
#
def auto_normalization(datas):
    # 计算最值
    min_value = datas.min(0)
    max_value = datas.max(0)
    ranges = max_value - min_value
    # 归一化：value = (value - min) / (max - min)
    normal = datas - tile(min_value, (datas.shape[0], 1))
    normal = normal / tile(ranges, (datas.shape[0], 1))
    return normal


def dating_run():
    # 加载数据并归一化
    train_dating_datas, class_dating_datas = file_to_matrix("./datingTestSet.txt")
    normal_data = auto_normalization(train_dating_datas)

    # 留出法分割数据为训练集和测试集
    # 测试集：test[0:test_num]；训练集train[test_num:]
    test_ratio = 0.10
    test_num = int(test_ratio * normal_data.shape[0])

    # 应用kNN算法，并统计错误率
    error_count = 0.0
    for i in range(test_num):
        class_result = knn_classify(normal_data[i, :], normal_data[test_num:, :],
                                    class_dating_datas[test_num:], 3)
        if class_result != class_dating_datas[i]:
            error_count += 1.0
        print("the classifier came back with: %s, the real answer is: %s" % (class_result, class_dating_datas[i]))
    print("the total error rate is: %f" % (error_count / float(test_num)))


######################################################################
# 示例 3：手写识别
#
# 将数据文件样本内容转换为相应格式(每张图片生成一个行向量)
# 图片大小：32x32
# 向量大小：1024
#
def image_to_vector(file_name):
    vector = zeros((1, 1024))
    fp = open(file_name)
    for i in range(32):
        line = fp.readline()
        for j in range(32):
            vector[0, 32 * i + j] = int(line[j])
    return vector


def hand_run():
    # 加载训练数据集
    train_file_list = os.listdir("trainingDigits")
    train_file_num = len(train_file_list)
    train_hand_datas = zeros((train_file_num, 1024))
    class_hand_datas = []
    for i in range(train_file_num):
        file_name = train_file_list[i].split(".")[0]
        class_type = int(file_name.split("_")[0])
        class_hand_datas.append(class_type)
        train_hand_datas[i, :] = image_to_vector("trainingDigits/%s" % train_file_list[i])

    # 加载测试数据集, 并依次测试统计
    test_file_list = os.listdir("testDigits")
    test_file_num = len(test_file_list)
    error_count = 0.0
    for i in range(test_file_num):
        file_name = test_file_list[i].split(".")[0]
        class_type = int(file_name.split("_")[0])
        test_vector = image_to_vector("testDigits/%s" % test_file_list[i])
        class_result = knn_classify(test_vector, train_hand_datas, class_hand_datas, 3)
        if class_result != class_type:
            error_count += 1.0
        print("the classifier came back with: %d, the real answer is: %d" % (class_result, class_type))
    print("\n the total number of errors is: %d" % error_count)
    print("\n the total error rate is: %f" % (error_count / float(test_file_num)))


if __name__ == '__main__':
    movie_run()
    #dating_run()
    #hand_run()
