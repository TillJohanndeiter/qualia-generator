import unittest
from src.constitutive_sequences import *
from src.spacy_utils import token_sequences_to_str_seq


class ConstitutiveRoleCase(unittest.TestCase):

    def test_is_made_up_of(self):
        is_made_up_of = IsMadeUpOf(False)

        self.assertEqual(is_made_up_of.get_regular_expression('PC'), 'PC is made up of')

        matching_words = is_made_up_of.extract_qualia_elements('PC',
                                                         'PC is made up of golden banana. Additional PC is made up of metal')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['banana'], ['metal']])

        matching_words = is_made_up_of.extract_qualia_elements('device', 'An electronic device is made up of bolts.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['bolts']])

        matching_words = is_made_up_of.extract_qualia_elements('bolt', 'Furthermore the additional bolt is made up of metal.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['metal']])

    def test_made_of(self):
        is_made_of = IsMadeOf(False)

        self.assertEqual(is_made_of.get_regular_expression('PC'), 'PC is made of')

        matching_words = is_made_of.extract_qualia_elements('PC',
                                                      'PC is made of golden banana. Additional PC is made of metal')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['banana'], ['metal']])

        matching_words = is_made_of.extract_qualia_elements('device', 'An electronic device is made of bolts.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['bolts']])

        matching_words = is_made_of.extract_qualia_elements('bolt', 'Furthermore the additional bolt is made of metal.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['metal']])

    def test_comprises(self):
        comprises = Comprises(False)

        self.assertEqual(comprises.get_regular_expression('PC'), 'PC comprises(\sof|)')

        matching_words = comprises.extract_qualia_elements('Pizza',
                                                     'Pizza comprises hamburger. '
                                                     'Additionally we celebrate pizza comprises nice salami.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['hamburger'], ['salami']])

        matching_words = comprises.extract_qualia_elements('bolt', 'The bolt comprises of '
                                                             'metal which snap fits over one component and has spacer section on other side')
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['metal']])

        matching_words = comprises.extract_qualia_elements('Students',
                                                     'The students '
                                                     'comprises of tears and depressions')
        self.assertEqual(token_sequences_to_str_seq(matching_words), [['tears']])

    def test_consist(self):
        consist_of_pattern = ConsistsOf(False)

        self.assertEqual(consist_of_pattern.get_regular_expression('PC'), 'PC consist(\sof|)')

        matching_words = consist_of_pattern.extract_qualia_elements('PC',
                                                              'PC consist of golden banana. Additional PC consist of metal')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['banana'], ['metal']])

        matching_words = consist_of_pattern.extract_qualia_elements('Car',
                                                              'My car consist of golden bolts and other components.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['bolts']])

        matching_words = consist_of_pattern.extract_qualia_elements('Students',
                                                              'The students '
                                                              'consists of tears and depressions')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['tears']])

        matching_words = consist_of_pattern.extract_qualia_elements('Bicycles',
                                                              'Bicycles consists of motorcycles.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['motorcycles']])

    def test_are_made_of(self):
        are_made_of = AreMadeOf(True)

        self.assertEqual(are_made_of.get_regular_expression('Computers'), 'Computers are made of')

        matching_words = are_made_of.extract_qualia_elements('Computers',
                                                       'Computers are made of golden banana. Computers are made of metal.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['banana'], ['metal']])

        matching_words = are_made_of.extract_qualia_elements('devices', 'All electronic devices are made of bolts.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['bolts']])

        matching_words = are_made_of.extract_qualia_elements('bolts', 'Furthermore the additional bolts are made of metal.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['metal']])

    def test_are_made_up_of(self):
        are_made_up_of = AreMadeUpOf(True)

        self.assertEqual(are_made_up_of.get_regular_expression('Computers'), 'Computers are made up of')

        matching_words = are_made_up_of.extract_qualia_elements('Computers',
                                                          'Computers are made up of golden banana. Computers are made up of metal.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['banana'], ['metal']])

        matching_words = are_made_up_of.extract_qualia_elements('devices', 'All electronic devices are made up of bolts.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['bolts']])

        matching_words = are_made_up_of.extract_qualia_elements('bolts',
                                                          'Furthermore the additional bolts are made up of metal.')

        self.assertEqual(token_sequences_to_str_seq(matching_words), [['metal']])


if __name__ == '__main__':
    unittest.main()
