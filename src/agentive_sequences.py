'''
Provide the semantic sequences for the role agentive.
'''

from spacy.symbols import *
from spacy.tokens.doc import Doc

from src.semantic_sequence import SemanticSequence, MASK, to_bert_seq
from src.spacy_utils import ROOT, get_ancestor


class ToANew(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return 'to(.*?)(\sa|) new ' + qualia_theorem

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'to * a new ' + qualia_theorem

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('to {} a new {}'.format(MASK, qualia_theorem), qualia_theorem),
                to_bert_seq('to {} new {}'.format(MASK, qualia_theorem), qualia_theorem)]

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        qualia_theorem_token = tokenized_seq[end]
        return get_ancestor(qualia_theorem_token, [ROOT, xcomp], VERB)


class ToAComplete(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return 'to(.*?)(\sa|) complete {}'.format(qualia_theorem)

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'to * a complete ' + qualia_theorem

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('to {} a complete {}'.format(MASK, qualia_theorem), qualia_theorem),
                to_bert_seq('to {} complete {}'.format(MASK, qualia_theorem), qualia_theorem)]

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        qualia_theorem_token = tokenized_seq[end]
        return get_ancestor(qualia_theorem_token, [ROOT, xcomp], VERB)


class NewHasBeen(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return '(a\s|)new {} has been'.format(qualia_theorem)

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'a new {} has been *'.format(qualia_theorem)

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('a new {} has been {}'.format(qualia_theorem, MASK), qualia_theorem),
                to_bert_seq('new {} has been {}'.format(qualia_theorem, MASK), qualia_theorem)]

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        been_tok = tokenized_seq[end]
        return get_ancestor(been_tok, [ROOT, ccomp], VERB)


class CompleteHasBeen(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return '(a\s|)complete {} has been'.format(qualia_theorem)

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'a complete {} has been *'.format(qualia_theorem)

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        been_tok = tokenized_seq[end]
        return get_ancestor(been_tok, [ROOT, ccomp], VERB)


class ToNew(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return 'to(.*?) new ' + qualia_theorem

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'to * new ' + qualia_theorem

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('to {} new {}'.format(MASK, qualia_theorem), qualia_theorem)]

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        qualia_theorem_token = tokenized_seq[end]
        return get_ancestor(qualia_theorem_token, [ROOT, xcomp], VERB)


class ToComplete(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return 'to(.*?) complete {}'.format(qualia_theorem)

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'to * complete ' + qualia_theorem

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('to {} complete {}'.format(MASK, qualia_theorem), qualia_theorem)]

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        qualia_theorem_token = tokenized_seq[end]
        return get_ancestor(qualia_theorem_token, [ROOT, xcomp], VERB)
