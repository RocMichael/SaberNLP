# encoding=utf-8
from segment.dag import DAGSegger
from segment.hmm import HMMSegger

from segment.extra import seg_stop_words, abstract_stop_words

import os


def data_path(filename):
    return os.path.join(os.path.dirname(__file__), "%s" % filename)

dag_segger = DAGSegger()
hmm_segger = HMMSegger()

dag_segger.stop_words = seg_stop_words
dag_segger.load(filename=data_path("words.txt"))
hmm_segger.load(filename=data_path("segger.hmm.json"))


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
    return dag_segger.cut(sentence)


def hmm_cut(sentence):
    return hmm_segger.cut(sentence)

cut = joint_cut


from segment.tf_idf import TF_IDF


idf_abstracter = TF_IDF()
idf_abstracter.stop_words = abstract_stop_words
idf_abstracter.load(filename=data_path("words.txt"))
idf_abstracter.build_word_count()


def get_abstract(txt):
    tmp = ""
    for c in txt:
        if c in abstract_stop_words:
            continue
        tmp += c
    words = cut(tmp)
    return idf_abstracter.get_key_words(words)
