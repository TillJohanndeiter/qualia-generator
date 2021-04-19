'''
Contains abstract class CreationStrategy for general creation of qualia structure
and implementation SearchEngineFactory for creation with google search requests.
For debugging and collection of extracted words, the classes
QualiaElement Role and DebugQualiaStructure are used. Contains
method debug_to_normal_structure which convert DebugQualiaStructure to normal class
QualiaStructure. This is used for pretty print.

'''
import string

from itertools import chain
from datetime import datetime

from pyinflect import getInflection

from src.spacy_utils import LANG_MODEL
from src.formal_sequences import *
from src.agentive_sequences import *
from src.constitutive_sequences import *
from src.telic_sequences import *

from src.requester import WebRequester
from src.metrics import WebBasedMetric, OccurrenceMetric

# Declare used semantic_seq and search Requests.
# True of False decide if singular of plural of qualia theorem is used
# for requests and semantic_seq.

FORMAL = [IsKindOf(False), IsSemanticSequence(False), AndOther(False), OrOther(False),
          SuchAs(True), AndOtherPlu(True), OrOtherPlu(True), Especially(True),
          Including(True)], 'formal'

CONSTITUTIVE = [IsMadeUpOf(False), IsMadeOf(False), Comprises(False), ConsistsOf(False),
                AreMadeUpOf(True), AreMadeOf(True), ComprisesPlu(True), ConsistsOfPlu(True)], \
               'constitutive'

AGENTIVE = [ToANew(False), ToAComplete(False), NewHasBeen(False), CompleteHasBeen(False),
            ToNew(True), ToComplete(True)], 'agentive'

TELIC = [IsUsedTo(False), PurposeOfA(False), AreUsedTo(True), PurposeOf(True)], 'telic'


class WordNotSupportedError(Exception):
    '''
    Exception for qualia theorems, which are not supported by the used
     inflection library pyinflect.
    '''


class QualiaElement:
    '''
    Internal structure of a qualia element for debugging and internal
    purpose. Contain str of qualia element all sources, of which
    qualia element could be extracted and metric_value used for
    order in qualia role.
    '''

    def __init__(self, word: str, metric_value: float = 0, sources=None):
        if sources is None:
            sources = []
        self.str = word
        self.sources = sources
        self.metric_value = metric_value

    def __eq__(self, other) -> bool:
        assert isinstance(other, QualiaElement)
        return self.str == other.str

    def __hash__(self) -> int:
        return self.str.__hash__()

    def __repr__(self) -> str:
        return self.str


class Role:
    '''
    Internal structure of a qualia role used for debugging and internal
    purpose. Dict seq_to_qualia_elements map a Pattern to
    extracted qualia elements. Dict pattern_to_not_resolved map a semantic_seq
    to sources, which could not used to extract a qualia element.
    '''

    def __init__(self, pattern: [SemanticSequence], name: str):
        self.sem_seq_to_qe = {pat: [] for pat in pattern}
        self.pattern_to_not_resolved = {pat: [] for pat in pattern}
        self.name = name

    def get_all_pattern(self) -> [SemanticSequence]:
        '''
        Return all semantic_seq used for creation of role
        :return: all semantic_seq used for creation of role
        '''
        return self.sem_seq_to_qe.keys()

    def add_to_not_resolved(self, pattern: SemanticSequence, source: str):
        '''
        Append source to dict pattern_to_not_resolved, which
        map a semantic_seq to sources of which no qualia element could
        be extracted.
        :param pattern: semantic_seq that couldn't extract qualia element
        from  source
        :param source: source from which no qualia element could
        extracted
        :return: None
        '''
        self.pattern_to_not_resolved[pattern].append(source)

    def __repr__(self) -> str:
        return self.name


class DebugQualiaStructure:
    '''
    Internal structure of a qualia element for debugging and internal
    purpose. Contains qualia theorem and used DebugRoles.
    '''

    def __init__(self, qualia_theorem: str):
        self.qualia_theorem = qualia_theorem
        self.all_roles = [Role(*FORMAL),
                          Role(*CONSTITUTIVE),
                          Role(*AGENTIVE),
                          Role(*TELIC)]

    def __repr__(self):
        return self.qualia_theorem


