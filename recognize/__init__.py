from recognize.hmm import HMMTagger

hmm_tagger = HMMTagger()

hmm_tagger.load(filename="tagger.hmm.json")


def tag(sentence):
    return hmm_tagger.tag(sentence)


