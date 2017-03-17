# encoding=utf-8
from config import data_path
from recognize import tag
from segment import cut, hmm_cut, dict_cut

import timeit


def test_seg():
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
        result = dict_cut(case)
        for word in result:
            print(word)
        print('')


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

fw = open(data_path("trisolars2.my.txt"), "w", encoding="utf-8")
fr = open(data_path("trisolars.raw.txt", data_dir='tmp'), "r", encoding="utf-8")


def cut_text():
    for line in fr:
        txt = ''
        words = dict_cut(line)
        for word in words:
            txt += word + ' '
        fw.write(txt)


def only_read():
    for line in fr:
        txt = line

if __name__ == '__main__':
    # full_time = timeit.repeat('cut_text()', setup='from __main__ import cut_text', number=1)
    # read_time = timeit.repeat('only_read()', setup='from __main__ import only_read', number=1)
    # for i in range(3):
    #     print(full_time[i], read_time[i], full_time[i]-read_time[i])
    test_tag()
