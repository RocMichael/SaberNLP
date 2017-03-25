# encoding=utf-8
from algorithm.word_dict import WordDictModel

INF = 1e4


class DAGSegger(WordDictModel):
    def build_dag(self, sentence):
        dag = {}
        for start in range(len(sentence)):
            tmp = {start + 1: 1}
            for stop in range(start+1, len(sentence)+1):
                fragment = sentence[start:stop]
                num = self.word_dict.get(fragment, 1)
                tmp[stop] = INF - num
            for stop in range(start+1):
                tmp[stop] = 0
            dag[start] = tmp
        return dag

    def predict(self, sentence):
        Len = len(sentence)
        # graph = self.build_dag(sentence)  # {i: (stop, num)}

        graph = {
            0: {0:0, 1:8, 2:3},
            1: {0:0, 1:0, 2:7},
            2: {0:0, 1:0, 2:0},
        }

        path = {}
        for i in graph.keys():
            path[i] = {}
            for j in graph.keys():
                path[i][j] = j

        for k in graph.keys():
            for i in graph.keys():
                for j in graph.keys():
                    if graph[i][k] + graph[k][j] < graph[i][j]:
                        graph[i][j] = graph[i][k] + graph[k][j]
                        path[i][j] = path[i][k]

        return graph[0].values()

    def cut(self, sentence):
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



