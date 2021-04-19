import unittest
from src.agentive_sequences import *
from src.spacy_utils import token_sequences_to_str_seq


class AgentiveRoleCase(unittest.TestCase):

    def test_to_a_new(self):
        a_new = ToANew(False)

        self.assertEqual(a_new.get_regular_expression('Computer'), 'to(.*?)(\sa|) new Computer')

        matching_words = a_new.extract_qualia_elements('car',
                                                 "Therefore to carefully test a new car.")
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['test']])

        matching_words = a_new.extract_qualia_elements('girl', 'They want to easily love a new girl.')
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['love']])

        matching_words = a_new.extract_qualia_elements('car', 'After that we want to carefully buy new car.')
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['buy']])

    def test_to_a_complete(self):
        a_complete_pattern = ToAComplete(False)

        self.assertEqual(a_complete_pattern.get_regular_expression('Computer'),
                         'to(.*?)(\sa|) complete Computer')

        matching_words = a_complete_pattern.extract_qualia_elements('car',
                                                              'Therefore to carefully test complete car.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['test']])

        matching_words = a_complete_pattern.extract_qualia_elements('girl', 'They want to easily love complete girl.')
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['love']])

        matching_words = a_complete_pattern.extract_qualia_elements('car',
                                                              'After that we want to carefully buy a complete car.')
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['buy']])

    def test_new_has_been(self):
        new_has_been = NewHasBeen(False)

        self.assertEqual(new_has_been.get_regular_expression('Computer'), '(a\s|)new Computer has been')

        matching_words = new_has_been.extract_qualia_elements('car',
                                                        "A new car has been here bought.A new car has been destroyed.")

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['bought'], ['destroyed']])

        matching_words = new_has_been.extract_qualia_elements('window', 'After that new window has been finally built')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['built']])

        matching_words = new_has_been.extract_qualia_elements('car', 'My final advice was that a new car has been cleared.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['cleared']])

    def test_complete_has_been(self):
        complete_has_been = CompleteHasBeen(False)

        self.assertEqual(complete_has_been.get_regular_expression('computer'), '(a\s|)complete computer has been')

        matching_words = complete_has_been.extract_qualia_elements('car',
                                                             "A complete car has been here bought. A complete car has been destroyed.")

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['bought'], ['destroyed']])

        matching_words = complete_has_been.extract_qualia_elements('window',
                                                             'After that the complete window has been finally built')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['built']])

        matching_words = complete_has_been.extract_qualia_elements('car',
                                                             'My final advice was that the complete car has been cleared.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['cleared']])

    def test_to_new(self):
        a_new = ToNew(True)

        self.assertEqual(a_new.get_regular_expression('Computers'), 'to(.*?) new Computers')

        matching_words = a_new.extract_qualia_elements('cars',
                                                 "Therefore to carefully test new cars.")
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['test']])

        matching_words = a_new.extract_qualia_elements('girls', 'They want to easily love new girls.')
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['love']])

        matching_words = a_new.extract_qualia_elements('cars', 'After that we want to carefully buy new cars.')
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['buy']])

    def test_to_complete(self):
        a_complete_pattern = ToComplete(True)

        self.assertEqual(a_complete_pattern.get_regular_expression('Computers'),
                         'to(.*?) complete Computers')

        matching_words = a_complete_pattern.extract_qualia_elements('cars',
                                                              'Therefore to carefully test complete cars.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['test']])

        matching_words = a_complete_pattern.extract_qualia_elements('girls', 'They want to easily love complete girls.')
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['love']])

        matching_words = a_complete_pattern.extract_qualia_elements('cars',
                                                              'After that we want to carefully buy complete cars.')
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['buy']])


if __name__ == '__main__':
    unittest.main()
