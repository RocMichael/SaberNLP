# encoding=utf-8
from segment import cut, hmm_cut, dict_cut


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
        result = dict_cut(case)
        for word in result:
            print(word)
        print('')

if __name__ == '__main__':
    test()
