import nltk


class FindChunks():

    def __init__(self):
        self.grammar = r"""
                        VPRT: {<.*,compound:lvc,NOUN>(<و,cc,CCONJ><.*conj,NOUN>)?}
                        VPRT: {<.*,compound:lvc,ADJ>(<و,cc,CCONJ><.*conj,ADJ]>)?}
                        VP: {<.*,compound:lvc,NOUN><.*,ADP><.*,NOUN><.*,VERB><.*,AUX>?}
                        VP: {<.*,compound:lvc,NOUN><.*,ADP><.*,NOUN><.*,AUX>?<.*,VERB>}
                        VP: {<.*,ADP><.*,compound:lvc,PRON><.*,VERB><.*,AUX>?}
                        VP: {<.*,ADP><.*,compound:lvc,PRON><.*,AUX>?<.*,VERB>}
                        VP: {<.*,ADP><.*,compound:lvc,NOUN><.*,VERB><.*,AUX>?}
                        VP: {<.*,ADP><.*,compound:lvc,NOUN><.*,AUX>?<.*,VERB>}
                        VP: {<VPRT><.*,VERB><.*,AUX>?}
                        VP: {<VPRT><.*,AUX>?<.*,VERB>}
                        VP: {<.*,AUX>?<.*,VERB>}
                        VP: {<.*,VERB><.*,AUX>*}
                        VP: {<.*,AUX>}
                        AJP: {<.*advmod,ADV>?<.*,ADJ>(<،,punct,PUNCT><.*,ADV>?<.*conj,ADJ]>)+<و,cc,CCONJ><.*,ADV>?<.*conj,ADJ>}
                        AJP: {<.*advmod,ADV>?<.*,ADJ>(<و,cc,CCONJ><.*,ADV>?<.*conj,ADJ>)*}
                        NUMP: {<.*,NUM>+(<و,cc,CCONJ><.*,NUM>+)+}
                        NUMP: {<.*,NUM>+((<،,punct,PUNCT><.*,NUM>)+<و,cc,CCONJ><.*,NUM>)?}
                        NP: {<.*,INTJ><.*vocative,NOUN><AJP>?}
                        NP: {<.*vocative,NOUN><.*,INTJ>}
                        NP: {<.*,NOUN>(<،,punct,PUNCT><.*conj,NOUN>)+<و,cc,CCONJ><.*conj,NOUN>}
                        NP: {<.*,NOUN>(<و,cc,CCONJ><.*conj,NOUN>)+}
                        NP: {<.*,DET>+<.*,NOUN><AJP>?}
                        NP: {<.*,DET>?<NUMP><.*,NOUN><AJP>?}
                        NP: {<.*,DET>?<.*,NOUN><NUMP>}
                        NP: {<.*,AJP>?<.*,NOUN><AJP>?}
                        NP: {<.*,PROPN><.*flat:name,PROPN>*(<،,punct,PUNCT><.*conj,PROPN><.*flat:name,PROPN>*)+<و,cc,CCONJ><.*conj,PROPN><.*flat:name,PROPN>*}
                        NP: {<.*,PROPN><.*flat:name,PROPN>*(<و,cc,CCONJ><.*conj,PROPN><.*flat:name,PROPN>*)+}
                        NP: {<.*,PRON>(<،,punct,PUNCT><.*conj,PRON>)+<و,cc,CCONJ><.*conj,PRON>}
                        NP: {<.*,PRON>(<و,cc,CCONJ><.*conj,PRON>)*}
                        NP: {<NUMP>}
                        ADJP: {<.*advmod,ADV>?<.*,ADJ>(<،,punct,PUNCT><.*,ADV>?<.*conj,ADJ>)+<و,cc,CCONJ><.*,ADV>?<.*conj,ADJ>}
                        ADJP: {<.*advmod,ADV>?<.*,ADJ>(<و,cc,CCONJ><.*,ADV>?<.*conj,ADJ>)*}
                        ADVP: {<.*,ADV>}
                        PP: {<.*,ADP>}
                        INTJP: {<.*case,INTJ>?<.*,INTJ>}
                        PARTP: {<.*,PART>}
                        CCONJP: {<.*,CCONJ>}
                        SCONJP: {<.*,SCONJ>}        
                        """

        self.cp = nltk.RegexpParser(self.grammar)

    def convert_nestedtree2rawstring(self, tree, d=0):
        s = ''
        for item in tree:
            if isinstance(item, tuple):
                s += item[0] + ' '
            elif d >= 1:
                news = self.convert_nestedtree2rawstring(item, d + 1)
                s += news + ' '
            else:
                tag = item._label
                news = '[' + self.convert_nestedtree2rawstring(item, d + 1) + ' ' + tag + ']'
                s += news + ' '
        return s.strip()

    def chunk_sentence(self, pos_taged_tuples):
        return self.cp.parse(pos_taged_tuples)
      
      
#How to use class
from __future__ import unicode_literals
import dadmatools.pipeline.language as language

chunker_dadma = FindChunks()
pips = 'tok,lem,pos,dep' 
nlp = language.Pipeline(pips)

sent = "چشمان سبزش در چهره رنگ‌پریده اش، با بی‌قراری شعله کشیده بودند."
doc = nlp(sent)
dictionary = language.to_json(pips, doc)
chnk_tags = list(zip([i['text'] for i in dictionary[0]],[str(j['text']+','+j['rel']+','+j['pos']) for j in dictionary[0]]))
print(chunker_dadma.convert_nestedtree2rawstring(chunker_dadma.chunk_sentence(chnk_tags)))

