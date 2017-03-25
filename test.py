# encoding=utf-8

from recognize import tag
from segment import cut, hmm_cut, dict_cut, dag_segger
from segment import get_abstract

import os
import jieba

import os


def data_path(filename):
    return os.path.join(os.path.dirname(__file__), "%s" % filename)


def test_seg():
    cases = [
        "你们传授",
        "我来到北京清华大学",
        "长春市长春节讲话",
        "我们在野生动物园玩",
        "我只是做了一些微小的工作",
        "国庆节我在研究中文分词",
        "比起生存还是死亡来忠诚与背叛可能更是一个问题"
    ]
    for case in cases:
        result = cut(case)
        for word in result:
            print(word)
        print('')


def text_seg():
    fr = open(data_path('tmp/news.txt'), 'r', encoding='utf-8')
    fw = open(data_path('tmp/tmp.txt'), 'w', encoding='utf-8')
    for line in fr:
        print(cut(line))


def test_tag():
    cases = [
        "给你们传授一点人生的经验",
        "我来到北京清华大学",
        "长春市长春节讲话",
        "我们在野生动物园玩",
        "我只是做了一些微小的工作",
        "国庆节我在研究中文分词",
        "比起生存还是死亡来忠诚与背叛可能更是一个问题"
    ]
    for case in cases:
        result = tag(case)
        print(result)


def test_abstract():
    fr = open(data_path('tmp/news.txt'), encoding='utf-8')

    case = ''
    for line in fr:
        line = line.strip()
        if line == '####':
            result = get_abstract(case)
            print(result)
            case = ''
        else:
            case += line

if __name__ == '__main__':
    # test_tag()
    test_seg()
    # test_abstract()
    # text_seg()
