'''
Provide the semantic sequences for the role formal.
'''

from spacy.symbols import NOUN, VERB, conj, nmod, dobj, nsubj, xcomp
from spacy.tokens.doc import Doc

from src.semantic_sequence import SemanticSequence, to_bert_seq, MASK
from src.spacy_utils import ROOT, get_ancestor, get_child


class IsSemanticSequence(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return qualia_theorem + ' is'

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'a|an {} is a'.format(qualia_theorem)

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        qualia_theorem_token = tokenized_seq[start]
        return get_ancestor(qualia_theorem_token, ROOT, NOUN)


class AndOther(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str):
        return qualia_theorem + '(,|) and other'

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'a|an {} and other'.format(qualia_theorem)

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        other_token = tokenized_seq[end]
        return get_ancestor(other_token, conj, NOUN)


class OrOther(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str):
        return qualia_theorem + '(,|) or other'

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'a|an {} or other'.format(qualia_theorem)

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        other_token = tokenized_seq[end]
        return get_ancestor(other_token, conj, NOUN)


class IsKindOf(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str) -> str:
        return qualia_theorem + ' is(\sa|) kind of'

    def get_search_requests(self, qualia_theorem: str) -> str:
        return 'a|an {} is kind of'.format(qualia_theorem)

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        of_token = tokenized_seq[end]
        return get_ancestor(of_token, [nmod, ROOT], [NOUN])


class SuchAs(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str):
        return 'such as ' + qualia_theorem

    def get_search_requests(self, qualia_theorem: str) -> str:
        return self.get_regular_expression(qualia_theorem)

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('{} such as {}'.format(MASK, qualia_theorem), qualia_theorem)]

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        qualia_theorem_token = tokenized_seq[end]
        return get_ancestor(qualia_theorem_token, [dobj, nsubj], NOUN)


class OrOtherPlu(OrOther):

    def get_search_requests(self, qualia_theorem: str) -> str:
        return '{} or other'.format(qualia_theorem)


class AndOtherPlu(AndOther):

    def get_search_requests(self, qualia_theorem: str) -> str:
        return '{} and other'.format(qualia_theorem)


class Especially(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str):
        return 'especially ' + qualia_theorem

    def get_search_requests(self, qualia_theorem: str) -> str:
        return self.get_regular_expression(qualia_theorem)

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('{} especially {}'.format(MASK, qualia_theorem), qualia_theorem)]

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        qualia_theorem_token = tokenized_seq[end]
        verb_token = get_ancestor(qualia_theorem_token, [ROOT, xcomp], VERB)
        return get_child(verb_token, dobj, NOUN)


class Including(SemanticSequence):

    def get_regular_expression(self, qualia_theorem: str):
        return 'including ' + qualia_theorem

    def get_search_requests(self, qualia_theorem: str) -> str:
        return self.get_regular_expression(qualia_theorem)

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        return [to_bert_seq('{} including {}'.format(MASK, qualia_theorem), qualia_theorem)]

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        qualia_theorem_token = tokenized_seq[end]
        verb_token = get_ancestor(qualia_theorem_token, [ROOT, xcomp], VERB)
        return get_child(verb_token, dobj, NOUN)
