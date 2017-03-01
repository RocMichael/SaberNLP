# encoding=utf-8


def my_decode(sentence):
    if not isinstance(sentence, unicode):
        try:
            sentence = sentence.decode('utf-8')
        except:
            sentence = sentence.decode('gbk', 'ignore')
    return sentence
