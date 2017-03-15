from config import data_path


def build(filename):
    fr = open(filename, 'r', encoding='utf-8')

    word_set = set()

    for line in fr:
        line = line.strip()
        word_set.add(line)
    return word_set

DEFAULT = {
    '我': 'pronoun',
    '我们': 'pronoun',
    '你们': 'pronoun',
    '给': 'verb',
    '春节': 'noun',
    '玩': 'verb',
    '玩耍': 'verb',
    '只是': 'adv',
    '忠诚': 'noun',
    '可能': 'adv',
}

PUNCT = {
    "，",
    "。",
    "“",
    "”",
    "？",
    "！",
    "：",
    "《",
    "》",
    "、",
    "；",
    "·",
    "‘ ",
    "’",
    "──",
}

PHRASE = build(data_path("phrase.txt"))


LOCATION = build(data_path("location.txt"))


def filter_punct(word, tag):
    if word in PUNCT:
        return 'punctuation'
    elif tag == 'punctuation':
        if word in DEFAULT:
            return DEFAULT[word]
        else:
            return 'noun'
    return tag


def filter_location(word, tag):
    if word in LOCATION:
        return 'location'
    return tag


def filter_phrase(word, tag):
    if word in PHRASE:
        return 'phrase'
    return tag

FILTERS = [filter_punct, filter_location, filter_phrase]


def main_filter(words, tags, filters=FILTERS):
    if len(words) != len(tags):
        return tags
    for i in range(len(words)):
        word = words[i]
        tag = tags[i]
        for the_filter in filters:
            tag = the_filter(word, tag)
        tags[i] = tag
    return tags

