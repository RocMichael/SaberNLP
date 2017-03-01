# encoding=utf-8
from config import data_path
from stop_words import stop_words
from utils import my_decode

import pickle
import json


class DAGSegger:
    def __init__(self):
        self.word_dict = {}
        self.data = None

    def load_data(self, filename):
        self.data = file(data_path(filename))

    def update(self):
        # build word_dict
        for line in self.data:
            words = line.split(" ")
            for word in words:
                if word in stop_words:
                    continue
                if self.word_dict.get(word):
                    self.word_dict[word] += 1
                else:
                    self.word_dict[word] = 1

    def save(self, filename="words.txt", code="txt"):
        filename = data_path(filename)
        fw = open(filename, 'wb')
        data = {
            "word_dict": self.word_dict
        }

        # encode and write
        if code == "json":
            txt = json.dumps(data)
            fw.write(txt)
        elif code == "pickle":
            pickle.dump(data, fw)
        if code == 'txt':
            for key in self.word_dict:
                tmp = "%s %d\n" % (key, self.word_dict[key])
                fw.write(tmp.encode("utf-8"))

    def load(self, filename="words.txt", code="txt"):
        filename = data_path(filename)
        fr = open(filename, 'rb')

        # load model
        model = {}
        if code == "json":
            model = json.loads(fr.read())
        elif code == "pickle":
            model = pickle.load(fr)
        elif code == 'txt':
            word_dict = {}
            for line in fr:
                line = line.decode("utf-8")
                tmp = line.split(" ")
                if len(tmp) < 2:
                    continue
                word_dict[tmp[0]] = int(tmp[1])
            model = {"word_dict": word_dict}

        # update word dict
        word_dict = model["word_dict"]
        for key in word_dict:
            key2 = key  # to unicode
            if self.word_dict.get(key):
                self.word_dict[key2] += word_dict[key]
            else:
                self.word_dict[key2] = word_dict[key]

    def build_dag(self, sentence):
        dag = {}
        for start in range(len(sentence)):
            tmp = [start + 1]
            for stop in range(start+1, len(sentence)+1):
                fragment = sentence[start:stop]
                if (fragment in self.word_dict.keys()) and (stop not in tmp):
                    tmp.append(stop)
            dag[start] = tmp
        return dag

    def predict(self, sentence):
        Len = len(sentence)
        route = [(0, 0)] * Len
        dag = self.build_dag(sentence)

        # dynamic search
        for i in range(Len-1, -1, -1):
            candidates = []
            for x in dag[i]:
                word_count = self.word_dict.get(sentence[i:x], 0)
                candidates.append((x, word_count))
            # get max
            max_count = -1
            max_item = None
            for item in candidates:
                if item[1] > max_count:
                    max_count = item[1]
                    max_item = item
            route[i] = max_item[0]
        return route

    def cut(self, sentence):
        sentence = my_decode(sentence)
        route = self.predict(sentence)
        next = 0
        word_list = []
        i = 0
        while i < len(sentence):
            next = route[i]
            word_list.append(sentence[i:next])
            i = next
        return word_list

    def test(self):
        cases = [
            "我来到北京清华大学",
            "长春市长春节讲话",
            "我们去野生动物园玩",
            "我只是做了一些微小的工作",
            "国庆节我在研究中文分词"
        ]
        for case in cases:
            result = self.cut(case)
            for word in result:
                print(word)
            print('')


if __name__ == '__main__':
    s = DAGSegger()
    # s.load_data("people_daily.txt")
    # s.setup()
    s.load("dict.txt")
    s.test()