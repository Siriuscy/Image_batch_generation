import hashlib
import random


def minhash(text, num_hashes):
    # 生成随机种子
    random.seed(42)

    # 初始化最小哈希签名列表
    minhash_signature = [float('inf')] * num_hashes

    # 对每个文本进行哈希计算
    for word in text.split():
        hash_values = []
        for i in range(num_hashes):
            # 使用不同的随机种子生成哈希函数
            random.seed(i)
            hash_value = hashlib.sha1(word.encode('utf-8')).hexdigest()
            hash_values.append(int(hash_value, 16))

        # 更新最小哈希签名
        for i in range(num_hashes):
            if hash_values[i] < minhash_signature[i]:
                minhash_signature[i] = hash_values[i]

    return minhash_signature


def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union


def duplicate_coefficient(texts):
    num_hashes = 100  # 设置哈希函数数量
    signatures = []

    # 计算每个文本的 MinHash 签名
    for text in texts:
        signature = minhash(text, num_hashes)
        signatures.append(signature)

    # 计算重复系数
    total_similarity = 0.0
    for i in range(len(signatures)):
        for j in range(i + 1, len(signatures)):
            similarity = jaccard_similarity(set(signatures[i]), set(signatures[j]))
            total_similarity += similarity

    duplicate_coefficient = (2.0 * total_similarity) / (len(signatures) * (len(signatures) - 1))
    return duplicate_coefficient


# 示例用法
texts = [

    "，这提升了手指的抗冲击能力，使其更加可靠哦。",
    "是的，他们有一款名为TRX-Hand的产品，这款产品采用了柔性驱动的指尖设计，这提升了手指的抗冲击能力，使其更加可靠哦。",

]

coefficient = duplicate_coefficient(texts)
print("Duplicate Coefficient:", coefficient)
