import re

from spacy.tokens import Token, Doc

from src.spacy_utils import LANG_MODEL

VOWELS = ['a', 'e', 'i', 'o', 'u']
MASK = '[MASK]'


def to_bert_seq(sentence: str, qualia_theorem: str):
    '''
    Convert sentence to input for bert by replace a|an and append mask to sentence.
    :param sentence: sentence to covert
    :param qualia_theorem: theorem which is part of the sentence
    :return: converted sentence
    '''
    if qualia_theorem[0] in VOWELS:
        sentence = sentence.replace('a|an', 'an')
    else:
        sentence = sentence.replace('a|an', 'a')

    if MASK not in sentence:
        sentence = sentence + ' ' + MASK
    return sentence


def _calc_start_end_indices_of_matches(regex: str, word_seq: str):
    '''
    Calculate list of (start_idx, end_idx) of regex in sequence
    :param regex: regex
    :param word_seq: whitespace separated token sequence
    :return: list of (start_idx, end_idx) of regex matches in token_ws_sep
    '''
    temp = re.finditer(regex.lower(), word_seq)
    indices = [(m.start(0), m.end(0)) for m in temp]
    return [(word_seq.count(' ', 0, start), word_seq.count(' ', 0, end))
            for (start, end) in indices]


class SemanticSequence:
    '''
    Abstract class for semantically theorem sequences, which are used to generate
    qualia elements. Provide regular expression, google clue, bert input and extraction
    for a qualia element using decency tree.
    '''

    def __init__(self, is_plural):
        self.is_plural = is_plural

    def get_regular_expression(self, qualia_theorem: str) -> str:
        '''
        Generate regular expression for theorem sequence including qualia theorem.
        :param qualia_theorem: will be placed into regular expression
        :return: Regex compatible expression
        '''

        raise AssertionError('Abstract Class SemanticSequence has been initiated')

    def get_search_requests(self, qualia_theorem: str) -> str:
        '''
        Generate search request for theorem sequence including qualia theorem.
        :param qualia_theorem: will be placed into the request.
        :return: Regex compatible expression
        '''
        raise AssertionError('Abstract Class SemanticSequence has been initiated')

    def _handle_pattern_found(self, tokenized_seq: Doc, start: int, end: int):
        '''
        Extract qualia element from tokenized_seq by using indices start and end
        of a matching semantic_seq and dependency tree of spacy.
        :param tokenized_seq: Tokenized sequence from which element should be extracted
        :param start: start of match
        :param end: end of match
        :return: extracted qualia elements
        '''

        raise AssertionError('Abstract Class SemanticSequence has been initiated')

    def get_bert_input(self, qualia_theorem: str) -> [str]:
        '''
        Generate bert input sequence including qualia theorem.
        :param qualia_theorem: will be placed into the input.
        :return: Bert compatible sequence
        '''
        return [to_bert_seq(self.get_search_requests(qualia_theorem), qualia_theorem)]

    def extract_qualia_elements(self, qualia_theorem: str, sequence: str) -> [Token]:
        '''
        Extract qualia elements from sequence.
        :param qualia_theorem: qualia theorem for that elements are collected
        :param sequence: sequence used for extraction
        :return: extracted qualia elements
        '''

        regex = self.get_regular_expression(qualia_theorem)

        tokenized_seq = LANG_MODEL(sequence)

        sequence_token_ws_sep = ' '.join([x.orth_ for x in tokenized_seq]).lower()

        indices = _calc_start_end_indices_of_matches(regex, sequence_token_ws_sep)

        qualia_elements = []

        for (start, end) in indices:
            if end < len(tokenized_seq):
                match = self._handle_pattern_found(tokenized_seq, start, end)

                if isinstance(match, Token):
                    match = [match]
                qualia_elements.append(match)

        return qualia_elements

    def __repr__(self):
        return self.__class__.__name__
