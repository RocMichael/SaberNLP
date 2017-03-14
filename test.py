# encoding=utf-8
from segment import cut, hmm_cut, dict_cut
from config import data_path


def test():
    cases = [
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


def cut_text():
    fw = open(data_path("trisolars.my.txt"), "w", encoding="utf-8")
    with open(data_path("trisolars.raw.txt"), "r", encoding="utf-8") as f:
        for line in f:
            r = cut(line)
            s = ""
            for w in r:
                s += w + ' '
            fw.write(s)


if __name__ == '__main__':
    cut_text()
