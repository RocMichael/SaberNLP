from config import data_path

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
        self.data = open(data_path(filename))
        self.setup()

    def train(self):
        word_set = set()
        for line in self.data:
            # pre processing
            line = line.strip()
            if not line:
                continue
            line = line.decode("utf-8", "ignore")

            # update word_set
            word_list = []
            for i in range(len(line)):
                if line[i] == " ":
                    continue
                word_list.append(line[i])
            word_set = word_set | set(word_list)

            # get tags
            arr = line.split(" ")
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


if __name__ == '__main__':
    segger = HMMSegger()

