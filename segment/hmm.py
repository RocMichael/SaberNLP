# encoding=utf-8
from config import data_path

import pickle
import json

STATES = {'B', 'M', 'E', 'S'}


def get_tags(src):
    tags = []
    if len(src) == 1:
        tags = ['S']
    elif len(src) == 2:
        tags = ['B', 'E']
    else:
        m_num = len(src) - 2
        tags.append('B')
        tags.extend(['M'] * m_num)
        tags.append('S')
    return tags


def cut_sent(src, tags):
    word_list = []
    start = -1
    started = False
    if len(tags) != len(src):
        return None
    for i in range(len(tags)):
        if tags[i] == 'S':
            if started:
                started = False
                word_list.append(src[start:i])  # for tags: r"BM*S"
            word_list.append(src[i])
        elif tags[i] == 'B':
            if started:
                word_list.append(src[start:i])  # for tags: r"BM*B"
            start = i
            started = True
        elif tags[i] == 'E':
            started = False
            word = src[start:i+1]
            word_list.append(word)
        elif tags[i] == 'M':
            continue
    return word_list


class HMMSegger:
    def __init__(self):
        self.trans_mat = {}  # trans_mat[status][status] = prob
        self.emit_mat = {}  # emit_mat[status][observe] = prob
        self.init_vec = {}  # init_vec[status] = prob
        self.state_count = {}  # state_count[status] = prob
        self.data = None

    def setup(self):
        for state in STATES:
            # build trans_mat
            self.trans_mat[state] = {}
            for target in STATES:
                self.trans_mat[state][target] = 0.0
            # build emit_mat
            self.emit_mat[state] = {}
            # build init_vec
            self.init_vec[state] = 0
            # build state_count
            self.state_count[state] = 0

    def load_data(self, filename):
        self.data = file(data_path(filename))
        self.setup()

    def save(self, filename="hmm.model", code="json"):
        filename = data_path(filename)
        fw = open(filename, 'wb')
        data = {
            "trans_mat": self.trans_mat,
            "emit_mat": self.emit_mat,
            "init_vec": self.init_vec,
        }
        if code == "json":
            txt = json.dumps(data)
            fw.write(txt)
        elif code == "pickle":
            pickle.dump(data, fw)

    def load(self, filename="hmm.model", code="json"):
        filename = data_path(filename)
        fr = open(filename, 'rb')
        if code == "json":
            model = json.loads(fr.read())
        elif code == "pickle":
            model = pickle.load(fr)
        self.trans_mat = model["trans_mat"]
        self.emit_mat = model["emit_mat"]
        self.init_vec = model["init_vec"]

    def train(self):
        line_num = 0
        word_set = set()
        for line in self.data:
            # pre processing
            line = line.strip()
            if not line:
                continue
            line = line.decode("utf-8", "ignore")
            line_num += 1

            # update word_set
            word_list = []
            for i in range(len(line)):
                if line[i] == " ":
                    continue
                word_list.append(line[i])
            word_set = word_set | set(word_list)

            # get tags
            arr = line.split(" ")  # spilt word by whitespace
            line_tags = []
            for item in arr:
                line_tags.extend(get_tags(item))

            # update model params
            for i in range(len(line_tags)):
                if i == 0:
                    self.init_vec[line_tags[0]] += 1
                    self.state_count[line_tags[0]] += 1
                else:
                    self.trans_mat[line_tags[i-1]][line_tags[i]] += 1
                    self.state_count[line_tags[i]] += 1
                    if word_list[i] not in self.emit_mat[line_tags[i]]:
                        self.emit_mat[line_tags[i]][word_list[i]] = 0.0
                    else:
                        self.emit_mat[line_tags[i]][word_list[i]] += 1
        # convert init_vec to prob
        for key in self.init_vec:
            self.init_vec[key] *= 1.0  # convert to float
            self.init_vec[key] /= self.state_count[key]
        # convert trans_mat to prob
        for key1 in self.trans_mat:
            for key2 in self.trans_mat[key1]:
                self.trans_mat[key1][key2] *= 1.0  # convert to float
                self.trans_mat[key1][key2] /= self.state_count[key1]
        # convert emit_mat to prob
        for key1 in self.emit_mat:
            for key2 in self.emit_mat[key1]:
                self.emit_mat[key1][key2] /= self.state_count[key1]

    def predict(self, sentence):
        tab = [{}]
        path = {}
        # init
        for y in STATES:
            tab[0][y] = self.init_vec[y] * self.emit_mat[y].get(sentence[0], 0)
            path[y] = [y]
        # build dynamic search table
        for t in range(1, len(sentence)):
            tab.append({})
            new_path = {}
            for y in STATES:
                items = []
                for y0 in STATES:
                    if tab[t - 1][y0] > 0:
                        prob = tab[t - 1][y0] * self.trans_mat[y0].get(y, 0) * self.emit_mat[y].get(sentence[t], 0)
                        items.append((prob, y0))
                (prob, state) = max(items)
                tab[t][y] = prob
                new_path[y] = path[state] + [y]
            path = new_path
        # search best path
        prob, state = max([(tab[len(sentence) - 1][y], y) for y in STATES])
        return path[state]

    def cut(self, sentence):
        tags = self.predict(sentence)
        return cut_sent(sentence, tags)

    def test(self):
        cases = [
            # u"长春市长春节讲话",
            # u"我们去野生动物园玩",
            u"我只是做了一些微小的工作",
        ]
        for case in cases:
            result = self.cut(case)
            print(result)

if __name__ == '__main__':
    segger = HMMSegger()
    # segger.load_data("people_daily.txt")
    # segger.train()
    # segger.save()
    segger.load()
    segger.test()
