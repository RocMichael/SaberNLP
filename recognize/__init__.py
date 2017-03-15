from recognize.hmm import HMMTagger
from config import data_path

hmm_tagger = HMMTagger()

hmm_tagger.load(filename=data_path("tagger.hmm.json"))


def tag(sentence):
    return hmm_tagger.tag(sentence)


