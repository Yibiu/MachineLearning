from numpy import *


######################################################################
#                  vocabulary
#                      |
#                      \/
# documents ---->  documents_vec  ---->  class prob
#                                           |
#                                           \/
# sample    ---->  sample_vec     ---->   sample prob ----> result
#
######################################################################
#
# 说明：
#   生成测试数据
#   1：侮辱性；0：非侮辱性
#
def load_datas():
    posting_datas = [
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    ]
    class_datas = [0, 1, 0, 1, 0, 1]
    return posting_datas, class_datas


#
# 说明：
#   创建词汇表
# 参数
#   datas[in][list]
#
def create_vocabulary(datas):
    vocab = set([])
    for line in datas:
        vocab = vocab | set(line)
    return list(vocab)


#
# 说明
#   将词条生成词汇表向量
# 参数
#   vocab[in][list]：词汇表
#   doc[in][list]：词条
#   words_vec[out][list]：词汇表向量
#
def to_words_vec(vocab, doc):
    words_vec = [0] * len(vocab)
    for i in range(len(vocab)):
        if vocab[i] in doc:
            words_vec[i] = 1
    return words_vec


#
# 说明：
#   朴素贝叶斯算法实现
#   p(ci|w) = p(w|ci)p(ci) / p(w)
#   先验概率：p(ci)
#   后验概率：p(ci|w)
#   调整因子：p(w|ci) / p(w)
#   p(w) = p(w|c0)p(c0) + p(w|c1)p(c1) 全概率公式
#   p(w) 在各种类别下是相同的，因此只需要比较p(w|c0)p(ci0)和p(w|c1)p(c1)即可。
#
# 参数：
#   train_datas[in][array]：训练数据集，由词汇表向量组成
#   class_datas[in][array]：样本对应的类别信息:1：侮辱性；0：非侮辱性
#   p_abusive[out][float]：侮辱性文档概率：p(c0)，p(c1) = 1 - p(c0)
#   p_abusive_vec[out][list]：词汇表侮辱性概率向量：p(w|c0)
#   p_normal_vec[out][list]：词汇表非侮辱性概率向量：p(w|c1)
#
def bayes_classify(train_datas, class_datas):
    num_doc = train_datas.shape[0]
    num_words = train_datas.shape[1]

    # 计算侮辱性文档所占比例：p(c0)
    # 非侮辱性文档比例：p(c1) = 1 - p(c0)
    p_abusive = sum(class_datas) / float(num_doc)

    # 统计词汇表中单词分别在侮辱性和非侮辱性词条中出现的概率：p(wn|ci)
    '''
    p_abusive_num = zeros(num_words)
    p_abusive_sum = 0.0
    p_normal_num = zeros(num_words)
    p_normal_sum = 0.0
    for i in range(num_doc):
        if class_datas[i] == 1:
            p_abusive_num += train_datas[i]
            p_abusive_sum += sum(train_datas)
        else:
            p_normal_num += train_datas[i]
            p_normal_sum += sum(train_datas)
    p_abusive_vec = p_abusive_num / p_abusive_sum
    p_normal_vec = p_normal_num / p_normal_sum
    '''
    # 解决0值影响和数据下溢
    p_abusive_num = ones(num_words)
    p_abusive_sum = 2.0
    p_normal_num = ones(num_words)
    p_normal_sum = 2.0
    for i in range(num_doc):
        if class_datas[i] == 1:
            p_abusive_num += train_datas[i]
            p_abusive_sum += sum(train_datas)
        else:
            p_normal_num += train_datas[i]
            p_normal_sum += sum(train_datas)
    p_abusive_vec = log(p_abusive_num / p_abusive_sum)
    p_normal_vec = log(p_normal_num / p_normal_sum)

    return p_abusive, p_abusive_vec, p_normal_vec


if __name__ == '__main__':
    # 加载数据生成词汇表
    datas, classes = load_datas()
    vocab = create_vocabulary(datas)

    # 生成词汇表向量
    datas_vecs = []
    for doc in datas:
        datas_vecs.append(to_words_vec(vocab, doc))

    # 获得贝叶斯概率向量
    p_abusive, p_abusive_vec, p_normal_vec = bayes_classify(array(datas_vecs), array(classes))

    # 训练 ---> 泛化
    # 测试样本
    # 等式两边取log简化计算
    # p_abusive_vec和p_normal_vec只是之前的估计概率
    # samplex_vec分别乘以它们得到样本的估计概率作为此样本的p(w|ci)
    sample1 = ["love", "my", "dalmation"]
    sample1_vec = array(to_words_vec(vocab, sample1))
    p0 = sum(sample1_vec * p_abusive_vec) + log(p_abusive)
    p1 = sum(sample1_vec * p_normal_vec) + log(1.0 - p_abusive)
    if p1 > p0:
        print("example1 is abusive")
    else:
        print("example1 is normal")
    sample2 = ["stupid", "garbage"]
    sample2_vec = array(to_words_vec(vocab, sample2))
    p0 = sum(sample2_vec * p_abusive_vec) + log(p_abusive)
    p1 = sum(sample2_vec * p_normal_vec) + log(1.0 - p_abusive)
    if p1 > p0:
        print("example2 is abusive")
    else:
        print("example2 is normal")

