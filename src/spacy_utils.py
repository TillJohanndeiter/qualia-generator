import spacy
from spacy.tokens import Token



ROOT = 8206900633647566924
LANG_MODEL = spacy.load('en_ud_model_lg')

class PatternNotFoundException(Exception):
    '''
    Exception is used to signalize, that a semantic_seq could not
    extract a theorem.
    '''


def token_sequences_to_str_seq(token_sequences: [[Token]]):
    return [[token.orth_ for token in token_seq]
            for token_seq in token_sequences]


def get_ancestor(token: Token, dep, pos):
    if isinstance(dep, int):
        dep = [dep]
    if isinstance(pos, int):
        pos = [pos]

    for ancestor in token.ancestors:
        if ancestor.dep in dep and ancestor.pos in pos:
            return ancestor

    raise PatternNotFoundException()


def get_child(token: Token, dep, pos):
    if isinstance(dep, int):
        dep = [dep]
    if isinstance(pos, int):
        pos = [pos]

    for child in token.children:
        if child.dep in dep and child.pos in pos:
            return child

    raise PatternNotFoundException()
