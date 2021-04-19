'''
Provide the semantic sequences for the role constitutive.
'''

from spacy.symbols import *
from spacy.tokens.doc import Doc

from src.semantic_sequence import SemanticSequence, to_bert_seq
from src.spacy_utils import get_ancestor, get_child


class IsMadeUpOf(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return qualia_theorem + ' is made up of'

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'a|an {} is made up of'.format(qualia_theorem)

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        of_token = tokenized_seq[end]
        return get_ancestor(of_token, nmod, NOUN)


class IsMadeOf(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return qualia_theorem + ' is made of'

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'a|an {} is made of'.format(qualia_theorem)

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        of_token = tokenized_seq[end]
        return get_ancestor(of_token, nmod, NOUN)


class Comprises(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return qualia_theorem + ' comprises(\sof|)'

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'a|an {} comprises'.format(qualia_theorem)

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('a|an {} comprises'.format(qualia_theorem), qualia_theorem),
                to_bert_seq('a|an {} comprises of'.format(qualia_theorem), qualia_theorem)]

    def _handle_pattern_found(self, tokenized_seq, start, end):
        comprises_token = tokenized_seq[start + 1]
        return get_child(comprises_token, [nmod, dobj], NOUN)


class ConsistsOf(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return qualia_theorem + ' consist(\sof|)'

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'a|an {} consists of'.format(qualia_theorem)

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int) -> str:
        consists_token = tokenized_seq[start + 1]
        return get_child(consists_token, [nmod, dobj], NOUN)


class AreMadeOf(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return qualia_theorem + ' are made of'

    def get_search_requests(self, qualia_theorem: str) -> str:
        return self.get_regular_expression(qualia_theorem)

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        made_token = tokenized_seq[start + 2]
        return get_child(made_token, nmod, NOUN)


class AreMadeUpOf(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return qualia_theorem + ' are made up of'

    def get_search_requests(self, qualia_theorem: str) -> str:
        return self.get_regular_expression(qualia_theorem)

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        of_token = tokenized_seq[end]
        return get_ancestor(of_token, nmod, NOUN)


class ComprisesPlu(Comprises):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return qualia_theorem + ' comprise'

    def get_search_requests(self, qualia_theorem: str) -> str:
        return '{} comprise'.format(qualia_theorem)

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('{} comprise'.format(qualia_theorem), qualia_theorem)]


class ConsistsOfPlu(ConsistsOf):

    def get_search_requests(self, qualia_theorem: str) -> str:
        return '{} consists of'.format(qualia_theorem)
