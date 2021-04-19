'''
Provide the semantic sequences for the role telic.
'''
from spacy.symbols import *
from spacy.tokens.doc import Doc

from src.semantic_sequence import SemanticSequence, to_bert_seq, MASK
from src.spacy_utils import ROOT, get_ancestor, get_child, PatternNotFoundException


class PurposeOfA(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return 'purpose of(\sa|\san|) {} is'.format(qualia_theorem)

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'purpose of a|an {} is'.format(qualia_theorem)

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [
            to_bert_seq('purpose of a|an {} is to {}'.format(qualia_theorem, MASK), qualia_theorem),
            to_bert_seq('purpose of a|an {} is to {} {}'.format(qualia_theorem, MASK, MASK),
                        qualia_theorem),
            to_bert_seq('purpose of a|an {} is {}'.format(qualia_theorem, MASK), qualia_theorem),
            to_bert_seq('purpose of a|an {} is {} {}'.format(qualia_theorem, MASK, MASK),
                        qualia_theorem),
            to_bert_seq('purpose of a|an {} is to be {}'.format(qualia_theorem, MASK),
                        qualia_theorem),
            to_bert_seq('purpose of a|an {} is be {}'.format(qualia_theorem, MASK), qualia_theorem)]

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        is_token = tokenized_seq[end]

        try:
            verb = get_child(is_token, xcomp, VERB)
            noun = get_child(verb, dobj, NOUN)
            return [verb, noun]
        except PatternNotFoundException:
            pass

        try:
            return get_child(is_token, xcomp, [VERB, NOUN])
        except PatternNotFoundException:
            pass

        return get_ancestor(is_token, [ccomp, ROOT], NOUN)


class PurposeOf(PurposeOfA):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return 'purpose of {} is'.format(qualia_theorem)

    def get_search_requests(self, qualia_theorem: str) -> str:
        return self.get_regular_expression(qualia_theorem)

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('purpose of {} is to {}'.format(qualia_theorem, MASK), qualia_theorem),
                to_bert_seq('purpose of {} is to {} {}'.format(qualia_theorem, MASK, MASK),
                            qualia_theorem),
                to_bert_seq('purpose of {} is {}'.format(qualia_theorem, MASK), qualia_theorem),
                to_bert_seq('purpose of {} is {} {}'.format(qualia_theorem, MASK, MASK),
                            qualia_theorem),
                to_bert_seq('purpose of {} is to be {}'.format(qualia_theorem, MASK),
                            qualia_theorem),
                to_bert_seq('purpose of {} is be {}'.format(qualia_theorem, MASK), qualia_theorem)]


class IsUsedTo(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return '(a\s|an\s|){} is used'.format(qualia_theorem)

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'a|an {} is used to'.format(qualia_theorem)

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('a|an {} is used to {}'.format(qualia_theorem, MASK), qualia_theorem),
                to_bert_seq('a|an {} is used to {} {}'.format(qualia_theorem, MASK, MASK),
                            qualia_theorem),
                to_bert_seq('a|an {} is used to be {}'.format(qualia_theorem, MASK),
                            qualia_theorem)]

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        used_token = tokenized_seq[end]

        try:
            verb = get_child(used_token, xcomp, [VERB, AUX])
            noun = get_child(verb, dobj, NOUN)
            if verb.orth_ != 'do':
                return [verb, noun]
            return noun
        except PatternNotFoundException:
            pass

        try:
            verb = get_child(used_token, xcomp, VERB)
            return verb
        except PatternNotFoundException:
            pass

        return get_child(used_token, nmod, NOUN)


class AreUsedTo(IsUsedTo):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return '{} are used'.format(qualia_theorem)

    def get_search_requests(self, qualia_theorem: str) -> str:
        return self.get_regular_expression(qualia_theorem)

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('{} are used to {}'.format(qualia_theorem, MASK), qualia_theorem),
                to_bert_seq('{} are used to {} {}'.format(qualia_theorem, MASK, MASK),
                            qualia_theorem),
                to_bert_seq('{} are used to be {}'.format(qualia_theorem, MASK),
                            qualia_theorem)]
