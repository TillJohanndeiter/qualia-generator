import unittest

from src.spacy_utils import token_sequences_to_str_seq
from src.telic_sequences import *


class TelicRoleCase(unittest.TestCase):

    def test_is_used_to(self):
        used_to = IsUsedTo(False)

        self.assertEqual(used_to.get_regular_expression('Human'), '(a\s|an\s|)Human is used')

        matching_words = used_to.extract_qualia_elements('Human',
                                                         'Human is used to animals. Additional human is used to cats')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['animals'], ['cats']])

        matching_words = used_to.extract_qualia_elements('Human', 'A Human is used to be loved.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['loved']])

        matching_words = used_to.extract_qualia_elements('Human', 'A Human is used to sacrifice')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['sacrifice']])

        matching_words = used_to.extract_qualia_elements('computer',
                                                         'A computer is used to do things')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['things']])

    def test_purpose_of_a(self):
        purpose_of = PurposeOfA(False)

        self.assertEqual(purpose_of.get_regular_expression('Human'),
                         'purpose of(\sa|\san|) Human is')

        matching_words = purpose_of.extract_qualia_elements('Satanism',
                                                            "And the purpose of Satanism is to destroy humanity. "
                                                            "Furthermore the purpose of Satanism is sacrifice. Finally"
                                                            "the purpose of satanism is to be destroyed")

        self.assertEqual(token_sequences_to_str_seq(matching_words),
                         [['destroy', 'humanity'], ['sacrifice'], ['destroyed']])

        matching_words = purpose_of.extract_qualia_elements('tank',
                                                            'I want to recognize that the purpose of a tank is war')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['war']])

        matching_words = purpose_of.extract_qualia_elements('children',
                                                            'To conclude the purpose of children is to be loved')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['loved']])

        matching_words = purpose_of.extract_qualia_elements('children',
                                                            'Finally we have to say that the purpose of children is love')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['love']])

        matching_words = purpose_of.extract_qualia_elements('bicycle',
                                                            'The purpose of a bicycle is to be free ride')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['ride']])

        matching_words = purpose_of.extract_qualia_elements('bicycle',
                                                            'The purpose of a bicycle is to learn')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['learn']])

        matching_words = purpose_of.extract_qualia_elements('bicycle',
                                                            'The purpose of a bicycle is to be the norm')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['norm']])

    def test_are_used_to(self):
        used_to = AreUsedTo(True)

        self.assertEqual(used_to.get_regular_expression('Humans'), 'Humans are used')

        matching_words = used_to.extract_qualia_elements('Humans',
                                                         'Humans are used to animals. Additional humans are used to cats')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['animals'], ['cats']])

        matching_words = used_to.extract_qualia_elements('Humans', 'Humans are used to be loved.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['loved']])

        matching_words = used_to.extract_qualia_elements('Dogs', 'Dogs are used to sacrifice')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['sacrifice']])

        matching_words = used_to.extract_qualia_elements('Dogs',
                                                         'Dogs are used to sacrifice humans')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['sacrifice', 'humans']])


if __name__ == '__main__':
    unittest.main()
