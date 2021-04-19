import unittest
from pathlib import Path

from src.formal_sequences import IsSemanticSequence
from src.requester import GoogleRequester, read_key_file

REQUESTER = GoogleRequester(read_key_file(Path('apiKeys')))


class TestGoogleSearchEngine(unittest.TestCase):

    def test_search_requests(self):
        self.assertIsNotNone(REQUESTER.search_for_patter(IsSemanticSequence(True), 'theorem'))

    def test_hits_for_word(self):
        self.assertGreaterEqual(REQUESTER.num_results('dog'), 2640000000)
        self.assertGreaterEqual(REQUESTER.num_results('cat'), 3200000000)
        self.assertGreaterEqual(REQUESTER.num_results('human'), 5010000000)

    def test_hits_for_near_words(self):
        self.assertLessEqual(REQUESTER.num_results_near('animal', 'dog'), 6990000000)
        self.assertLessEqual(REQUESTER.num_results_near('cat', 'human'), 3200000000)
        self.assertLessEqual(REQUESTER.num_results_near('cat', 'animal'), 3200000000)

    def test_hits_for_both_words(self):
        self.assertLessEqual(REQUESTER.num_search_and('dog', 'animal'), 3470000000)
        self.assertLessEqual(REQUESTER.num_search_and('dog', 'vehicle'), 3470000000)
        self.assertLessEqual(REQUESTER.num_search_and('dog', 'home'), 3470000000)


if __name__ == '__main__':
    unittest.main()