class QualiaStructure:
    '''
    External/User representation for a qualia structure. Dict role_to_words Map
    the roles to lemmatized extracted qualia elements.
    '''

    def __init__(self, qualia_theorem: str, creation_time: str):
        self.creation_time = creation_time
        self.qualia_theorem = qualia_theorem
        self.role_to_words = {'formal': [], 'constitutive': [], 'agentive': [], 'telic': []}

    def __repr__(self):
        return self.qualia_theorem

    def __eq__(self, o: object) -> bool:
        if isinstance(o, QualiaStructure):
            return self.qualia_theorem == o.qualia_theorem
        return False


def debug_to_normal_structure(debug_qualia_structure: DebugQualiaStructure,
                              top_k: int) -> QualiaStructure:
    '''
    Convert internal representation DebugQualiaStructure to external QualiaStructure
    by merging all extracted Qualia Elements of a role and sort by metric values.
    :param debug_qualia_structure: internal representation
    :param top_k: Limit of maximal qualia elements per role
    :return: external representation
    '''
    qualia_structure = QualiaStructure(qualia_theorem=debug_qualia_structure.qualia_theorem,
                                       creation_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    for debug_role in debug_qualia_structure.all_roles:
        qes_for_roles = list(
            chain.from_iterable(debug_role.sem_seq_to_qe.values()))  # merge
        qes_for_roles = sorted(qes_for_roles, key=lambda a: a.metric_value,
                               reverse=True)  # sort by value
        qes_for_roles = list(dict.fromkeys(qes_for_roles))  # rm duplicates
        qes_for_roles = qes_for_roles[:top_k]
        qualia_structure.role_to_words[debug_role.__repr__()] = [qe.str for qe in
                                                                 qes_for_roles]

    return qualia_structure


class CreationStrategy:
    '''
    Abstract class for a strategy to create a qualia structure by
    method plural_and_singular_of_word. Contains inflection_dict for
    words, which can not be inflected by pyinflect.
    '''

    def __init__(self, inflection_dict):
        self.inflection_dict = inflection_dict

    def generate_qualia_structure(self, qualia_theorem: str) -> DebugQualiaStructure:
        '''
        Abstract method to create DebugQualiaStructure
        :param qualia_theorem: theorem of created DebugQualiaStructure
        :return: DebugQualiaStructure for theorem
        '''

    def inflect_sing_plural(self, noun: str) -> (str, str):
        '''
        Inflect plural and singular for word.
        :param noun: noun to inflect
        :return: sing and plural of noun
        '''

        if noun in self.inflection_dict:
            sing = noun
            plu = self.inflection_dict[noun]
        else:
            lemma = LANG_MODEL(noun)[0].lemma_
            sing = getInflection(lemma, 'NN')
            plu = getInflection(lemma, 'NNS')

            if sing is not None and plu is not None:
                sing = sing[0]
                plu = plu[0]
            else:
                raise WordNotSupportedError(
                    'Pyinflect could not inflect {}. Please add word '
                    'to inflection dict.'.format(noun))

        return sing, plu


def clean_search_item(search_item: str) -> str:
    '''
    Remove all artifacts from google search items like dots
    :param search_item: search_item to clean up
    :return: cleaned up search_item
    '''
    cleaned_item = remove_prefix_and_suffix(search_item, '...')
    cleaned_item = cleaned_item.replace('\n', '')
    cleaned_item = cleaned_item.replace('... ...', '.')
    cleaned_item = cleaned_item.replace('...', '.')
    return cleaned_item


def remove_prefix_and_suffix(str_to_edit: str, pattern: str):
    '''
    Remove prefix and suffix of str_to_edit
    :param str_to_edit: string to edit
    :param pattern: semantic_seq to remove if suffix or prefix equals
    :return: cleaned up str_to_edit with removed semantic_seq
    '''
    if str_to_edit.endswith(pattern):
        str_to_edit = str_to_edit[: -len(pattern)]
    if str_to_edit.startswith(pattern):
        str_to_edit = str_to_edit[len(pattern):]
    return str_to_edit


BLACKLIST = {'xyz'}  # List with strange occurrence that could not be removed automatically


def is_valid_extraction(theorem: str, found_element: str):
    '''
    Validate extracted element by check length, blacklist or is punctuation
    or digit.
    :param theorem: QT for which found_element was extracted
    :param found_element: word extracted from web search by semantic_seq
    :return: True if valid extraction else false
    '''
    return theorem != found_element \
           and len(found_element) > 2 \
           and found_element not in BLACKLIST \
           and not any(c in string.punctuation or c in string.digits for c in found_element)


class SearchEngineStrategy(CreationStrategy):
    '''
    Implementation of abstract class CreationStrategy. Use implementation of WebRequester
    and semantic_seq from DebugQualiaStructure to execute web requests, extract word, validate
    and lemmatize them.
    '''

    def __init__(self, inflection_dict: dict, requester: WebRequester,
                 metric: [OccurrenceMetric, WebBasedMetric]):

        super().__init__(inflection_dict)
        self.search_engine = requester
        self.metric = metric

    def generate_qualia_structure(self, qualia_theorem: str) -> DebugQualiaStructure:
        '''
        Generate debug qualia structure by using google strategy.
        :param qualia_theorem: qualia theorem of created strategy
        :return: created qebug qualia structure
        '''

        structure = DebugQualiaStructure(qualia_theorem=qualia_theorem)

        for role in structure.all_roles:
            sem_seq_to_qe = dict()
            for semantic_seq in role.get_all_pattern():
                sem_seq_to_qe[semantic_seq] = set()
                lemma_to_result = self.__extract_lemmas_from_results(qualia_theorem, role,
                                                                     semantic_seq)
                for lemma, sources in lemma_to_result.items():
                    qualia_element = QualiaElement(lemma, sources=sources)
                    sem_seq_to_qe[semantic_seq].add(qualia_element)

            role.sem_seq_to_qe = sem_seq_to_qe

        self.__sort_qualia_elements(structure)

        return structure

    def __extract_lemmas_from_results(self, theorem: str, role: Role,
                                      semantic_seq: SemanticSequence) -> dict:
        '''
        Extract qualia elements from search results and return
        dict with lemmatize elements to search result.
        :param theorem: qualia theorem of created strategy
        :param role: Role of semantic seq
        :param semantic_seq: Provide executed search request and extraction pattern
        :return: None
        '''
        sing, plu = self.inflect_sing_plural(theorem)
        lemma_to_result = dict()

        tense = plu if semantic_seq.is_plural else sing
        found_items = self.search_engine.search_for_patter(semantic_seq, tense)
        for search_item in found_items:
            try:
                search_item = clean_search_item(search_item)
                token_sequences = semantic_seq.extract_qualia_elements(tense, search_item)
                for token_seq in token_sequences:
                    found_element = ' '.join([token.lemma_.strip() for token in token_seq]).lower()

                    if is_valid_extraction(theorem, found_element):

                        if found_element not in lemma_to_result:
                            lemma_to_result[found_element] = []
                        lemma_to_result[found_element].append(search_item)

            except PatternNotFoundException:
                role.pattern_to_not_resolved[semantic_seq].append(search_item)

        return lemma_to_result

    def __sort_qualia_elements(self, structure: DebugQualiaStructure):
        '''
        Calc the metric values for each qualia element and sort the elements
        according to metric value of each semantic sequence.
        :param structure: Qualia structure to create
        :return: None
        '''
        for role in structure.all_roles:

            self.__calc_metric_values(role, structure)

            for semantic_seq in role.sem_seq_to_qe:
                role.sem_seq_to_qe[semantic_seq] = sorted(
                    role.sem_seq_to_qe[semantic_seq],
                    key=lambda d_qe: d_qe.metric_value, reverse=True)

    def __calc_metric_values(self, role: Role, structure: DebugQualiaStructure):
        '''
        Calculate metric values for the qualia element of the a role.
        :param role: the role
        :param structure: Qualia structure to create
        :return: None
        '''
        metric_values = dict()
        for qualia_element in chain.from_iterable(role.sem_seq_to_qe.values()):

            if qualia_element not in metric_values:
                if isinstance(self.metric, WebBasedMetric):
                    metric_value = self.metric.calc_metric_value(qualia_element.str,
                                                                 structure.qualia_theorem)
                elif isinstance(self.metric, OccurrenceMetric):
                    metric_value = self.metric.calc_metric_value(qualia_element, role)
                else:
                    raise AttributeError('Metric is not an instance of a subclass of'
                                         ' WebBasedMetric or OccurrenceMetric')

                metric_values[qualia_element] = metric_value

            qualia_element.metric_value = metric_values[qualia_element]
