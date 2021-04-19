import unittest
from src.formal_sequences import *
from src.spacy_utils import token_sequences_to_str_seq, PatternNotFoundException


class FormalRoleCase(unittest.TestCase):

    def test_kind_of(self):
        is_kind_of_pattern = IsKindOf(False)

        self.assertEqual(is_kind_of_pattern.get_regular_expression('Dog'), 'Dog is(\sa|) kind of')

        matching_words = is_kind_of_pattern.extract_qualia_elements('Dog',
                                                                    'Dog is kind of animal. Additional Dog is kind of human')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['animal'], ['human']])

        self.assertEqual(is_kind_of_pattern.get_regular_expression('aunt'), 'aunt is(\sa|) kind of')

        matching_words = is_kind_of_pattern.extract_qualia_elements('aunt',
                                                                    'My aunt is kind of human and likes my turtle.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['human']])

        self.assertEqual(is_kind_of_pattern.get_regular_expression('thing'),
                         'thing is(\sa|) kind of')

        matching_words = is_kind_of_pattern.extract_qualia_elements('thing',
                                                                    'Furthermore that thing is kind of magic.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['magic']])

        self.assertRaises(PatternNotFoundException, is_kind_of_pattern.extract_qualia_elements,
                          'bicycle',
                          'A bicycle is kind of funny.')

    def test_is_pattern(self):
        is_pattern = IsSemanticSequence(False)

        self.assertEqual(is_pattern.get_regular_expression('Dog'), 'Dog is')

        matching_words = is_pattern.extract_qualia_elements('Dog',
                                                            'Dog is a nice animal. Additional Dog is a good friend.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['animal'], ['friend']])

        self.assertEqual(is_pattern.get_regular_expression('Dog'), 'Dog is')

        matching_words = is_pattern.extract_qualia_elements('Dog', 'Dog is an animal.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['animal']])

        self.assertEqual(is_pattern.get_regular_expression('Albert Einstein'), 'Albert Einstein is')

        matching_words = is_pattern.extract_qualia_elements('Dog', 'Dog is an animal.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['animal']])

    def test_such_as(self):
        such_as_pattern = SuchAs(True)
        self.assertEqual(such_as_pattern.get_regular_expression('Computer'), 'such as Computer')

        matching_words = such_as_pattern.extract_qualia_elements('food',
                                                                 'I like pommes such as food. Additionally i eat pizzas such as food.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['pommes'], ['pizzas']])

        matching_words = such_as_pattern.extract_qualia_elements('europeans',
                                                                 'In medieval there were crusaders such as europeans.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['crusaders']])

    def test_and_other(self):
        and_other_pattern = AndOther(True)

        self.assertEqual(and_other_pattern.get_regular_expression('PC'), 'PC(,|) and other')

        matching_words = and_other_pattern.extract_qualia_elements('PC',
                                                                   'PC and other electronic devices. PC and other things.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['devices'], ['things']])

        matching_words = and_other_pattern.extract_qualia_elements('animals',
                                                                   'I very much into animals and other species')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['species']])

        matching_words = and_other_pattern.extract_qualia_elements('people',
                                                                   'After thinking about nice people and other animals i'
                                                                   'would like to start.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['animals']])

        matching_words = and_other_pattern.extract_qualia_elements('bicycles',
                                                                   'Bicycles and other objects.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['objects']])

    def test_or_other(self):
        or_other_pattern = OrOther(True)

        self.assertEqual(or_other_pattern.get_regular_expression('PC'), 'PC(,|) or other')

        matching_words = or_other_pattern.extract_qualia_elements('PC',
                                                                  'PC or other electronic devices. PC or other things.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['devices'], ['things']])

        matching_words = or_other_pattern.extract_qualia_elements('animals',
                                                                  'I very much into animals or other species')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['species']])

        matching_words = or_other_pattern.extract_qualia_elements('people',
                                                                  'After thinking about nice people or other animals i'
                                                                  'would like to start.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['animals']])

        matching_words = or_other_pattern.extract_qualia_elements('bicycles',
                                                                  'Bicycles or other objects.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['objects']])

    def test_especially(self):
        especially = Especially(True)

        self.assertEqual(especially.get_regular_expression('PC'), 'especially PC')

        matching_words = especially.extract_qualia_elements('pizza',
                                                            'I like hamburger especially pizza. We ate salami '
                                                            'especially pizza.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['hamburger'], ['salami']])

        matching_words = especially.extract_qualia_elements('things',
                                                            'I like moving pizzas especially things.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['pizzas']])

    def test_including(self):
        especially = Including(True)

        self.assertEqual(especially.get_regular_expression('PC'), 'including PC')

        matching_words = especially.extract_qualia_elements('pizzas',
                                                            'I like foods including pizzas. We ate many things '
                                                            'including pizzas.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['foods'], ['things']])

        matching_words = especially.extract_qualia_elements('things',
                                                            'I like moving pizzas including things.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['pizzas']])


if __name__ == '__main__':
    unittest.main()
