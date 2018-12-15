from numpy import *
from os import *
import operator


#
# sample[numpy.array]: input sample
# train_data[numpy.array]: samples to train
# class_data[list]: classes the samples belongs to
# k: k number in KNN
#
def knn_classify(sample, train_data, class_data, k):
    row_count = train_data.shape[0]
    # Calculate sqrt[(x1 - x2)^2 + (y1 - y2)^2 + ...]
    diff_data = tile(sample, (row_count, 1)) - train_data
    sqrt_diff_data = diff_data ** 2
    sqrt_distances = sqrt_diff_data.sum(axis=1)
    distances = sqrt_distances ** 0.5
    # Sort and get top K class type
    sort_distances_indexes = distances.argsort()
    class_count = {}
    for i in range(k):
        class_type = class_data[sort_distances_indexes[i]]
        class_count[class_type] = class_count.get(class_type, 0) + 1
    # The maximum class type
    sort_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sort_class_count[0][0]


# Example 1: movie classify
def create_test_movie_set():
    train_movie_data = array([[1, 101], [5, 89], [108, 5], [115, 8]])
    class_movie_data = ["love", "love", "action", "action"]
    return train_movie_data, class_movie_data


def movie_run():
    movie_train_data, movie_class_data = create_test_movie_set()
    movie_result = knn_classify(array([101, 20]), movie_train_data, movie_class_data, 3)
    print(movie_result)


# Example 2: dating classify
def file_to_matrix(file_name):
    fp = open(file_name)
    arr_lines = fp.readlines()
    line_count = len(arr_lines)
    train_data = zeros((line_count, 3))
    class_data = []
    index = 0
    for line in arr_lines:
        line = line.strip()
        line_elems = line.split('\t')
        train_data[index, :] = line_elems[0:3]
        if "didntLike" == line_elems[-1]:
            class_data.append(1)
        elif "smallDoses" == line_elems[-1]:
            class_data.append(2)
        elif "largeDoses" == line_elems[-1]:
            class_data.append(3)
        index += 1
    return train_data, class_data


def auto_normalization(data):
    # The max/min vector
    min_value = data.min(0)
    max_value = data.max(0)
    ranges = max_value - min_value
    # Normalization
    normal = data - tile(min_value, (data.shape[0], 1))
    normal = normal / tile(ranges, (data.shape[0], 1))
    return normal


def dating_run():
    train_data, class_data = file_to_matrix("./datingTestSet.txt")
    normal_data = auto_normalization(train_data)
    # test[0:test_num], train[test_num:]
    test_ratio = 0.10
    test_num = int(test_ratio * normal_data.shape[0])
    error_count = 0.0
    for i in range(test_num):
        class_result = knn_classify(normal_data[i, :], normal_data[test_num:, :],
                                    class_data[test_num:], 3)
        if class_result != class_data[i]:
            error_count += 1.0
        print("the classifier came back with: %d, the real answer is: %d" % (class_result, class_data[i]))
    print("the total error rate is: %f" % (error_count / float(test_num)))


# Hand Writing
def image_to_vector(file_name):
    vector = zeros((1, 1024))
    fp = open(file_name)
    for i in range(32):
        line = fp.readline()
        for j in range(32):
            vector[0, 32 * i + j] = int(line[j])
    return vector


def hand_run(train_dir_name, test_dir_name):
    train_file_list = listdir(train_dir_name)
    file_num = len(train_file_list)
    hand_matrix = zeros((file_num, 1024))
    hand_class = []
    for i in range(file_num):
        file_name_ext = train_file_list[i]
        file_name = file_name_ext.split(".")[0]
        class_type = int(file_name.split("_")[0])
        hand_class.append(class_type)
        hand_matrix[i, :] = image_to_vector("trainingDigits/%s" % file_name_ext)
    test_file_list = listdir(test_dir_name)
    test_file_num = len(test_file_list)
    error_count = 0.0
    for i in range(test_file_num):
        file_name_ext = test_file_list[i]
        file_name = file_name_ext.split(".")[0]
        class_type = int(file_name.split("_")[0])
        test_vector = image_to_vector("testDigits/%s" % file_name_ext)
        class_result = knn_classify(test_vector, hand_matrix, hand_class, 3)
        if class_result != class_type:
            error_count += 1.0
        print("the classifier came back with: %d, the real answer is: %d" % (class_result, class_type))
    print("\n the total number of errors is: %d" % error_count)
    print("\n the total error rate is: %f" % (error_count / float(test_file_num)))


if __name__ == '__main__':
    #movie_run()
    #dating_run()
    hand_run("trainingDigits", "trainingDigits")
