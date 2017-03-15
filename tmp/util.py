# encoding=utf-8
import jieba

from config import data_path
from segment.stop_words import stop_words


def single(input, output):
    input = data_path(input)
    fr = open(input, 'r')
    output = data_path(output)
    fw = open(output, 'w')

    count = 0
    for line in fr:
        item = line.split(" ")
        if len(item) < 2:
            continue

        # distinct
        if len(item[0]) > 2 * 3:
            out_str = "%s %d\n" % (item[0], int(item[1]))
            fw.write(out_str)
        else:
            count += 1
    print(count)


def trim(line):
    result = ''
    for ch in line:
        if ch in stop_words:
            continue
        if ch in {' '}:
            continue
        result += ch
    return result


def cut(input, output):
    input = data_path(input)
    fr = open(input, 'r')
    output = data_path(output)
    fw = open(output, 'w')

    for line in fr:
        line = trim(line)
        word_list = jieba.cut(line)
        txt = u""
        for word in word_list:
            if word not in stop_words:
                txt += word
                txt += u" "
        txt += u"\n"
        fw.write(txt.encode("utf-8"))
    fw.close()
    fr.close()


def build(input, output):
    input = data_path(input)
    fr = open(input, 'r', encoding='utf-8')
    ouput = data_path(output)
    fw = open(output, 'w', encoding='utf-8')

    word_set = set()

    for line in fr:
        line = line.strip()
        word_set.add(line)

    txt = str(word_set)
    txt = txt.replace(',', ',\n')
    fw.write(txt)

build("phrase.txt", "tmp.txt")
