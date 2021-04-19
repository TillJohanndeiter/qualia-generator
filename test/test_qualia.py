import unittest

from src.bert_strategy import BertStrategy
from src.qualia_structure import *
from src.formal_sequences import IsKindOf

INFLECTION_DICT = {}


class FactoryCase(unittest.TestCase):

    def test_sing_plu(self):
        qf = CreationStrategy(INFLECTION_DICT)
        self.assertEqual(qf.inflect_sing_plural('watch'), ('watch', 'watches'))
        self.assertEqual(qf.inflect_sing_plural('dog'), ('dog', 'dogs'))
        self.assertEqual(qf.inflect_sing_plural('computers'), ('computer', 'computers'))


class BertFactoryCase(unittest.TestCase):

    def test_sum_of_prob_equal_1(self):
        factory = BertStrategy(INFLECTION_DICT)
        for pattern in [IsKindOf(False), AndOther(False)]:
            inputs = pattern.get_bert_input('Dog')
            for bert_text in inputs:
                self.assertAlmostEqual(sum(a[1] for a in factory._predict_masks(bert_text)),
                                       1, places=3)


class QualiaElementTest(unittest.TestCase):

    def test_init(self):
        qualia_element = QualiaElement('testWord', 0)
        self.assertEqual(qualia_element.metric_value, 0)
        self.assertEqual(qualia_element.str, 'testWord')

    def test_add_source(self):
        qualia_element = QualiaElement('testWord', 1)
        qualia_element.sources.append('source1')
        self.assertEqual(qualia_element.metric_value, 1)
        self.assertEqual(qualia_element.sources, ['source1'])

    def test_set_rating(self):
        qualia_element = QualiaElement('testWord', 0.5)
        self.assertEqual(qualia_element.metric_value, 0.5)


class QualiaStructureTest(unittest.TestCase):

    def test_type_of_data_structure(self):
        qualia_element = DebugQualiaStructure('testWord')
        self.assertIsInstance(qualia_element.all_roles, (list, SemanticSequence))

    def test_add_word_to_kind_of(self):
        qualia_structure = DebugQualiaStructure('testWord')
        formal_sing = qualia_structure.all_roles[0]
        kind_of = list(formal_sing.get_all_pattern())[0]

        self.assertIsInstance(kind_of, IsKindOf)
        qualia_element = QualiaElement('foundWord', metric_value=0)

        pattern_to_qualia_elements = {kind_of: [qualia_element]}

        formal_sing.sem_seq_to_qe = pattern_to_qualia_elements

        self.assertTrue(qualia_element in qualia_structure.all_roles[0].sem_seq_to_qe[kind_of])
