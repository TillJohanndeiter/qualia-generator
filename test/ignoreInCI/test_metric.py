import unittest
from pathlib import Path

from src.metrics import WebPMI, WebP, WebJac
from src.requester import GoogleRequester, read_key_file

SEARCH_ENGINE = GoogleRequester(read_key_file(Path('apiKeys')))

CAT_EXAMPLE = 'cat', ['animal', 'friend', ], ['animal', 'friend']
CAR_EXAMPLE = 'car', ['automobile', 'vehicle'], ['vehicle', 'automobile']
COMPUTER_EXAMPLE = 'computer', ['hardware', 'flesh'], ['hardware', 'flesh']

web_jack = WebJac(SEARCH_ENGINE)
web_p = WebP(SEARCH_ENGINE)
web_pmi = WebPMI(SEARCH_ENGINE)


def sort_by_metric(metric, qualia_theorem, qualia_elements):
    return list(sorted(qualia_elements, reverse=True,
                       key=lambda qualia_element: metric.calc_metric_value(qualia_element, qualia_theorem)))


class WebPTestCases(unittest.TestCase):

    def test_web_p_cat_example(self):
        qualia_theorem, qualia_elements, correct_order = CAT_EXAMPLE
        sorted_list = sort_by_metric(web_p, qualia_theorem, qualia_elements)
        self.assertEqual(correct_order, sorted_list)

    def test_web_p_car_example(self):
        qualia_theorem, qualia_elements, correct_order = CAR_EXAMPLE
        sorted_list = sort_by_metric(web_p, qualia_theorem, qualia_elements)
        self.assertEqual(correct_order, sorted_list)

    def test_web_p_computer_example(self):
        qualia_theorem, qualia_elements, correct_order = COMPUTER_EXAMPLE
        sorted_list = sort_by_metric(web_p, qualia_theorem, qualia_elements)
        self.assertEqual(correct_order, sorted_list)


class WebPMITestCases(unittest.TestCase):

    def test_web_pmi_cat_example(self):
        qualia_theorem, qualia_elements, correct_order = CAT_EXAMPLE
        sorted_list = sort_by_metric(web_pmi, qualia_theorem, qualia_elements)
        self.assertEqual(correct_order, sorted_list)

    def test_web_pmi_car_example(self):
        qualia_theorem, qualia_elements, correct_order = CAR_EXAMPLE
        sorted_list = sort_by_metric(web_pmi, qualia_theorem, qualia_elements)
        self.assertEqual(correct_order, sorted_list)

    def test_web_pmi_computer_example(self):
        qualia_theorem, qualia_elements, correct_order = COMPUTER_EXAMPLE
        sorted_list = sort_by_metric(web_pmi, qualia_theorem, qualia_elements)
        self.assertEqual(correct_order, sorted_list)


class WebJacTestCases(unittest.TestCase):

    def test_web_jack_cat_example(self):
        qualia_theorem, qualia_elements, correct_order = CAT_EXAMPLE
        sorted_list = sort_by_metric(web_jack, qualia_theorem, qualia_elements)
        self.assertEqual(correct_order, sorted_list)

    def test_web_jack_car_example(self):
        qualia_theorem, qualia_elements, correct_order = CAR_EXAMPLE
        sorted_list = sort_by_metric(web_jack, qualia_theorem, qualia_elements)
        self.assertEqual(correct_order, sorted_list)

    def test_web_jack_computer_example(self):
        qualia_theorem, qualia_elements, correct_order = COMPUTER_EXAMPLE
        sorted_list = sort_by_metric(web_jack, qualia_theorem, qualia_elements)
        self.assertEqual(correct_order, sorted_list)


if __name__ == '__main__':
    unittest.main()
