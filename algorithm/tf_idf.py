import math


def get_tf(word, word_dict):
    return word_dict.get(word, 0)


def get_total(word_dict):
    return sum(map(lambda x: word_dict[x], word_dict))


def get_idf(word, word_dict, total):
    tf = word_dict.get(word, 1)
    return math.log(total / tf)


def get_tf_idf(word, word_dict, total):
    tf = get_tf(word, word_dict)
    idf = get_idf(word, word_dict, total)
    return tf * idf
