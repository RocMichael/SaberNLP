# encoding=utf-8
from segment.dag import DAGSegger
from segment.hmm import HMMSegger

from utils import my_decode

dag_segger = DAGSegger()
hmm_segger = HMMSegger()

dag_segger.load()
hmm_segger.load()


def __get_single_end(word_list):
    i = 0
    while i < len(word_list):
        word = word_list[i]
        if len(word) > 1:
            return i
        i += 1
    return i


def __merge(seq):
    txt = u""
    for item in seq:
        txt += item
    return txt


def joint_cut(sentence):
    sentence = my_decode(sentence)
    final_list = []
    word_list = dag_segger.cut(sentence)

    i = 0
    while i < len(word_list):
        word = word_list[i]
        if len(word) > 1:
            final_list.append(word)
            i += 1
        else:
            j = i + __get_single_end(word_list[i:])
            if i + 1 == j:
                final_list.append(word)
                i += 1
            else:
                second = __merge(word_list[i:j])
                second_list = hmm_segger.cut(second)
                final_list.extend(second_list)
                i = j

    return final_list


def dict_cut(sentence):
    sentence = my_decode(sentence)
    return dag_segger.cut(sentence)


def hmm_cut(sentence):
    sentence = my_decode(sentence)
    return hmm_segger.cut(sentence)

cut = joint_cut

